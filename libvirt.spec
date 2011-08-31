#
# Conditional build:
%bcond_with	xen		# xen
%bcond_without	xen_proxy		# Xen proxy
%bcond_without	qemu		# Qemu
%bcond_without	polkit		# PolicyKit
%bcond_with	lokkit		# Lokkit
%bcond_with	netcf		# host interfaces support

# Xen is available only on i386 x86_64 ia64
%ifnarch %{ix86} %{x8664} ia64
%undefine	with_xen
%endif
%ifarch i386 i486 i586
%undefine	with_xen
%endif

%if %{without xen}
%undefine	with_xen_proxy
%endif

%ifnarch %{ix86} %{x8664} ppc
%undefine	with_qemu
%endif

Summary:	Toolkit to interact with virtualization capabilities
Name:		libvirt
Version:	0.9.3
Release:	5
License:	LGPL
Group:		Base/Kernel
URL:		http://www.libvirt.org/
Source0:	ftp://ftp.libvirt.org/libvirt/%{name}-%{version}.tar.gz
# Source0-md5:	04f47fad7d0c614af9dcc5d1351c2148
Source1:	%{name}.init
Patch0:		gcrypt.patch
Patch1:		%{name}-sasl.patch
%{?with_lokkit:BuildRequires:	/usr/sbin/lokkit}
BuildRequires:	augeas-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-devel >= 0.6.0
BuildRequires:	curl-devel >= 7.18.0
BuildRequires:	cyrus-sasl-devel
BuildRequires:	device-mapper-devel >= 1.0.0
BuildRequires:	gettext-devel
BuildRequires:	gnutls-devel >= 1.0.25
BuildRequires:	libapparmor-devel
BuildRequires:	libcap-ng-devel
BuildRequires:	libnl1-devel
BuildRequires:	libpcap-devel
BuildRequires:	libselinux-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.6.0
BuildRequires:	libxslt-devel
BuildRequires:	openldap-devel
BuildRequires:	ncurses-devel
%{?with_netcf:BuildRequires:	netcf-devel >= 0.1.4}
BuildRequires:	numactl-devel
BuildRequires:	parted-devel >= 1.8.0
BuildRequires:	perl-tools-pod
%{?with_polkit:BuildRequires:	polkit >= 0.90}
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	sqlite3-devel
BuildRequires:	udev-devel >= 145
# For mount/umount in FS driver
BuildRequires:	util-linux
%{?with_xen:BuildRequires:	xen-devel >= 3.0.4}
# For disk driver
BuildRequires:	xmlrpc-c-devel
BuildRequires:	xorg-lib-libpciaccess-devel
BuildRequires:	yajl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# libxenstore is not versionned properly
%define		_noautoreq	devel(libxenstore.*)

%description
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

Virtualization of the Linux Operating System means the ability to run
multiple instances of Operating Systems concurently on a single
hardware system where the basic resources are driven by a Linux
instance. The library aim at providing long term stable C API
initially for the Xen paravirtualization but should be able to
integrate other virtualization mechanisms if needed.

%package devel
Summary:	Development tools for programs using libvirt
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_xen:Requires: xen-devel}

%description devel
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

This package contains the header files and libraries needed for
developing programs using the libvirt library.

%package static
Summary:	Development static libraries for programs using libvirt
Group:		Development/Libraries

%description static
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

This package contains the static libraries needed for developing
programs using the libvirt library.

%package -n	python-%{name}
Summary:	Python bindings to interact with virtualization capabilities
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n	python-%{name}
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

This package contains the Python bindings for the libvirt library.

%package utils
Summary:	Tools to interact with virtualization capabilities
Group:		Base/Kernel
Requires:	%{name} = %{version}-%{release}
Suggests:	iptables
Suggests:	bridge-utils
Suggests:	dmidecode
Suggests:	dnsmasq
Suggests:	ebtables
Suggests:	gawk
Suggests:	iptables
Suggests:	lvm2
# for management through ssh
Suggests:	netcat-openbsd
Suggests:	polkit

%description utils
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

This package contains tools for the libvirt library.

%prep
%setup -q
#%patch0 -p1
%patch1 -p1
# weird translations
rm -f po/{my,eu_ES}.{po,gmo}

mv po/vi_VN.po po/vi.po
mv po/vi_VN.gmo po/vi.gmo

%build
%{__libtoolize}
%{__aclocal} -I gnulib/m4 -I m4
%{__autoheader}
%{__autoconf}
%{__automake}


%configure \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir} \
	--with-html-subdir=%{name} \
	--x-libraries=%{_libdir} \
	%{!?with_xen:--without-xen} \
	%{!?with_qemu:--without-qemu} \
	%{!?with_netcf:--without-netcf} \
	--with-init-script=redhat \
	--with-storage-lvm \
	--without-hal \
	--with-udev \
	PVCREATE=/sbin/pvcreate \
	VGCREATE=/sbin/vgcreate \
	LVCREATE=/sbin/lvcreate \
	PVREMOVE=/sbin/pvremove \
	VGREMOVE=/sbin/vgremove \
	LVREMOVE=/sbin/lvremove \
	VGCHANGE=/sbin/vgchange \
	  VGSCAN=/sbin/vgscan   \
	     PVS=/sbin/pvs      \
	     VGS=/sbin/vgs      \
	     LVS=/sbin/lvs      \
	   BRCTL=/sbin/brctl    \
	SHOWMOUNT=/usr/sbin/showmount \
	IPTABLES_PATH=/usr/sbin/iptables \
	IP6TABLES_PATH=/usr/sbin/ip6tables \
	EBTABLES_PATH=/usr/sbin/ebtables \
	ISCSIADM=/sbin/iscsiadm

%{__make} AWK=gawk

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DEVHELP_DIR=%{_gtkdocdir}/%{name}/devhelp \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/sysconfig
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

#install qemud/libvirtd.sysconf $RPM_BUILD_ROOT/etc/sysconfig/libvirtd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/libvirtd

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog README TODO NEWS
%attr(755,root,root) %{_libdir}/%{name}*.so.*
%attr(755,root,root) %{_libdir}/libvirt_lxc
%attr(755,root,root) %{_libdir}/libvirt_iohelper
%{?with_polkit:%{_datadir}/polkit-1/actions/org.libvirt.unix.policy}
%dir %{_datadir}/libvirt
%dir %{_datadir}/libvirt/schemas
%{_datadir}/libvirt/schemas/capability.rng
%{_datadir}/libvirt/schemas/domain.rng
%{_datadir}/libvirt/schemas/domainsnapshot.rng
%{_datadir}/libvirt/schemas/interface.rng
%{_datadir}/libvirt/schemas/network.rng
%{_datadir}/libvirt/schemas/nodedev.rng
%{_datadir}/libvirt/schemas/nwfilter.rng
%{_datadir}/libvirt/schemas/secret.rng
%{_datadir}/libvirt/schemas/storageencryption.rng
%{_datadir}/libvirt/schemas/storagepool.rng
%{_datadir}/libvirt/schemas/storagevol.rng

%files devel
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}
%doc %{_gtkdocdir}/%{name}
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}*.so
%{_libdir}/%{name}*.la
%{_pkgconfigdir}/%{name}.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/%{name}.a
%{_libdir}/%{name}-qemu.a

%files -n python-%{name}
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-python-%{version}
%{py_sitedir}/libvirt.py
%{py_sitedir}/libvirtmod.la
%{py_sitedir}/libvirtmod.so

%files utils
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sasl/libvirt.conf
%attr(755,root,root) %{_bindir}/virsh
%attr(755,root,root) %{_sbindir}/libvirtd
%attr(754,root,root) /etc/rc.d/init.d/libvirtd
%attr(754,root,root) /etc/rc.d/init.d/libvirt-guests
%attr(755,root,root) %{_bindir}/virt-xml-validate
%attr(755,root,root) %{_bindir}/virt-pki-validate
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/libvirtd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/libvirt-guests
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.lxc
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.qemu
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.uml
%{_libdir}/libvirt_parthelper
%{_libdir}/virt-aa-helper
%{_mandir}/man1/virsh.1*
%{_mandir}/man1/virt-xml-validate.1*
%{_mandir}/man1/virt-pki-validate.1*
%{_mandir}/man8/libvirtd.8*
%{_datadir}/%{name}/*.xml
%{_datadir}/augeas/lenses/*.aug
%{_datadir}/augeas/lenses/tests/*.aug
%dir /var/run/libvirt
%dir /var/lib/libvirt
