#
# Conditional build:
%bcond_without	libGL		# don't build mesa's libGL
#
Summary:	Xgl X server
Summary(pl):	Serwer X Xgl
Name:		xorg-xserver-xgl
%define		_mesasnap	20060406
%define		_snap		20060411
Version:	0.0.%{_snap}
Release:	1
License:	MIT
Group:		X11/Servers
Source0:	xserver-%{_snap}.tar.bz2
# Source0-md5:	f73dba494834a0dff86259486a3b10eb
Source1:	Mesa-%{_mesasnap}.tar.bz2
# Source1-md5:	277cc3e846bfe33862ea70c2558721aa
Patch0:		%{name}-mesa-tfp-update-1.patch
URL:		http://www.freedesktop.org/wiki/Software/Xgl
# for glx headers
BuildRequires:	Mesa-libGL-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	cpp
BuildRequires:	glitz-devel >= 0.5.5
BuildRequires:	libdrm-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	pam-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXfont-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXres-devel
BuildRequires:	xorg-lib-libXt-devel >= 1.0.0
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libXxf86misc-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-lib-libfontenc-devel
BuildRequires:	xorg-lib-libxkbfile-devel
BuildRequires:	xorg-lib-libxkbui-devel
BuildRequires:	xorg-lib-xtrans-devel
BuildRequires:	xorg-proto-bigreqsproto-devel
BuildRequires:	xorg-proto-compositeproto-devel
BuildRequires:	xorg-proto-damageproto-devel
BuildRequires:	xorg-proto-evieext-devel
BuildRequires:	xorg-proto-fixesproto-devel
BuildRequires:	xorg-proto-fontsproto-devel
BuildRequires:	xorg-proto-glproto-devel >= 1.4.5-3
BuildRequires:	xorg-proto-printproto-devel
BuildRequires:	xorg-proto-randrproto-devel
BuildRequires:	xorg-proto-recordproto-devel
BuildRequires:	xorg-proto-renderproto-devel
BuildRequires:	xorg-proto-resourceproto-devel
BuildRequires:	xorg-proto-scrnsaverproto-devel
BuildRequires:	xorg-proto-trapproto-devel
BuildRequires:	xorg-proto-videoproto-devel
BuildRequires:	xorg-proto-xcmiscproto-devel
BuildRequires:	xorg-proto-xextproto-devel
BuildRequires:	xorg-proto-xf86bigfontproto-devel
BuildRequires:	xorg-proto-xf86dgaproto-devel
BuildRequires:	xorg-proto-xf86driproto-devel
BuildRequires:	xorg-proto-xf86miscproto-devel
BuildRequires:	xorg-proto-xf86vidmodeproto-devel
BuildRequires:	xorg-proto-xineramaproto-devel
BuildRequires:	xorg-proto-xproto-devel
BuildRequires:	xorg-util-util-macros >= 0.99.2
# for rgb.txt
Requires:	xorg-app-rgb >= 0.99.3
Requires:	xorg-app-xkbcomp
# just for %{_includedir}/bitmaps dir
Requires:	xorg-data-xbitmaps
Requires:	xorg-data-xkbdata
# xserver requires default fixed and cursosr fonts.
Requires:	xorg-font-font-alias
Requires:	xorg-font-font-cursor-misc
Requires:	xorg-font-font-misc-misc-base
# for new app-defaults location
Requires:	xorg-lib-libXt >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Xorg server is a generally used X server which uses display hardware.
It requires proper driver for your display hardware.

This package contains Xgl server.

%description -l pl
Serwer Xorg to podstawowy serwer X wy¶wietlaj±cy obraz na karcie
graficznej. Do dzia³ania wymaga odpowiedniego sterownika.

Ten pakiet zawiera serwer Xgl.

%package libGL
Summary:	OpenGL library used inside Xgl
Summary(pl):	Biblioteka OpenGL u¿ywana wewn±trz Xgl
Group:		X11/Servers
Requires:	%{name} = %{version}-%{release}

%description libGL
OpenGL library used inside Xgl to allow rendering. You still need
normal OpenGL library (like nvidia's or ati's) to run Xgl.

%description libGL -l pl
BIblioteka OpenGL u¿ywana wewn±trz Xgl w celu umo¿liwienia
renderingu. Normalna biblioteka OpenGL (jak nvidii lub ati) jest
w dalszym ci±gu potrzebna by uruchomiæ Xgl.

%prep
%setup -q -a1 -n xserver-%{_snap}

cd Mesa-%{_mesasnap}
%patch0 -p0

%build
cd xorg
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-glx \
	--enable-dri \
	--enable-xkb \
	--enable-xgl \
	--enable-xglx \
	--disable-xorg \
	--disable-xprint \
	--disable-dmx \
	--disable-xvfb \
	--disable-xnest \
	--with-default-font-path="%{_fontsdir}/misc,%{_fontsdir}/TTF,%{_fontsdir}/OTF,%{_fontsdir}/Type1,%{_fontsdir}/CID,%{_fontsdir}/100dpi,%{_fontsdir}/75dpi" \
	--with-mesa-source="`pwd`/../Mesa-%{_mesasnap}"

%{__make}

# build libGL from mesa snap
%if %{with libGL}
cd ../Mesa-%{_mesasnap}

%ifarch %{ix86}
targ=-x86
%else
targ=""
%endif

%{__make} linux${targ} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_FLAGS="%{rpmcflags} -fno-strict-aliasing" \
	XLIB_DIR=%{_libdir} \
	SRC_DIRS="glx/x11" \
	PROGRAM_DIRS=

%endif

%install
rm -rf $RPM_BUILD_ROOT

cd xorg
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{*,*/*}.{la,a}

%if %{with libGL}
install -d $RPM_BUILD_ROOT%{_libdir}/xgl

cd ../Mesa-%{_mesasnap}/lib

install libGL.so.1.2 $RPM_BUILD_ROOT%{_libdir}/xgl
ln -s libGL.so.1.2 $RPM_BUILD_ROOT%{_libdir}/xgl/libGL.so.1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/Xgl
%dir %{_libdir}/xorg/modules/xgl
%attr(755,root,root) %{_libdir}/xorg/modules/xgl/lib*.so

%if %{with libGL}
%files libGL
%defattr(644,root,root,755)
%dir %{_libdir}/xgl
%attr(755,root,root) %{_libdir}/xgl/*
%endif
