#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.116
%define		qtver		5.15.2
%define		kfname		prison

Summary:	A barcode abstraction layer
Name:		kf5-%{kfname}
Version:	5.116.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	a65d26234fa57ad6ba40b42e31911df5
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Multimedia-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	hspell-devel
BuildRequires:	hunspell-devel
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	libdmtx-devel
BuildRequires:	ninja
BuildRequires:	qrencode-devel
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRequires:	zxing-cpp-nu-devel >= 1.2.0
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
Prison has a Prison::AbstractBarcode, which is the base class for the
actual barcode generators, currently Prison::QRCodeBarcode and
Prison::DataMatrixBarcode are the two implemented barcode generators.

Prison currently ships a BarcodeWidget, which is a QWidget with a
barcode painted upon, as well as a BarcodeItem, which is a
QGraphicsItem with a barcode painted upon.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{_datadir}/qlogging-categories5/prison.categories
%ghost %{_libdir}/libKF5Prison.so.5
%{_libdir}/libKF5Prison.so.5.*.*
%ghost %{_libdir}/libKF5PrisonScanner.so.5
%{_libdir}/libKF5PrisonScanner.so.5.*.*
%{_libdir}/qt5/qml/org/kde/prison
%{_datadir}/qlogging-categories5/prison.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/Prison
%{_libdir}/cmake/KF5Prison
%{_libdir}/qt5/mkspecs/modules/qt_Prison.pri
%{_libdir}/libKF5Prison.so
%{_includedir}/KF5/PrisonScanner
%{_libdir}/libKF5PrisonScanner.so
