# TODO:
# - parallels-sdk >= 7.0.22?
# - virtuozzo storage?
# - pldize virtlockd.init
# - update vserver patch, if anybody needs it
#
# Conditional build:
# - virtualization
%bcond_without	esx		# VMware ESX support
%bcond_without	hyperv		# Hyper-V support
%bcond_without	libxl		# libxenlight support
%bcond_without	lxc		# LXC support
%bcond_without	openvz		# OpenVZ support
%bcond_without	phyp		# PHYP support
%bcond_without	qemu		# Qemu support
%bcond_without	uml		# UML support
%bcond_without	vbox		# VirtualBox support
%bcond_without	vmware		# VMware Workstation/Player support
%bcond_with	vserver		# Support for Linux-VServer guests
%bcond_without	xenapi		# Xen API (Citrix XenServer) support
%bcond_without	xen		# Xen support
# - storage
%bcond_without	ceph		# RADOS BD (Ceph) storage support
%bcond_without	glusterfs	# GlusterFS storage support
# - storage locking
%bcond_without	sanlock		# sanlock storage lock manager
# - other
%bcond_without	netcf		# host interfaces support
%bcond_without	polkit		# PolicyKit support
%bcond_without	systemtap	# systemtap/dtrace probes
%bcond_without	wireshark	# wireshark dissector module
%bcond_without	static_libs	# static libraries build

# qemu available only on x86 and ppc
%ifnarch %{ix86} %{x8664} ppc
%undefine	with_qemu
%endif

# Xen is available only on x86 and ia64
%ifnarch %{ix86} %{x8664} ia64
%undefine	with_xen
%undefine	with_xenapi
%undefine	with_libxl
%endif

Summary:	Toolkit to interact with virtualization capabilities
Summary(pl.UTF-8):	Narzędzia współpracujące z funkcjami wirtualizacji
Name:		libvirt
Version:	4.1.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://libvirt.org/sources/libvirt-%{version}.tar.xz
# Source0-md5:	30b95c458da4f8c3d073a82755815997
Source1:	%{name}.init
Source2:	%{name}.tmpfiles
Patch0:		%{name}-sasl.patch
Patch2:		%{name}-qemu-acl.patch
Patch3:		virtlockd.init.patch
Patch4:		%{name}-udevadm-settle.patch
Patch5:		vserver.patch
Patch6:		bashisms.patch
Patch7:		%{name}-guests.init.patch
Patch8:		%{name}-link.patch
URL:		http://www.libvirt.org/
BuildRequires:	acl-devel
BuildRequires:	attr-devel
BuildRequires:	audit-libs-devel
BuildRequires:	augeas-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	avahi-devel >= 0.6.0
%{?with_ceph:BuildRequires:	ceph-devel}
BuildRequires:	curl-devel >= 7.18.0
BuildRequires:	cyrus-sasl-devel
BuildRequires:	dbus-devel >= 1.0.0
BuildRequires:	device-mapper-devel >= 1.0.0
BuildRequires:	gawk
BuildRequires:	gcc >= 6:4.4
BuildRequires:	gettext-tools >= 0.17
%{?with_glusterfs:BuildRequires:	glusterfs-devel >= 3.4.1}
BuildRequires:	gnutls-devel >= 2.2.0
BuildRequires:	libapparmor-devel
BuildRequires:	libblkid-devel >= 2.17
BuildRequires:	libcap-ng-devel >= 0.4.0
BuildRequires:	libfuse-devel >= 2.8.6
BuildRequires:	libgcrypt-devel
BuildRequires:	libnl-devel >= 3.2
BuildRequires:	libpcap-devel >= 1.0.0
BuildRequires:	libselinux-devel >= 2.5
BuildRequires:	libssh-devel >= 0.7
BuildRequires:	libssh2-devel >= 1.3
BuildRequires:	libtool
%{?with_xenapi:BuildRequires:	libxenserver-devel}
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	libxslt-devel
BuildRequires:	ncurses-devel
%{?with_netcf:BuildRequires:	netcf-devel >= 0.2.0}
BuildRequires:	numactl-devel
%{?with_hyperv:BuildRequires:	openwsman-devel >= 2.2.3}
BuildRequires:	parted-devel >= 1.8.0
BuildRequires:	pkgconfig
%{?with_polkit:BuildRequires:	polkit}
%{?with_polkit:BuildRequires:	polkit-devel >= 0.90}
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.627
%{?with_sanlock:BuildRequires:	sanlock-devel >= 0.8}
BuildRequires:	systemd-devel
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	udev-devel >= 1:218
%{?with_wireshark:BuildRequires:	wireshark-devel >= 1.11.3}
%{?with_xen:BuildRequires:	xen-devel >= 4.2}
%{?with_libxl:BuildRequires:	xen-devel >= 4.4}
# For disk driver
BuildRequires:	xorg-lib-libpciaccess-devel >= 0.10.0
BuildRequires:	yajl-devel
Requires:	curl-libs >= 7.18.0
Requires:	device-mapper >= 1.0.0
Requires:	libcap-ng >= 0.4.0
Requires:	libnl >= 3.2
Requires:	libpcap >= 1.0.0
Requires:	libselinux >= 2.5
Requires:	libssh >= 0.7
Requires:	libssh2 >= 1.3
Requires:	libxml2 >= 1:2.6.0
%{?with_hyperv:Requires:	openwsman-libs >= 2.2.3}
Obsoletes:	libvirt-daemon-esx
Obsoletes:	libvirt-daemon-hyperv
Obsoletes:	libvirt-daemon-openvz
Obsoletes:	libvirt-daemon-phyp
Obsoletes:	libvirt-daemon-vbox
Obsoletes:	libvirt-daemon-vmware
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

This package contains the base libraries and configuration file.

%description -l pl.UTF-8
Libvirt to zestaw narzędzi w C do współpracy z funkcjami wirtualizacji
obecnych wersji Linuksa.

Wirtualizacja w systemie operacyjnym Linux oznacza możliwość
jednoczesnego uruchamiania wielu instancji systemu operacyjnego na
pojedynczym systemie sprzętowym, którego podstawowe zasoby są
zarządzane przez instancję Linuksa. Celem biblioteki jest zapewnienie
długotrwale stabilnego API C, początkowo do parawirtualizacji Xen, ale
dającej się zintegrować w razie potrzeby z innymi mechanizmami
wirtualizacji.

Ten pakiet zawiera podstawowe biblioteki oraz plik konfiguracyjny.

%package -n bash-completion-%{name}
Summary:        bash-completion for libvirt
Group:          Applications/Shells
Requires:       bash-completion
%if "%{_rpmversion}" >= "5"
BuildArch:      noarch
%endif

%description -n bash-completion-%{name}
This package provides bash-completion for libvirt.

%package devel
Summary:	Development files for programs using libvirt
Summary(pl.UTF-8):	Pliki programistyczne do programów wykorzystujących libvirt
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	audit-libs-devel
Requires:	curl-devel >= 7.18.0
Requires:	dbus-devel >= 1.0.0
Requires:	device-mapper-devel >= 1.0.0
Requires:	gnutls-devel >= 2.2.0
Requires:	libapparmor-devel
Requires:	libcap-ng-devel >= 0.4.0
Requires:	libgcrypt-devel
Requires:	libnl-devel >= 3.2
Requires:	libpcap-devel >= 1.0.0
Requires:	libselinux-devel >= 2.5
Requires:	libxml2-devel >= 1:2.6.0
Requires:	numactl-devel
%{?with_hyperv:Requires:	openwsman-devel >= 2.2.3}
%{?with_xen:Requires:	xen-devel >= 4.2}
Requires:	yajl-devel

%description devel
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

This package contains the header files needed for developing programs
using the libvirt library.

%description devel -l pl.UTF-8
Libvirt to zestaw narzędzi w C do współpracy z funkcjami wirtualizacji
obecnych wersji Linuksa.

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
Libvirt to zestaw narzędzi w C do współpracy z funkcjami wirtualizacji
obecnych wersji Linuksa.

Ten pakiet zawiera biblioteki statyczne do tworzenia programów
wykorzystujących bibliotekę libvirt.

%package lock-sanlock
Summary:	Sanlock lock manager plugin for libvirt
Summary(pl.UTF-8):	Zarządca blokad sanlock dla biblioteki libvirt
Group:		Libraries
Requires:	%{name}-daemon = %{version}-%{release}

%description lock-sanlock
Sanlock lock manager plugin for libvirt.

%description lock-sanlock -l pl.UTF-8
Zarządca blokad sanlock dla biblioteki libvirt.

%package daemon
Summary:	Server side daemon and supporting files for libvirt library
Summary(pl.UTF-8):	Demon działający po stronie serwera oraz pliki wspierające dla biblioteki libvirt
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	avahi-libs >= 0.6.0
Requires:	iproute2
Requires:	libblkid >= 2.17
%{?with_netcf:Requires:	netcf >= 0.2.0}
Requires:	parted-libs >= 1.8.0
Requires:	rc-scripts
# Needed for probing the power management features of the host.
Requires:	pm-utils
Requires:	systemd-units >= 37-0.10
Requires:	udev-libs >= 1:218
Requires:	util-linux
Requires:	virtual(module-tools)
Requires:	xorg-lib-libpciaccess >= 0.10.0
Requires(post):	systemd-units
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	systemd-units
Requires(preun):	systemd-units
Suggests:	bridge-utils
Suggests:	cyrus-sasl
Suggests:	cyrus-sasl-digest-md5
Suggests:	dmidecode
Suggests:	dnsmasq >= 2.41
Suggests:	ebtables
Suggests:	gawk
Suggests:	glusterfs-client >= 2.0.1
Suggests:	iptables
Suggests:	iptables
Suggests:	libcgroup
Suggests:	lvm2
Suggests:	numad
Suggests:	open-iscsi
Suggests:	parted >= 1.8.0
Suggests:	polkit >= 0.93
#Suggests:	radvd
Suggests:	scrub
#Suggests:	sheepdog
Provides:	libvirt(hypervisor)

%description daemon
Server side daemon required to manage the virtualization capabilities
of recent versions of Linux. Requires a hypervisor specific sub-RPM
for specific drivers.

%description daemon -l pl.UTF-8
Demon działający po stronie serwera wymagany do zarządzania funkcjami
wirtualizacji nowych wersji Linuksa. Wymaga podpakietu specyficznego
dla hipernadzorcy.

%package daemon-storage-gluster
Summary:	Storage driver plugin for GlusterFS
Summary(pl.UTF-8):	Wtyczka składowania danych wykorzystująca GlusterFS
Group:		Libraries
Requires:	%{name}-daemon = %{version}-%{release}
Requires:	glusterfs-libs >= 3.4.1

%description daemon-storage-gluster
Storage driver plugin for GlusterFS.

%description daemon-storage-gluster -l pl.UTF-8
Wtyczka składowania danych wykorzystująca system plików GlusterFS.

%package daemon-storage-rbd
Summary:	Storage driver plugin for Ceph RADOS Block Device
Summary(pl.UTF-8):	Wtyczka składowania danych wykorzystująca urządzenie blokowe RADOS (Ceph)
Group:		Libraries
Requires:	%{name}-daemon = %{version}-%{release}

%description daemon-storage-rbd
Storage driver plugin for Ceph RADOS Block Device.

%description daemon-storage-rbd -l pl.UTF-8
Wtyczka składowania danych wykorzystująca urządzenie blokowe RADOS
(system plików Ceph).

%package daemon-libxl
Summary:	Server side driver required to run XEN guests (xenlight)
Summary(pl.UTF-8):	Sterownik wymagany po stronie serwera do uruchamiania gości XEN (xenlight)
Group:		Libraries
Requires:	%{name}-daemon = %{version}-%{release}
Requires:	/usr/sbin/qcow-create
Requires:	xen >= 4.4
Provides:	libvirt(hypervisor)

%description daemon-libxl
Server side driver required to manage the virtualization capabilities
of XEN via xenlight interface.

%description daemon-libxl -l pl.UTF-8
Sterownik wymagany po stronie serwera do zarządzania funkcjami
wirtualizacji XEN poprzez interfejs xenlight.

%package daemon-lxc
Summary:	Server side driver required to run LXC guests
Summary(pl.UTF-8):	Sterownik wymagany po stronie serwera do uruchamiania gości LXC
Group:		Libraries
Requires:	%{name}-daemon = %{version}-%{release}
Requires:	libfuse >= 2.8.6
Provides:	libvirt(hypervisor)

%description daemon-lxc
Server side driver required to manage the virtualization capabilities
of LXC.

%description daemon-lxc -l pl.UTF-8
Sterownik wymagany po stronie serwera do zarządzania funkcjami
wirtualizacji LXC.

%package daemon-qemu
Summary:	Server side driver required to run QEMU guests
Summary(pl.UTF-8):	Sterownik wymagany po stronie serwera do uruchamiania gości QEMU
Group:		Libraries
Requires:	%{name}-daemon = %{version}-%{release}
Requires:	/usr/bin/qemu-img
Requires:	bzip2
Requires:	gzip
Requires:	lzop
Requires:	qemu-system-x86
Requires:	xz
Provides:	libvirt(hypervisor)

%description daemon-qemu
Server side driver required to manage the virtualization capabilities
of the QEMU emulators.

%description daemon-qemu -l pl.UTF-8
Sterownik wymagany po stronie serwera do zarządzania funkcjami
wirtualizacji emulatora QEMU.

%package daemon-uml
Summary:	Server side driver required to run UML guests
Summary(pl.UTF-8):	Sterownik wymagany po stronie serwera do uruchamiania gości UML
Group:		Libraries
Requires:	%{name}-daemon = %{version}-%{release}
Provides:	libvirt(hypervisor)

%description daemon-uml
Server side driver required to manage the virtualization capabilities
of UML.

%description daemon-uml -l pl.UTF-8
Sterownik wymagany po stronie serwera do zarządzania funkcjami
wirtualizacji UML.

%package daemon-xen
Summary:	Server side driver required to run XEN guests
Summary(pl.UTF-8):	Sterownik wymagany po stronie serwera do uruchamiania gości XEN
Group:		Libraries
Requires:	%{name}-daemon = %{version}-%{release}
Requires:	/usr/sbin/qcow-create
Requires:	xen
Provides:	libvirt(hypervisor)

%description daemon-xen
Server side driver required to manage the virtualization capabilities
of XEN.

%description daemon-xen -l pl.UTF-8
Sterownik wymagany po stronie serwera do zarządzania funkcjami
wirtualizacji XEN.

%package client
Summary:	Client side utilities of the libvirt library
Summary(pl.UTF-8):	Narzędzia klienckie do biblioteki libvirt
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	gettext >= 0.18.1.1-6
Requires:	gnutls >= 2.2.0
Requires:	netcat-openbsd
Requires:	rc-scripts
Requires(post):	systemd-units
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	systemd-units
Requires(preun):	systemd-units

%description client
Client binaries needed to access to the virtualization capabilities of
recent versions of Linux (and other OSes).

%description client -l pl.UTF-8
Programy klienckie potrzebne do funkcji wirtualizacji nowych wersji
Linuksa (oraz innych systemów operacyjnych).

%package utils
Summary:	Tools to interact with virtualization capabilities (metapackage)
Summary(pl.UTF-8):	Narzędzia do współpracy z funkcjami wirtualizacyjnymi (metapakiet)
Group:		Applications/System
Requires:	%{name}-client = %{version}-%{release}
Requires:	%{name}-daemon = %{version}-%{release}
%{?with_libxl:Requires:	%{name}-daemon-libxl = %{version}-%{release}}
Requires:	%{name}-daemon-lxc = %{version}-%{release}
Requires:	%{name}-daemon-qemu = %{version}-%{release}
%{?with_uml:Requires:	%{name}-daemon-uml = %{version}-%{release}}
Requires:	%{name}-daemon-xen = %{version}-%{release}

%description utils
Libvirt is a C toolkit to interact with the virtualization
capabilities of recent versions of Linux.

This is metapackage gathering all tools for the libvirt library.

%description utils -l pl.UTF-8
Libvirt to zestaw narzędzi w C do współpracy z funkcjami wirtualizacji
obecnych wersji Linuksa.

To jest metapakiet zbierający wszystkie narzędzia przeznaczone dla
biblioteki libvirt.

%package -n systemtap-libvirt
Summary:	systemtap/dtrace probes for libvirt
Summary(pl.UTF-8):	Sondy systemtap/dtrace dla libvirt
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	systemtap-client

%description -n systemtap-libvirt
systemtap/dtrace probes for libvirt.

%description -n systemtap-libvirt -l pl.UTF-8
Sondy systemtap/dtrace dla libvirt.

%package -n wireshark-libvirt
Summary:	Wireshark dissector module for libvirt packets
Summary(pl.UTF-8):	Moduł sekcji Wiresharka do pakietów libvirt
Group:		Libraries
Requires:	wireshark >= 1.11.3

%description -n wireshark-libvirt
Wireshark dissector module for libvirt packets.

%description -n wireshark-libvirt -l pl.UTF-8
Moduł sekcji Wiresharka do pakietów libvirt.

%prep
%setup -q
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%{?with_vserver:%patch5 -p1}
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
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
	OVSVSCTL=/usr/bin/ovs-vsctl \
	NUMAD=/usr/bin/numad \
	SHEEPDOGCLI=/usr/sbin/collie \
	ZFS=/usr/sbin/zfs \
	ZPOOL=/usr/sbin/zpool \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-bash-completion \
	--with-bash-completions-dir=/etc/bash_completion.d \
	--with-html-dir=%{_gtkdocdir} \
	--with-html-subdir=%{name} \
	--with-init-script=systemd+redhat \
	--with-packager="PLD-Linux" \
	--with-packager-version="%{name}-%{version}-%{release}.%{_target_cpu}" \
	--with-qemu-user=qemu \
	--with-qemu-group=qemu \
	--with-storage-disk \
	--with-storage-fs \
	--with-storage-gluster%{!?with_glusterfs:=no} \
	--with-storage-iscsi \
	--with-storage-lvm \
	--with-storage-mpath \
	--with-storage-rbd%{!?with_ceph:=no} \
	--with-storage-scsi \
	--with-storage-sheepdog \
	--with-apparmor \
	--with-audit \
	--with-avahi \
	%{__with_without systemtap dtrace} \
	%{__with_without esx} \
	--with-driver-modules \
	--without-hal \
	%{__with_without hyperv} \
	--with-blkid \
	--with-ssh2 \
	%{__with_without libxl} \
	%{__with_without lxc} \
	--with-macvtap \
	%{__with_without netcf} \
	--with-numactl \
	--with-numad \
	%{__with_without openvz} \
	%{__with_without phyp} \
	%{__with_without polkit} \
	%{__with_without qemu} \
	%{__with_without sanlock} \
	--with-sasl \
	--with-selinux \
	--with-udev \
	%{__with_without uml} \
	%{__with_without vbox vbox %{_libdir}/VirtualBox} \
	--with-virtualport \
	%{__with_without vmware} \
	%{!?with_wireshark:--without-wireshark-dissector} \
	%{__with_without xen} \
	%{__with_without xenapi} \
	--with-yajl \
	--x-libraries=%{_libdir}

%{__make} \
	AWK=gawk

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} install \
	DEVHELP_DIR=%{_gtkdocdir}/%{name}/devhelp \
	SYSTEMD_UNIT_DIR=%{systemdunitdir} \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/libvirtd
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvirt/connection-driver/*.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/libvirt/connection-driver/*.a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvirt/storage-backend/*.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/libvirt/storage-backend/*.a}

%if %{with sanlock}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvirt/lock-driver/*.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/libvirt/lock-driver/*.a}
%endif
%if %{with wireshark}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/wireshark/plugins/*/libvirt.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/wireshark/plugins/*/libvirt.a} \
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post daemon
/sbin/chkconfig --add libvirtd
%service libvirtd restart
%systemd_post libvirtd.service

%preun daemon
if [ "$1" = "0" ]; then
	%service -q libvirtd stop
	/sbin/chkconfig --del libvirtd
fi
%systemd_preun libvirtd.service

%postun daemon
%systemd_reload

%post client
/sbin/chkconfig --add libvirt-guests
%service -n libvirt-guests restart
NORESTART=1
%systemd_post libvirt-guests.service

%preun client
%systemd_preun libvirt-guests.service
if [ "$1" = "0" ]; then
	%service -q libvirt-guests stop
	/sbin/chkconfig --del libvirt-guests
fi

%postun client
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%dir %{_sysconfdir}/libvirt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/libvirt.conf
%attr(755,root,root) %{_libdir}/libvirt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvirt.so.0
%attr(755,root,root) %{_libdir}/libvirt-admin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvirt-admin.so.0
%if %{with lxc}
%attr(755,root,root) %{_libdir}/libvirt-lxc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvirt-lxc.so.0
%endif
%attr(755,root,root) %{_libdir}/libvirt-qemu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvirt-qemu.so.0

# NSS modules
%attr(755,root,root) %{_libdir}/libnss_libvirt.so.2
%attr(755,root,root) %{_libdir}/libnss_libvirt_guest.so.2

%dir %{_libdir}/libvirt
%dir %{_datadir}/libvirt

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/virsh
/etc/bash_completion.d/virt-admin
/etc/bash_completion.d/vsh

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvirt.so
%attr(755,root,root) %{_libdir}/libvirt-admin.so
%{?with_lxc:%attr(755,root,root) %{_libdir}/libvirt-lxc.so}
%attr(755,root,root) %{_libdir}/libvirt-qemu.so
%{_datadir}/%{name}/api
%{_gtkdocdir}/%{name}
%{_includedir}/%{name}
%{_pkgconfigdir}/libvirt.pc
%{_pkgconfigdir}/libvirt-admin.pc
%{?with_lxc:%{_pkgconfigdir}/libvirt-lxc.pc}
%{_pkgconfigdir}/libvirt-qemu.pc
%{_mandir}/man7/virkeycode-*.7*
%{_mandir}/man7/virkeyname-*.7*

%files static
%defattr(644,root,root,755)
%{_libdir}/libvirt.a
%{_libdir}/libvirt-admin.a
%{?with_lxc:%{_libdir}/libvirt-lxc.a}
%{_libdir}/libvirt-qemu.a

%if %{with sanlock}
%files lock-sanlock
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/virt-sanlock-cleanup
%attr(755,root,root) %{_libexecdir}/libvirt_sanlock_helper
%attr(755,root,root) %{_libdir}/libvirt/lock-driver/sanlock.so
%{_datadir}/augeas/lenses/libvirt_sanlock.aug
%{_datadir}/augeas/lenses/tests/test_libvirt_sanlock.aug
%dir /var/lib/libvirt/sanlock
%{_mandir}/man8/virt-sanlock-cleanup.8*
%endif

%files daemon
%defattr(644,root,root,755)
%doc docs/*.xml
%dir %attr(700,root,root) %{_sysconfdir}/libvirt/nwfilter
%dir %attr(700,root,root) %{_sysconfdir}/libvirt/qemu
%dir %attr(700,root,root) %{_sysconfdir}/libvirt/qemu/networks
%dir %attr(700,root,root) %{_sysconfdir}/libvirt/qemu/networks/autostart
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/libvirtd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtlockd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/libvirt-admin.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtlogd.conf
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/qemu/networks/default.xml
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/nwfilter/*.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sasl/libvirt.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/libvirtd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtlockd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtlogd
%attr(754,root,root) /etc/rc.d/init.d/libvirtd
%attr(754,root,root) /etc/rc.d/init.d/virtlockd
%attr(754,root,root) /etc/rc.d/init.d/virtlogd
%{systemdunitdir}/libvirtd.service
%{systemdunitdir}/virt-guest-shutdown.target
%{systemdunitdir}/virtlockd.service
%{systemdunitdir}/virtlockd.socket
%{systemdunitdir}/virtlockd-admin.socket
%{systemdunitdir}/virtlogd.service
%{systemdunitdir}/virtlogd.socket
%{systemdunitdir}/virtlogd-admin.socket
%config(noreplace) %verify(not md5 mtime size) /usr/lib/sysctl.d/60-libvirtd.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd
%attr(755,root,root) %{_libexecdir}/libvirt_iohelper
%attr(755,root,root) %{_libexecdir}/libvirt_parthelper
%attr(755,root,root) %{_libexecdir}/virt-aa-helper
%attr(755,root,root) %{_sbindir}/libvirtd
%attr(755,root,root) %{_sbindir}/virtlockd
%attr(755,root,root) %{_sbindir}/virtlogd
%{_datadir}/augeas/lenses/libvirtd.aug
%{_datadir}/augeas/lenses/libvirt_lockd.aug
%{_datadir}/augeas/lenses/virtlockd.aug
%{_datadir}/augeas/lenses/virtlogd.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd.aug
%{?with_qemu:%{_datadir}/augeas/lenses/tests/test_libvirt_lockd.aug}
%{_datadir}/augeas/lenses/tests/test_virtlockd.aug
%{_datadir}/augeas/lenses/tests/test_virtlogd.aug
%if %{with polkit}
%{_datadir}/polkit-1/actions/org.libvirt.api.policy
%{_datadir}/polkit-1/actions/org.libvirt.unix.policy
%{_datadir}/polkit-1/rules.d/50-libvirt.rules
%endif
%{_mandir}/man8/libvirtd.8*
%{_mandir}/man8/virtlockd.8*
%{_mandir}/man8/virtlogd.8*
%dir /var/lib/libvirt
%dir /var/lib/libvirt/dnsmasq
%attr(711,root,root) %dir /var/lib/libvirt/boot
%attr(700,root,root) %dir /var/lib/libvirt/network
%attr(711,root,root) %dir /var/lib/libvirt/images
%attr(711,root,root) %dir /var/lib/libvirt/filesystems
%attr(700,root,root) %dir /var/log/libvirt
%attr(711,root,root) %dir /var/cache/libvirt
%dir /var/run/libvirt
%dir /var/run/libvirt/network
%{systemdtmpfilesdir}/%{name}.conf
%attr(755,root,root) %{_libexecdir}/libvirt_leaseshelper
%dir %{_libdir}/libvirt/connection-driver
%{_datadir}/libvirt/cpu_map.xml
%{?with_netcf:%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_interface.so}
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_network.so
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_nodedev.so
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_nwfilter.so
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_secret.so
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_storage.so
%{?with_vbox:%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_vbox.so}
%dir %{_libdir}/libvirt/lock-driver
%attr(755,root,root) %{_libdir}/libvirt/lock-driver/lockd.so
%dir %{_libdir}/libvirt/storage-backend
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_disk.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_fs.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_iscsi.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_logical.so
# mpath requires libdevmapper, but libvirt itself requires it too
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_mpath.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_scsi.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_sheepdog.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_zfs.so

%if %{with glusterfs}
%files daemon-storage-gluster
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_gluster.so
%endif

%if %{with ceph}
%files daemon-storage-rbd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_rbd.so
%endif

%if %{with libxl}
%files daemon-libxl
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/libxl.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/libxl-lockd.conf
%{?with_sanlock:%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/libxl-sanlock.conf}
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.libxl
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_libxl.so
%{_datadir}/augeas/lenses/libvirtd_libxl.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_libxl.aug
%attr(700,root,root) %dir /var/lib/libvirt/libxl
%attr(700,root,root) %dir /var/run/libvirt/libxl
%attr(700,root,root) %dir /var/log/libvirt/libxl
%endif

%if %{with lxc}
%files daemon-lxc
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/lxc.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.lxc
%attr(700,root,root) %dir /var/lib/libvirt/lxc
%attr(700,root,root) %dir /var/run/libvirt/lxc
%attr(700,root,root) %dir /var/log/libvirt/lxc
%{_datadir}/augeas/lenses/libvirtd_lxc.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_lxc.aug
%attr(755,root,root) %{_libexecdir}/libvirt_lxc
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_lxc.so
%endif

%if %{with qemu}
%files daemon-qemu
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/qemu.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/qemu-lockd.conf
%{?with_sanlock:%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/qemu-sanlock.conf}
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.qemu
%attr(750,qemu,qemu) %dir /var/cache/libvirt/qemu
%attr(750,qemu,qemu) %dir /var/lib/libvirt/qemu
%attr(700,root,root) %dir /var/log/libvirt/qemu
%attr(700,root,root) %dir /var/run/libvirt/qemu
%{_datadir}/augeas/lenses/libvirtd_qemu.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_qemu.so
%endif

%if %{with uml}
%files daemon-uml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_uml.so
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.uml
%attr(700,root,root) %dir /var/lib/libvirt/uml
%attr(700,root,root) %dir /var/run/libvirt/uml
%attr(700,root,root) %dir /var/log/libvirt/uml
%endif

%if %{with xen}
%files daemon-xen
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_xen.so
%endif

%files client
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/libvirt-guests
%attr(754,root,root) /etc/rc.d/init.d/libvirt-guests
%{systemdunitdir}/libvirt-guests.service
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virt-login-shell.conf
%attr(755,root,root) %{_bindir}/virsh
%attr(755,root,root) %{_bindir}/virt-admin
%attr(755,root,root) %{_bindir}/virt-host-validate
%attr(4755,root,root) %{_bindir}/virt-login-shell
%attr(755,root,root) %{_bindir}/virt-xml-validate
%attr(755,root,root) %{_bindir}/virt-pki-validate
%attr(754,root,root) %{_libexecdir}/libvirt-guests.sh
%{_mandir}/man1/virsh.1*
%{_mandir}/man1/virt-admin.1*
%{_mandir}/man1/virt-host-validate.1*
%{_mandir}/man1/virt-login-shell.1*
%{_mandir}/man1/virt-xml-validate.1*
%{_mandir}/man1/virt-pki-validate.1*
%dir %{_datadir}/libvirt/schemas
%{_datadir}/libvirt/schemas/basictypes.rng
%{_datadir}/libvirt/schemas/capability.rng
%{_datadir}/libvirt/schemas/cputypes.rng
%{_datadir}/libvirt/schemas/domain.rng
%{_datadir}/libvirt/schemas/domaincaps.rng
%{_datadir}/libvirt/schemas/domaincommon.rng
%{_datadir}/libvirt/schemas/domainsnapshot.rng
%{_datadir}/libvirt/schemas/interface.rng
%{_datadir}/libvirt/schemas/network.rng
%{_datadir}/libvirt/schemas/networkcommon.rng
%{_datadir}/libvirt/schemas/nodedev.rng
%{_datadir}/libvirt/schemas/nwfilter.rng
%{_datadir}/libvirt/schemas/secret.rng
%{_datadir}/libvirt/schemas/storagecommon.rng
%{_datadir}/libvirt/schemas/storagepool.rng
%{_datadir}/libvirt/schemas/storagevol.rng
# for test driver (built into libvirt)
%{_datadir}/libvirt/test-screenshot.png

%files utils
%defattr(644,root,root,755)

%if %{with systemtap}
%files -n systemtap-libvirt
%defattr(644,root,root,755)
%{_datadir}/systemtap/tapset/libvirt_functions.stp
%{_datadir}/systemtap/tapset/libvirt_probes.stp
%{_datadir}/systemtap/tapset/libvirt_qemu_probes.stp
%endif

%if %{with wireshark}
%files -n wireshark-libvirt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/wireshark/plugins/*/libvirt.so
%endif
