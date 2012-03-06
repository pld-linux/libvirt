#
# Conditional build:
%bcond_without	xen		# xen
%bcond_without	xen_proxy	# Xen proxy
%bcond_without	qemu		# Qemu
%bcond_without	polkit		# PolicyKit
%bcond_with	sanlock		# sanlock storage lock manager
%bcond_with	netcf		# host interfaces support
%bcond_without	uml		# UML support
%bcond_without	openvz		# OpenVZ support
%bcond_without	phyp		# PHYP support
%bcond_without	xenapi		# XenAPI support
%bcond_without	libxl		# libxenlight
%bcond_without	esx		# ESX support
%bcond_without	hyperv		# Hyper-V support

# qemu available only on x86 and ppc
%ifnarch %{ix86} %{x8664} ppc
%undefine	with_qemu
%endif
# Xen is available only on x86 and ia64
%ifnarch %{ix86} %{x8664} ia64
%undefine	with_xen
%endif
%if %{without xen}
%undefine	with_xen_proxy
%endif

Summary:	Toolkit to interact with virtualization capabilities
Summary(pl.UTF-8):	Narzędzia współpracujące z funkcjami wirtualizacji
Name:		libvirt
Version:	0.9.10
Release:	5
License:	LGPL v2.1+
Group:		Base/Kernel
Source0:	ftp://ftp.libvirt.org/libvirt/%{name}-%{version}.tar.gz
# Source0-md5:	a424bb793521e637349da47e93dd5fff
Source1:	%{name}.init
Source2:	%{name}.tmpfiles
Patch0:		%{name}-sasl.patch
Patch1:		%{name}-lxc.patch
Patch2:		libvirt-qemu-acl.patch
Patch3:		libvirt-xend.patch
URL:		http://www.libvirt.org/
BuildRequires:	audit-libs-devel
BuildRequires:	augeas-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	avahi-devel >= 0.6.0
BuildRequires:	curl-devel >= 7.18.0
BuildRequires:	cyrus-sasl-devel
BuildRequires:	device-mapper-devel >= 1.0.0
BuildRequires:	gawk
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	gnutls-devel >= 1.0.25
BuildRequires:	libapparmor-devel
BuildRequires:	libblkid-devel >= 2.17
BuildRequires:	libcap-ng-devel >= 0.4.0
BuildRequires:	libgcrypt-devel
BuildRequires:	libnl1-devel >= 1.1
BuildRequires:	libpcap-devel >= 1.0.0
BuildRequires:	libselinux-devel >= 2.0.82
BuildRequires:	libssh2-devel >= 1.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	libxslt-devel
BuildRequires:	openldap-devel
BuildRequires:	openwsman-devel >= 2.2.3
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
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.627
%{?with_sanlock:BuildRequires:	sanlock-devel >= 0.8}
BuildRequires:	udev-devel >= 145
%{?with_xen:BuildRequires:	xen-devel >= 4.1.2}
# For disk driver
BuildRequires:	xorg-lib-libpciaccess-devel >= 0.10.0
BuildRequires:	yajl-devel
Requires:	curl-libs >= 7.18.0
Requires:	device-mapper >= 1.0.0
Requires:	gnutls >= 1.0.25
Requires:	libcap-ng >= 0.4.0
Requires:	libnl1 >= 1.1
Requires:	libpcap >= 1.0.0
Requires:	libselinux >= 2.0.82
Requires:	libssh2 >= 1.0
Requires:	libxml2 >= 1:2.6.0
Requires:	openwsman-libs >= 2.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

Virtualization of the Linux Operating System means the ability to run
multiple instances of Operating Systems concurently on a single
hardware system where the basic resources are driven by a Linux
instance. The library aim at providing long term stable C API
initially for the Xen paravirtualization but should be able to
integrate other virtualization mechanisms if needed.

%description -l pl.UTF-8
Libvirt to zestaw narzędzi w C do współpracy z funkcjami
wirtualizacji obecnych wersji Linuksa.

Wirtualizacja w systemie operacyjnym Linux oznacza możliwość
jednoczesnego uruchamiania wielu instancji systemu operacyjnego na
pojedynczym systemie sprzętowym, którego podstawowe zasoby są
zarządzane przez instancję Linuksa. Celem biblioteki jest zapewnienie
długotrwale stabilnego API C, początkowo do parawirtualizacji Xen, ale
dającej się zintegrować w razie potrzeby z innymi mechanizmami
wirtualizacji.

%package devel
Summary:	Development files for programs using libvirt
Summary(pl.UTF-8):	Pliki programistyczne do programów wykorzystujących libvirt
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	audit-libs-devel
Requires:	curl-devel >= 7.18.0
Requires:	device-mapper-devel >= 1.0.0
Requires:	gnutls-devel >= 1.0.25
Requires:	libapparmor-devel
Requires:	libcap-ng-devel >= 0.4.0
Requires:	libgcrypt-devel
Requires:	libnl1-devel >= 1.1
Requires:	libpcap-devel >= 1.0.0
Requires:	libselinux-devel >= 2.0.82
Requires:	libxml2-devel >= 1:2.6.0
Requires:	numactl-devel
Requires:	openwsman-devel >= 2.2.3
%{?with_xen:Requires: xen-devel}
Requires:	yajl-devel

%description devel
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

This package contains the header files needed for developing programs
using the libvirt library.

%description devel -l pl.UTF-8
Libvirt to zestaw narzędzi w C do współpracy z funkcjami
wirtualizacji obecnych wersji Linuksa.

Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
wykorzystujących bibliotekę libvirt.

%package static
Summary:	Development static libraries for programs using libvirt
Summary(pl.UTF-8):	Statyczne biblioteki programistyczne do programów wykorzystujących libvirt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

This package contains the static libraries for developing programs
using the libvirt library.

%description static -l pl.UTF-8
Libvirt to zestaw narzędzi w C do współpracy z funkcjami
wirtualizacji obecnych wersji Linuksa.

Ten pakiet zawiera biblioteki statyczne do tworzenia programów
wykorzystujących bibliotekę libvirt.

%package -n python-%{name}
Summary:	Python bindings to interact with virtualization capabilities
Summary(pl.UTF-8):	Wiązania Pythona do współpracy z funkcjami wirtualizacji
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n	python-%{name}
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

This package contains the Python bindings for the libvirt library.

%description -n	python-%{name} -l pl.UTF-8
Libvirt to zestaw narzędzi w C do współpracy z funkcjami
wirtualizacji obecnych wersji Linuksa.

Ten pakiet zawiera wiązania Pythona do biblioteki libvirt.

%package utils
Summary:	Tools to interact with virtualization capabilities
Summary(pl.UTF-8):	Narzędzia do współpracy z funkcjami wirtualizacyjnymi
Group:		Base/Kernel
Requires:	%{name} = %{version}-%{release}
Requires:	avahi-libs >= 0.6.0
# /etc/init.d/libvirt-guests[37]: .: /usr/bin/gettext.sh: not found, some better split needed
Requires:	gettext-devel
Requires:	libblkid >= 2.17
Requires:	parted-libs >= 1.8.0
Requires:	systemd-units >= 37-0.10
Requires:	udev-libs >= 145
Requires:	xorg-lib-libpciaccess >= 0.10.0
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
Suggests:	polkit >= 0.90
Suggests:	scrub

%description utils
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

This package contains tools for the libvirt library.

%description utils -l pl.UTF-8
Libvirt to zestaw narzędzi w C do współpracy z funkcjami
wirtualizacji obecnych wersji Linuksa.

Ten pakiet zawiera narzędzia do biblioteki libvirt.

%package lock-sanlock
Summary:	Sanlock lock manager plugin for libvirt
Summary(pl.UTF-8):	Zarządca blokad sanlock dla biblioteki libvirt
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description lock-sanlock
Sanlock lock manager plugin for libvirt.

%description lock-sanlock -l pl.UTF-8
Zarządca blokad sanlock dla biblioteki libvirt.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# weird translations
%{__rm} po/{my,eu_ES}.{po,gmo}

mv po/vi_VN.po po/vi.po
mv po/vi_VN.gmo po/vi.gmo

%build
%{__libtoolize}
%{__aclocal} -I gnulib/m4 -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	PVCREATE=/sbin/pvcreate \
	VGCREATE=/sbin/vgcreate \
	LVCREATE=/sbin/lvcreate \
	PVREMOVE=/sbin/pvremove \
	VGREMOVE=/sbin/vgremove \
	LVREMOVE=/sbin/lvremove \
	VGCHANGE=/sbin/vgchange \
	LVCHANGE=/sbin/lvchange \
	  VGSCAN=/sbin/vgscan   \
	     PVS=/sbin/pvs      \
	     VGS=/sbin/vgs      \
	     LVS=/sbin/lvs      \
	      TC=/sbin/tc \
	   BRCTL=/sbin/brctl    \
	ISCSIADM=/sbin/iscsiadm	\
	SHOWMOUNT=/usr/sbin/showmount \
	MOUNT=/bin/mount \
	UMOUNT=/bin/umount \
	MKFS=/sbin/mkfs \
	SHOWMOUNT=/usr/sbin/showmount \
	IPTABLES_PATH=/usr/sbin/iptables \
	IP6TABLES_PATH=/usr/sbin/ip6tables \
	EBTABLES_PATH=/usr/sbin/ebtables \
	ISCSIADM=/sbin/iscsiadm \
	DNSMASQ=/usr/sbin/dnsmasq \
	RADVD=/usr/sbin/radvd \
	UDEVADM=/sbin/udevadm \
	MODPROBE=/sbin/modprobe \
	SCRUB=/usr/bin/scrub \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir} \
	--with-html-subdir=%{name} \
	--with-init-script=redhat \
	--with-storage-lvm \
	--with-storage-fs \
	--with-storage-iscsi \
	--with-storage-scsi \
	--with-storage-mpath \
	--with-storage-disk \
	--with-macvtap \
	--with-virtualport \
	--with-scrub \
	--with-udev \
	--without-hal \
	--with-lxc \
	--with-vbox=%{_libdir}/VirtualBox \
	%{!?with_netcf:--without-netcf} \
	%{!?with_sanlock:--without-sanlock} \
	%{!?with_qemu:--without-qemu} \
	%{!?with_xen:--without-xen} \
	%{!?with_uml:--without-uml} \
	%{!?with_openvz:--without-openvz} \
	%{!?with_phyp:--without-phyp} \
	%{!?with_xenapi:--without-xenapi} \
	%{!?with_libxl:--without-libxl} \
	%{!?with_esx:--without-esx} \
	%{!?with_hyperv:--without-hyperv} \
	--x-libraries=%{_libdir} \
	--with-init-script=systemd

%{__make} \
	AWK=gawk

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

%{__make} install \
	DEVHELP_DIR=%{_gtkdocdir}/%{name}/devhelp \
	DESTDIR=$RPM_BUILD_ROOT

#install qemud/libvirtd.sysconf $RPM_BUILD_ROOT/etc/sysconfig/libvirtd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/libvirtd
install %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la

%if %{with sanlock}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvirt/lock-driver/*.{a,la}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post utils
%systemd_post libvirtd.service
NORESTART=1
%systemd_post libvirt-guests.service

%preun utils
%systemd_preun libvirtd.service
%systemd_preun libvirt-guests.service

%postun utils
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog README TODO NEWS
%attr(755,root,root) %{_libdir}/libvirt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvirt.so.0
%attr(755,root,root) %{_libdir}/libvirt-qemu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvirt-qemu.so.0
%attr(755,root,root) %{_libdir}/libvirt_lxc
%attr(755,root,root) %{_libdir}/libvirt_iohelper
%attr(755,root,root) %{_libdir}/virt-aa-helper
%dir %{_libdir}/libvirt
%if %{with sanlock}
%dir %{_libdir}/libvirt/lock-driver
%endif
%dir %{_datadir}/libvirt
%dir %{_datadir}/libvirt/schemas
%{_datadir}/libvirt/schemas/basictypes.rng
%{_datadir}/libvirt/schemas/capability.rng
%{_datadir}/libvirt/schemas/domain.rng
%{_datadir}/libvirt/schemas/domaincommon.rng
%{_datadir}/libvirt/schemas/domainsnapshot.rng
%{_datadir}/libvirt/schemas/interface.rng
%{_datadir}/libvirt/schemas/network.rng
%{_datadir}/libvirt/schemas/networkcommon.rng
%{_datadir}/libvirt/schemas/nodedev.rng
%{_datadir}/libvirt/schemas/nwfilter.rng
%{_datadir}/libvirt/schemas/secret.rng
%{_datadir}/libvirt/schemas/storageencryption.rng
%{_datadir}/libvirt/schemas/storagepool.rng
%{_datadir}/libvirt/schemas/storagevol.rng

%if %{with sanlock}
%files lock-sanlock
%attr(755,root,root) %{_sbindir}/virt-sanlock-cleanup
%attr(755,root,root) %{_libdir}/libvirt/lock-driver/sanlock.so
%dir /var/lib/libvirt/sanlock
%{_mandir}/man8/virt-sanlock-cleanup.8*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvirt.so
%attr(755,root,root) %{_libdir}/libvirt-qemu.so
%{_libdir}/libvirt.la
%{_libdir}/libvirt-qemu.la
%{_gtkdocdir}/%{name}
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvirt.a
%{_libdir}/libvirt-qemu.a

%files -n python-%{name}
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-python-%{version}
%attr(755,root,root) %{py_sitedir}/libvirtmod.so
%attr(755,root,root) %{py_sitedir}/libvirtmod_qemu.so
%{py_sitedir}/libvirt.py[co]
%{py_sitedir}/libvirt_qemu.py[co]

%files utils
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sasl/libvirt.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/libvirtd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/libvirt-guests
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.lxc
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.qemu
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.uml
%attr(754,root,root) /etc/rc.d/init.d/libvirtd
%attr(754,root,root) /etc/rc.d/init.d/libvirt-guests
%{systemdunitdir}/libvirtd.service
%{systemdunitdir}/libvirt-guests.service
%config(noreplace) %verify(not md5 mtime size) /etc/sysctl.d/libvirtd
%attr(755,root,root) %{_sbindir}/libvirtd
%attr(755,root,root) %{_bindir}/virsh
%attr(755,root,root) %{_bindir}/virt-host-validate
%attr(755,root,root) %{_bindir}/virt-xml-validate
%attr(755,root,root) %{_bindir}/virt-pki-validate
%attr(755,root,root) %{_libdir}/libvirt_parthelper
%{?with_polkit:%{_datadir}/polkit-1/actions/org.libvirt.unix.policy}
%{_mandir}/man1/virsh.1*
%{_mandir}/man1/virt-host-validate.1*
%{_mandir}/man1/virt-xml-validate.1*
%{_mandir}/man1/virt-pki-validate.1*
%{_mandir}/man8/libvirtd.8*
%{_datadir}/%{name}/*.xml
%{_datadir}/augeas/lenses/*.aug
%{_datadir}/augeas/lenses/tests/*.aug
/usr/lib/tmpfiles.d/%{name}.conf
%attr(711,root,root) %dir /var/cache/libvirt
%dir /var/lib/libvirt
%attr(711,root,root) %dir /var/lib/libvirt/boot
%dir /var/lib/libvirt/dnsmasq
%attr(711,root,root) %dir /var/lib/libvirt/images
%attr(700,root,root) %dir /var/lib/libvirt/lxc
%attr(700,root,root) %dir /var/lib/libvirt/network
%attr(700,root,root) %dir /var/lib/libvirt/uml
%dir /var/log/libvirt
%attr(700,root,root) %dir /var/log/libvirt/lxc
%attr(700,root,root) %dir /var/log/libvirt/uml
%dir /var/run/libvirt
%attr(700,root,root) %dir /var/run/libvirt/lxc
%if %{with qemu}
# %attr(750,qemu,qemu) ?
%dir /var/cache/libvirt/qemu
# %attr(750,qemu,qemu) ?
%dir /var/lib/libvirt/qemu
%attr(700,root,root) %dir /var/log/libvirt/qemu
%attr(700,root,root) %dir /var/run/libvirt/qemu
%endif
