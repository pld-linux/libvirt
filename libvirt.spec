# TODO:
# - parallels-sdk >= 7.0.22?
# - virtuozzo storage?
# - mm-ctl (https://github.com/tfukushima/mm-ctl ?)
# - numad (https://pagure.io/numad/ or https://github.com/yhaenggi/numad/releases ?)
# - vstorage, vstorage-mount
# - pldize virtlockd.init
# - update vserver patch, if anybody needs it
# - package firewalld zone definition (see files)
#
# Conditional build:
# - virtualization
%bcond_without	esx		# VMware ESX support
%bcond_without	hyperv		# Hyper-V support
%bcond_without	libxl		# libxenlight support
%bcond_without	lxc		# LXC support
%bcond_without	openvz		# OpenVZ support
%bcond_without	qemu		# Qemu support
%bcond_without	vbox		# VirtualBox support
%bcond_without	vmware		# VMware Workstation/Player support
%bcond_with	vserver		# Support for Linux-VServer guests
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

# Xen supported architectures
%ifnarch %{ix86} %{x8664} %{arm} aarch64
%undefine	with_libxl
%endif

Summary:	Toolkit to interact with virtualization capabilities
Summary(pl.UTF-8):	Narzędzia współpracujące z funkcjami wirtualizacji
Name:		libvirt
Version:	6.4.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://libvirt.org/sources/libvirt-%{version}.tar.xz
# Source0-md5:	a14cfce86474d4f039a27ce140b176e7
Source1:	%{name}.init
Source2:	%{name}.tmpfiles
Patch0:		%{name}-sasl.patch
Patch1:		%{name}-bash-completions-dir.patch
Patch2:		%{name}-qemu-acl.patch
Patch4:		%{name}-udevadm-settle.patch
Patch5:		vserver.patch
Patch6:		bashisms.patch
URL:		https://www.libvirt.org/
BuildRequires:	acl-devel
BuildRequires:	attr-devel
BuildRequires:	audit-libs-devel
BuildRequires:	augeas-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_ceph:BuildRequires:	ceph-devel}
BuildRequires:	curl-devel >= 7.18.0
BuildRequires:	cyrus-sasl-devel >= 2.1.26
BuildRequires:	dbus-devel >= 1.0.0
BuildRequires:	device-mapper-devel >= 1.0.0
# rst2html5 rst2man
BuildRequires:	docutils
BuildRequires:	gawk
BuildRequires:	gcc >= 6:4.4
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.48.0
%{?with_glusterfs:BuildRequires:	glusterfs-devel >= 3.4.1}
BuildRequires:	gnutls-devel >= 3.2.0
BuildRequires:	libapparmor-devel
BuildRequires:	libblkid-devel >= 2.17
BuildRequires:	libcap-ng-devel >= 0.4.0
BuildRequires:	libfuse-devel >= 2.8.6
BuildRequires:	libgcrypt-devel
BuildRequires:	libiscsi-devel >= 1.18.0
BuildRequires:	libnl-devel >= 3.2
BuildRequires:	libpcap-devel >= 1.5.0
BuildRequires:	libselinux-devel >= 2.5
BuildRequires:	libssh-devel >= 0.7
BuildRequires:	libssh2-devel >= 1.3
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.9.1
BuildRequires:	libxml2-progs >= 1:2.9.1
BuildRequires:	libxslt-devel
BuildRequires:	libxslt-progs
BuildRequires:	ncurses-devel
%{?with_netcf:BuildRequires:	netcf-devel >= 0.2.0}
BuildRequires:	numactl-devel
%{?with_hyperv:BuildRequires:	openwsman-devel >= 2.2.3}
BuildRequires:	parted-devel >= 1.8.0
BuildRequires:	pkgconfig
%{?with_polkit:BuildRequires:	polkit}
%{?with_polkit:BuildRequires:	polkit-devel >= 0.90}
BuildRequires:	python3 >= 1:3.0
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.673
%{?with_sanlock:BuildRequires:	sanlock-devel >= 0.8}
BuildRequires:	systemd-devel
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	udev-devel >= 1:219
%{?with_wireshark:BuildRequires:	wireshark-devel >= 2.4.0}
%{?with_libxl:BuildRequires:	xen-devel >= 4.6}
# For disk driver
BuildRequires:	xorg-lib-libpciaccess-devel >= 0.10.0
BuildRequires:	yajl-devel >= 2.0.3
Requires:	curl-libs >= 7.18.0
Requires:	cyrus-sasl-libs >= 2.1.26
Requires:	device-mapper-libs >= 1.0.0
Requires:	glib2 >= 1:2.48.0
Requires:	gnutls-libs >= 3.2.0
Requires:	libcap-ng >= 0.4.0
Requires:	libnl >= 3.2
Requires:	libpcap >= 1.5.0
Requires:	libselinux >= 2.5
Requires:	libssh >= 0.7
Requires:	libssh2 >= 1.3
Requires:	libxml2 >= 1:2.9.1
%{?with_hyperv:Requires:	openwsman-libs >= 2.2.3}
Requires:	yajl >= 2.0.3
Obsoletes:	libvirt-daemon-esx
Obsoletes:	libvirt-daemon-hyperv
Obsoletes:	libvirt-daemon-openvz
Obsoletes:	libvirt-daemon-phyp < 6.0.0
Obsoletes:	libvirt-daemon-uml < 5.0.0
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
Summary:	bash-completion for libvirt
Summary(pl.UTF-8):	Bashowe dopełnianie składni poleceń libvirt
Group:		Applications/Shells
Requires:	bash-completion >= 2.0
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description -n bash-completion-%{name}
This package provides bash-completion for libvirt.

%description -n bash-completion-%{name} -l pl.UTF-8
Ten pakiet zapewnia bashowe dopełnianie składni dla poleceń libvirt.

%package devel
Summary:	Development files for programs using libvirt
Summary(pl.UTF-8):	Pliki programistyczne do programów wykorzystujących libvirt
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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

%package doc
Summary:	Documentation for libvirt
Summary(pl.UTF-8):	Dokumentacja do libvirt
Group:		Documentation
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description doc
Documentation for libvirt.

%description doc -l pl.UTF-8
Dokumentacja do libvirt.

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
Requires(post):	systemd-units
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	systemd-units
Requires(preun):	systemd-units
Requires:	%{name} = %{version}-%{release}
Requires:	device-mapper >= 1.0.0
Requires:	iproute2
Requires:	libblkid >= 2.17
# iscsi-direct driver
Requires:	libiscsi >= 1.18.0
%{?with_netcf:Requires:	netcf >= 0.2.0}
Requires:	parted-libs >= 1.8.0
Requires:	rc-scripts
# Needed for probing the power management features of the host.
Requires:	pm-utils
Requires:	systemd-units >= 37-0.10
Requires:	udev-libs >= 1:219
Requires:	util-linux
Requires:	virtual(module-tools)
Requires:	xorg-lib-libpciaccess >= 0.10.0
Suggests:	bridge-utils
Suggests:	cyrus-sasl >= 2.1.26
Suggests:	cyrus-sasl-digest-md5 >= 2.1.26
Suggests:	dmidecode
Suggests:	dnsmasq >= 2.41
Suggests:	ebtables
Suggests:	gawk
Suggests:	glusterfs-client >= 3.4.1
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
Requires:	xen >= 4.6
Provides:	libvirt(hypervisor)
Obsoletes:	libvirt-daemon-xen < 4.3.0

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

%package daemon-vbox
Summary:	Server side driver required to run VirtalBox guests
Summary(pl.UTF-8):	Sterownik wymagany po stronie serwera do uruchamiania gości VirtalBox
Group:		Libraries
Requires:	%{name}-daemon = %{version}-%{release}
Requires:	VirtualBox >= 5.2
Provides:	libvirt(hypervisor)

%description daemon-vbox
Server side driver required to manage the virtualization capabilities
of VirtualBox.

%description daemon-vbox -l pl.UTF-8
Sterownik wymagany po stronie serwera do zarządzania funkcjami
wirtualizacji VirtualBoksa.

%package client
Summary:	Client side utilities of the libvirt library
Summary(pl.UTF-8):	Narzędzia klienckie do biblioteki libvirt
Group:		Applications/System
Requires(post):	systemd-units
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	systemd-units
Requires(preun):	systemd-units
Requires:	%{name} = %{version}-%{release}
Requires:	gettext >= 0.18.1.1-6
Requires:	gnutls >= 3.2.0
Requires:	netcat-openbsd
Requires:	rc-scripts

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
Requires:	wireshark >= 2.4.0

%description -n wireshark-libvirt
Wireshark dissector module for libvirt packets.

%description -n wireshark-libvirt -l pl.UTF-8
Moduł sekcji Wiresharka do pakietów libvirt.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch4 -p1
%{?with_vserver:%patch5 -p1}
%patch6 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
install -d build
cd build
../%configure \
	PVCREATE=/sbin/pvcreate \
	VGCREATE=/sbin/vgcreate \
	LVCREATE=/sbin/lvcreate \
	PVREMOVE=/sbin/pvremove \
	VGREMOVE=/sbin/vgremove \
	LVREMOVE=/sbin/lvremove \
	LVCHANGE=/sbin/lvchange \
	VGCHANGE=/sbin/vgchange \
	  VGSCAN=/sbin/vgscan   \
	     PVS=/sbin/pvs      \
	     VGS=/sbin/vgs      \
	     LVS=/sbin/lvs      \
	      TC=/sbin/tc \
	   BRCTL=/sbin/brctl    \
	AUGPARSE=/usr/bin/augparse \
	ISCSIADM=/sbin/iscsiadm	\
	SHOWMOUNT=/usr/sbin/showmount \
	MOUNT=/bin/mount \
	UMOUNT=/bin/umount \
	MKFS=/sbin/mkfs \
	SHOWMOUNT=/usr/sbin/showmount \
	IP_PATH=/sbin/ip \
	IPTABLES_PATH=/usr/sbin/iptables \
	IP6TABLES_PATH=/usr/sbin/ip6tables \
	EBTABLES_PATH=/usr/sbin/ebtables \
	ISCSIADM=/sbin/iscsiadm \
	DMIDECODE=/usr/sbin/dmidecode \
	DNSMASQ=/usr/sbin/dnsmasq \
	RADVD=/usr/sbin/radvd \
	UDEVADM=/sbin/udevadm \
	MODPROBE=/sbin/modprobe \
	RMMOD=/sbin/rmmod \
	MMCTL=/usr/sbin/mm-ctl \
	OVSVSCTL=/usr/bin/ovs-vsctl \
	SCRUB=/usr/bin/scrub \
	NUMAD=/usr/bin/numad \
	QEMU_BRIDGE_HELPER=%{_libexecdir}/qemu-bridge-helper \
	QEMU_PR_HELPER=/usr/bin/qemu-pr-helper \
	SHEEPDOGCLI=/usr/sbin/collie \
	ZFS=/usr/sbin/zfs \
	ZPOOL=/usr/sbin/zpool \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-bash-completion \
	--with-bash-completions-dir=%{bash_compdir} \
	--with-init-script=systemd \
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
	%{__with_without polkit} \
	%{__with_without qemu} \
	%{__with_without sanlock} \
	--with-sasl \
	--with-selinux \
	--with-udev \
	%{__with_without vbox vbox %{_libdir}/VirtualBox} \
	--with-virtualport \
	%{__with_without vmware} \
	%{!?with_wireshark:--without-wireshark-dissector} \
	--x-libraries=%{_libdir}

%{__make} \
	AWK=gawk

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} -C build install \
	SYSTEMD_UNIT_DIR=%{systemdunitdir} \
	sasldir=%{_sysconfdir}/sasl \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/libvirtd
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvirt/connection-driver/*.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/libvirt/connection-driver/*.a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvirt/storage-backend/*.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/libvirt/storage-backend/*.a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvirt/storage-file/*.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/libvirt/storage-file/*.a}

%if %{with sanlock}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvirt/lock-driver/*.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/libvirt/lock-driver/*.a}
%endif
%if %{with wireshark}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/wireshark/plugins/*/epan/libvirt.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/wireshark/plugins/*/epan/libvirt.a} \
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
%doc AUTHORS ChangeLog NEWS README.rst
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
%{bash_compdir}/virsh
%{bash_compdir}/virt-admin
%{bash_compdir}/vsh

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvirt.so
%attr(755,root,root) %{_libdir}/libvirt-admin.so
%{?with_lxc:%attr(755,root,root) %{_libdir}/libvirt-lxc.so}
%attr(755,root,root) %{_libdir}/libvirt-qemu.so
%{_datadir}/%{name}/api
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

%files doc
%defattr(644,root,root,755)
%dir %{_docdir}/libvirt
%{_docdir}/libvirt/examples
%{_docdir}/libvirt/html

%if %{with sanlock}
%files lock-sanlock
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/virt-sanlock-cleanup
%attr(755,root,root) %{_libexecdir}/libvirt_sanlock_helper
%attr(755,root,root) %{_libdir}/libvirt/lock-driver/sanlock.so
%{_datadir}/augeas/lenses/libvirt_sanlock.aug
%if %{with qemu}
%{_datadir}/augeas/lenses/tests/test_libvirt_sanlock.aug
%endif
%dir /var/lib/libvirt/sanlock
%{_mandir}/man8/virt-sanlock-cleanup.8*
%endif

%files daemon
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/libvirt-admin.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/libvirtd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtinterfaced.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtlockd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtlogd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtnetworkd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtnodedevd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtnwfilterd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtproxyd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtsecretd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtstoraged.conf
%dir %attr(700,root,root) %{_sysconfdir}/libvirt/qemu
%dir %attr(700,root,root) %{_sysconfdir}/libvirt/qemu/networks
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/qemu/networks/default.xml
%dir %attr(700,root,root) %{_sysconfdir}/libvirt/qemu/networks/autostart
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
%dir %attr(700,root,root) %{_sysconfdir}/libvirt/nwfilter
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/nwfilter/*.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sasl/libvirt.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/libvirtd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtinterfaced
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtlockd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtlogd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtnetworkd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtnodedevd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtnwfilterd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtproxyd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtsecretd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtstoraged
%attr(754,root,root) /etc/rc.d/init.d/libvirtd
%{systemdunitdir}/libvirtd.service
%{systemdunitdir}/libvirtd.socket
%{systemdunitdir}/libvirtd-admin.socket
%{systemdunitdir}/libvirtd-ro.socket
%{systemdunitdir}/libvirtd-tcp.socket
%{systemdunitdir}/libvirtd-tls.socket
%{systemdunitdir}/virt-guest-shutdown.target
%{systemdunitdir}/virtinterfaced.service
%{systemdunitdir}/virtinterfaced.socket
%{systemdunitdir}/virtinterfaced-admin.socket
%{systemdunitdir}/virtinterfaced-ro.socket
%{systemdunitdir}/virtlockd.service
%{systemdunitdir}/virtlockd.socket
%{systemdunitdir}/virtlockd-admin.socket
%{systemdunitdir}/virtlogd.service
%{systemdunitdir}/virtlogd.socket
%{systemdunitdir}/virtlogd-admin.socket
%{systemdunitdir}/virtnetworkd.service
%{systemdunitdir}/virtnetworkd.socket
%{systemdunitdir}/virtnetworkd-admin.socket
%{systemdunitdir}/virtnetworkd-ro.socket
%{systemdunitdir}/virtnodedevd.service
%{systemdunitdir}/virtnodedevd.socket
%{systemdunitdir}/virtnodedevd-admin.socket
%{systemdunitdir}/virtnodedevd-ro.socket
%{systemdunitdir}/virtnwfilterd.service
%{systemdunitdir}/virtnwfilterd.socket
%{systemdunitdir}/virtnwfilterd-admin.socket
%{systemdunitdir}/virtnwfilterd-ro.socket
%{systemdunitdir}/virtproxyd.service
%{systemdunitdir}/virtproxyd.socket
%{systemdunitdir}/virtproxyd-admin.socket
%{systemdunitdir}/virtproxyd-ro.socket
%{systemdunitdir}/virtproxyd-tcp.socket
%{systemdunitdir}/virtproxyd-tls.socket
%{systemdunitdir}/virtsecretd.service
%{systemdunitdir}/virtsecretd.socket
%{systemdunitdir}/virtsecretd-admin.socket
%{systemdunitdir}/virtsecretd-ro.socket
%{systemdunitdir}/virtstoraged.service
%{systemdunitdir}/virtstoraged.socket
%{systemdunitdir}/virtstoraged-admin.socket
%{systemdunitdir}/virtstoraged-ro.socket
%config(noreplace) %verify(not md5 mtime size) /usr/lib/sysctl.d/60-libvirtd.conf
%attr(755,root,root) %{_sbindir}/libvirtd
%attr(755,root,root) %{_sbindir}/virtinterfaced
%attr(755,root,root) %{_sbindir}/virtlockd
%attr(755,root,root) %{_sbindir}/virtlogd
%attr(755,root,root) %{_sbindir}/virtnetworkd
%attr(755,root,root) %{_sbindir}/virtnodedevd
%attr(755,root,root) %{_sbindir}/virtnwfilterd
%attr(755,root,root) %{_sbindir}/virtproxyd
%attr(755,root,root) %{_sbindir}/virtsecretd
%attr(755,root,root) %{_sbindir}/virtstoraged
%attr(755,root,root) %{_libexecdir}/libvirt_iohelper
%attr(755,root,root) %{_libexecdir}/libvirt_leaseshelper
%attr(755,root,root) %{_libexecdir}/libvirt_parthelper
%attr(755,root,root) %{_libexecdir}/virt-aa-helper
# TODO:
#%{_libdir}/firewalld/zones/libvirt.xml
%dir %{_libdir}/libvirt/connection-driver
%{?with_netcf:%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_interface.so}
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_network.so
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_nodedev.so
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_nwfilter.so
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_secret.so
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_storage.so
%dir %{_libdir}/libvirt/lock-driver
%attr(755,root,root) %{_libdir}/libvirt/lock-driver/lockd.so
%dir %{_libdir}/libvirt/storage-backend
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_disk.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_fs.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_iscsi.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_iscsi-direct.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_logical.so
# mpath requires libdevmapper, but libvirt itself requires it too
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_mpath.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_scsi.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_sheepdog.so
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_zfs.so
%dir %{_libdir}/libvirt/storage-file
%attr(755,root,root) %{_libdir}/libvirt/storage-file/libvirt_storage_file_fs.so
%{_datadir}/augeas/lenses/libvirtd.aug
%{_datadir}/augeas/lenses/libvirt_lockd.aug
%{_datadir}/augeas/lenses/virtinterfaced.aug
%{_datadir}/augeas/lenses/virtlockd.aug
%{_datadir}/augeas/lenses/virtlogd.aug
%{_datadir}/augeas/lenses/virtnetworkd.aug
%{_datadir}/augeas/lenses/virtnodedevd.aug
%{_datadir}/augeas/lenses/virtnwfilterd.aug
%{_datadir}/augeas/lenses/virtproxyd.aug
%{_datadir}/augeas/lenses/virtsecretd.aug
%{_datadir}/augeas/lenses/virtstoraged.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd.aug
%{_datadir}/augeas/lenses/tests/test_virtinterfaced.aug
%{_datadir}/augeas/lenses/tests/test_virtlockd.aug
%{_datadir}/augeas/lenses/tests/test_virtlogd.aug
%{_datadir}/augeas/lenses/tests/test_virtnetworkd.aug
%{_datadir}/augeas/lenses/tests/test_virtnodedevd.aug
%{_datadir}/augeas/lenses/tests/test_virtnwfilterd.aug
%{_datadir}/augeas/lenses/tests/test_virtproxyd.aug
%{_datadir}/augeas/lenses/tests/test_virtsecretd.aug
%{_datadir}/augeas/lenses/tests/test_virtstoraged.aug
%{_datadir}/libvirt/cpu_map
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

%if %{with glusterfs}
%files daemon-storage-gluster
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvirt/storage-backend/libvirt_storage_backend_gluster.so
%attr(755,root,root) %{_libdir}/libvirt/storage-file/libvirt_storage_file_gluster.so
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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtxend.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.libxl
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtxend
%{systemdunitdir}/virtxend.service
%{systemdunitdir}/virtxend.socket
%{systemdunitdir}/virtxend-admin.socket
%{systemdunitdir}/virtxend-ro.socket
%attr(755,root,root) %{_sbindir}/virtxend
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_libxl.so
%{_datadir}/augeas/lenses/libvirtd_libxl.aug
%{_datadir}/augeas/lenses/virtxend.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_libxl.aug
%{_datadir}/augeas/lenses/tests/test_virtxend.aug
%attr(700,root,root) %dir /var/lib/libvirt/libxl
%attr(700,root,root) %dir /var/run/libvirt/libxl
%attr(700,root,root) %dir /var/log/libvirt/libxl
%endif

%if %{with lxc}
%files daemon-lxc
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/lxc.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtlxcd.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.lxc
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtlxcd
%{systemdunitdir}/virtlxcd.service
%{systemdunitdir}/virtlxcd.socket
%{systemdunitdir}/virtlxcd-admin.socket
%{systemdunitdir}/virtlxcd-ro.socket
%attr(755,root,root) %{_sbindir}/virtlxcd
%attr(755,root,root) %{_libexecdir}/libvirt_lxc
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_lxc.so
%{_datadir}/augeas/lenses/libvirtd_lxc.aug
%{_datadir}/augeas/lenses/virtlxcd.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_lxc.aug
%{_datadir}/augeas/lenses/tests/test_virtlxcd.aug
%attr(700,root,root) %dir /var/lib/libvirt/lxc
%attr(700,root,root) %dir /var/run/libvirt/lxc
%attr(700,root,root) %dir /var/log/libvirt/lxc
%endif

%if %{with qemu}
%files daemon-qemu
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/virt-qemu-run
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/qemu.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/qemu-lockd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtqemud.conf
%{?with_sanlock:%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/qemu-sanlock.conf}
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/libvirtd.qemu
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtqemud
%{systemdunitdir}/virtqemud.service
%{systemdunitdir}/virtqemud.socket
%{systemdunitdir}/virtqemud-admin.socket
%{systemdunitdir}/virtqemud-ro.socket
%attr(755,root,root) %{_sbindir}/virtqemud
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_qemu.so
%{_datadir}/augeas/lenses/libvirtd_qemu.aug
%{_datadir}/augeas/lenses/virtqemud.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
%{_datadir}/augeas/lenses/tests/test_libvirt_lockd.aug
%{_datadir}/augeas/lenses/tests/test_virtqemud.aug
%{_mandir}/man1/virt-qemu-run.1*
%attr(750,qemu,qemu) %dir /var/cache/libvirt/qemu
%attr(750,qemu,qemu) %dir /var/lib/libvirt/qemu
%attr(700,root,root) %dir /var/log/libvirt/qemu
%attr(700,root,root) %dir /var/run/libvirt/qemu
%endif

%if %{with vbox}
%files daemon-vbox
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virtvboxd.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/virtvboxd
%{systemdunitdir}/virtvboxd.service
%{systemdunitdir}/virtvboxd.socket
%{systemdunitdir}/virtvboxd-admin.socket
%{systemdunitdir}/virtvboxd-ro.socket
%attr(755,root,root) %{_sbindir}/virtvboxd
%attr(755,root,root) %{_libdir}/libvirt/connection-driver/libvirt_driver_vbox.so
%{_datadir}/augeas/lenses/virtvboxd.aug
%{_datadir}/augeas/lenses/tests/test_virtvboxd.aug
%endif

%files client
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/libvirt-guests
%{systemdunitdir}/libvirt-guests.service
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt/virt-login-shell.conf
%attr(755,root,root) %{_bindir}/virsh
%attr(755,root,root) %{_bindir}/virt-admin
%attr(755,root,root) %{_bindir}/virt-host-validate
# TODO: %attr(4754,root,virtlogin) and virtlogin group to access binary
%attr(4755,root,root) %{_bindir}/virt-login-shell
%attr(755,root,root) %{_bindir}/virt-xml-validate
%attr(755,root,root) %{_bindir}/virt-pki-validate
%attr(754,root,root) %{_libexecdir}/libvirt-guests.sh
%attr(754,root,root) %{_libexecdir}/virt-login-shell-helper
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
%{_datadir}/libvirt/schemas/domainbackup.rng
%{_datadir}/libvirt/schemas/domaincaps.rng
%{_datadir}/libvirt/schemas/domaincheckpoint.rng
%{_datadir}/libvirt/schemas/domaincommon.rng
%{_datadir}/libvirt/schemas/domainsnapshot.rng
%{_datadir}/libvirt/schemas/interface.rng
%{_datadir}/libvirt/schemas/network.rng
%{_datadir}/libvirt/schemas/networkcommon.rng
%{_datadir}/libvirt/schemas/networkport.rng
%{_datadir}/libvirt/schemas/nodedev.rng
%{_datadir}/libvirt/schemas/nwfilter.rng
%{_datadir}/libvirt/schemas/nwfilter_params.rng
%{_datadir}/libvirt/schemas/nwfilterbinding.rng
%{_datadir}/libvirt/schemas/secret.rng
%{_datadir}/libvirt/schemas/storagecommon.rng
%{_datadir}/libvirt/schemas/storagepool.rng
%{_datadir}/libvirt/schemas/storagepoolcaps.rng
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
%{?with_qemu:%{_datadir}/systemtap/tapset/libvirt_qemu_probes.stp}
%endif

%if %{with wireshark}
%files -n wireshark-libvirt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/wireshark/plugins/*/epan/libvirt.so
%endif
