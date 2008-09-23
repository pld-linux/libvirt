#
# Conditional build:
%bcond_with	xen		# xen
%bcond_without	xen_proxy		# Xen proxy
%bcond_without	qemu		# Qemu
%bcond_with	polkit		# PolicyKit
%bcond_with	lokkit		# Lokkit

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
Version:	0.4.5
Release:	0.1
License:	LGPL
Group:		Base/Kernel
URL:		http://www.libvirt.org/
Source0:	ftp://ftp.libvirt.org/libvirt/%{name}-%{version}.tar.gz
# Source0-md5:	dcb590a6202c332907eae7b44e47ca4b
%{?with_lokkit:BuildRequires: /usr/sbin/lokkit}
%{?with_polkit:BuildRequires:	PolicyKit-devel >= 0.6}
BuildRequires:	avahi-devel
BuildRequires:	bridge-utils
BuildRequires:	cyrus-sasl-devel
BuildRequires:	dnsmasq
BuildRequires:	gawk
BuildRequires:	gettext
BuildRequires:	gnutls-devel
BuildRequires:	libselinux-devel
BuildRequires:	libxml2-devel
BuildRequires:	ncurses-devel
BuildRequires:	nfs-utils
BuildRequires:	python-devel
BuildRequires:	readline-devel
# For mount/umount in FS driver
BuildRequires:	util-linux
%{?with_xen:BuildRequires:	xen-devel >= 3.0.4}
# For LVM drivers
BuildRequires:	lvm2
BuildRequires:	ncurses-devel
# For ISCSI driver
BuildRequires:	open-iscsi
# For disk driver
BuildRequires:	parted-devel
BuildRequires:	python
BuildRequires:	python-devel
%{?with_qemu:BuildRequires: qemu}
BuildRequires:	readline-devel
%if %{with qemu}
BuildRequires:	/usr/bin/qemu-img
# From QEMU RPMs
%else
%if %{with xen}
BuildRequires:	/usr/sbin/qcow-create
# From Xen RPMs
%endif
%endif
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

%description utils
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

This package contains tools for the libvirt library.

%prep
%setup -q

%build
CPPFLAGS=-std=c99
./configure \
        --host=x86_64-pld-linux \
        --build=x86_64-pld-linux \
        --prefix=/usr \
        --exec-prefix=/usr \
        --bindir=/usr/bin \
        --sbindir=/usr/sbin \
        --sysconfdir=/etc \
        --datadir=/usr/share \
        --includedir=/usr/include \
        --libdir=/usr/lib64 \
        --libexecdir=/usr/lib64 \
        --localstatedir=/var \
        --sharedstatedir=/var/lib \
        --mandir=/usr/share/man \
        --infodir=/usr/share/info \
        --x-libraries=/usr/lib64 \
	%{!?with_xen:--without-xen} \
	%{!?with_qemu:--without-qemu} \
	--with-init-script=redhat \
	--with-qemud-pid-file=%{_localstatedir}/run/libvirt_qemud.pid \
	--with-remote-file=%{_localstatedir}/run/libvirtd.pid

%{__make} AWK=gawk

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog README TODO NEWS
%attr(755,root,root) %{_libdir}/%{name}.so.*
#%{_libdir}/%{name}_proxy
%dir %{_datadir}/augeas
%dir %{_datadir}/augeas/lenses
%{_datadir}/augeas/lenses/*.aug
%dir %{_datadir}/augeas/lenses/tests
%{_datadir}/augeas/lenses/tests/*.aug
%{_datadir}/PolicyKit/policy/org.libvirt.unix.policy
%attr(755,root,root) %{_libdir}/libvirt_lxc

%files devel
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}
%doc %{_datadir}/gtk-doc/html/%{name}
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}.so
%{_libdir}/%{name}.la
%{_pkgconfigdir}/%{name}.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/%{name}.a

%files -n python-%{name}
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-python-%{version}
%{py_sitedir}/libvirt.py
%{py_sitedir}/libvirtmod.a
%{py_sitedir}/libvirtmod.la
%{py_sitedir}/libvirtmod.so

%files utils
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt
%config(noreplace) %verify(not md5 mtime size) /etc/sasl2/libvirt.conf
%attr(755,root,root) %{_bindir}/virsh
%attr(755,root,root) %{_sbindir}/libvirtd
#%attr(755,root,root) %{_sbindir}/libvirt_qemud
#/etc/rc.d/init.d/libvirtd
%{_libdir}/libvirt_parthelper
%{_mandir}/man1/virsh.1*
