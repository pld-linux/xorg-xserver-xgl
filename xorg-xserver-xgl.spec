Summary:	X.org server
Summary(pl):	Serwer X.org
Name:		xorg-xserver-xgl
%define		_snap	20060220
Version:	0.0.%{_snap}
Release:	0.1
License:	MIT
Group:		X11/Servers
Source0:	xserver-%{_snap}.tar.bz2
# Source0-md5:	aa0ccb851ec5f7f9b132581d9a5827e4
Source1:	Mesa-%{_snap}.tar.bz2
# Source1-md5:	7674d2c603b5834259e4e5a820cefd5b
Patch0:		%{name}-slang-library-noise.patch
URL:		http://www.freedesktop.org/wiki/Software/Xgl
# for glx headers
BuildRequires:	Mesa-libGL-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	cpp
BuildRequires:	libdrm-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	pam-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXdmcp-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfont-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXres-devel
BuildRequires:	xorg-lib-libXt-devel >= 1.0.0
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libXxf86dga-devel
BuildRequires:	xorg-lib-libXxf86misc-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-lib-libdmx-devel
BuildRequires:	xorg-lib-libfontenc-devel
BuildRequires:	xorg-lib-liblbxutil-devel
BuildRequires:	xorg-lib-libxkbfile-devel
BuildRequires:	xorg-lib-libxkbui-devel
BuildRequires:	xorg-lib-xtrans-devel
BuildRequires:	xorg-proto-bigreqsproto-devel
BuildRequires:	xorg-proto-compositeproto-devel
BuildRequires:	xorg-proto-damageproto-devel
BuildRequires:	xorg-proto-dmxproto-devel
BuildRequires:	xorg-proto-evieext-devel
BuildRequires:	xorg-proto-fixesproto-devel
BuildRequires:	xorg-proto-fontsproto-devel
BuildRequires:	xorg-proto-glproto-devel >= 1.4.4
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
Obsoletes:	X11-Xserver
Obsoletes:	X11-modules
Obsoletes:	XFree86-Xserver
Obsoletes:	XFree86-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Xorg server is a generally used X server which uses display hardware.
It requires proper driver for your display hardware.

%description -l pl
Serwer Xorg to podstawowy serwer X wyświetlający obraz na karcie
graficznej. Do działania wymaga odpowiedniego sterownika.

%prep
%setup -q -a1 -n xserver-%{_snap}
cd xorg
%patch0 -p1

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
	--with-mesa-source="`pwd`/../Mesa-%{_snap}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd xorg
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{*,*/*}.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/Xgl
%dir %{_libdir}/xorg/modules/xgl
%attr(755,root,root) %{_libdir}/xorg/modules/xgl/lib*.so
