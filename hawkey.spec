#
# Conditional build:
%bcond_without	python3		# Python 3.x bindings

%define		gitrev	428a977
Summary:	High-level API for the libsolv library
Summary(pl.UTF-8):	Wysokopoziomowe API dla biblioteki libsolv
Name:		hawkey
Version:	0.4.14
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/hawkey/%{name}-%{gitrev}.tar.xz/627bc061598350d8eb2615df8f6c653b/%{name}-%{gitrev}.tar.xz
# Source0-md5:	627bc061598350d8eb2615df8f6c653b
URL:		https://github.com/akozumpl/hawkey
BuildRequires:	check-devel
BuildRequires:	cmake >= 2.4
BuildRequires:	expat-devel
BuildRequires:	libsolv-devel >= 0.6.0
BuildRequires:	python-devel >= 2
%{?with_python3:BuildRequires:	python3-devel >= 3}
BuildRequires:	rpm-devel
BuildRequires:	sphinx-pdg
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	libsolv >= 0.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hawkey is a library providing simplified C and Python API to libsolv.

%description -l pl.UTF-8
Hawkey to biblioteka udostępniająca uproszczone API dla języków C i
Python do biblioteki libsolv.

%package devel
Summary:	Header files for hawkey library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki hawkey
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libsolv-devel >= 0.6.0
Requires:	rpm-devel
Requires:	zlib-devel

%description devel
Header files for hawkey library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki hawkey.

%package static
Summary:	Static hawkey library
Summary(pl.UTF-8):	Statyczna biblioteka hawkey
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static hawkey library.

%description static -l pl.UTF-8
Statyczna biblioteka hawkey.

%package apidocs
Summary:	API documentation for hawkey library
Summary(pl.UTF-8):	Dokumentacja API biblioteki hawkey
Group:		Documentation

%description apidocs
API documentation for hawkey library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki hawkey.

%package -n python-hawkey
Summary:	Python 2.x bindings for hawkey library
Summary(pl.UTF-8):	Wiązania Pythona 2.x do biblioteki hawkey
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-hawkey
Python 2.x bindings for hawkey library.

%description -n python-hawkey -l pl.UTF-8
Wiązania Pythona 2.x do biblioteki hawkey.

%package -n python3-hawkey
Summary:	Python 3.x bindings for hawkey library
Summary(pl.UTF-8):	Wiązania Pythona 3.x do biblioteki hawkey
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-hawkey
Python 3.x bindings for hawkey library.

%description -n python3-hawkey -l pl.UTF-8
Wiązania Pythona 3.x do biblioteki hawkey.

%prep
%setup -q -n %{name}

%build
install -d build %{?with_python3:build-py3}
cd build
%cmake ..

%{__make}
%{__make} doc

%if %{with python3}
cd ../build-py3
%cmake .. \
	-DPYTHON_DESIRED=3

%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%{__make} -C build-py3/src/python install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/hawkey/test
%py_comp $RPM_BUILD_ROOT%{py_sitedir}/hawkey
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/hawkey
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%attr(755,root,root) %{_libdir}/libhawkey.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhawkey.so
%{_includedir}/hawkey
%{_pkgconfigdir}/hawkey.pc
%{_mandir}/man3/hawkey.3*

%files apidocs
%defattr(644,root,root,755)
%doc build/doc/{*.html,*.js,_static}

%files -n python-hawkey
%defattr(644,root,root,755)
%dir %{py_sitedir}/hawkey
%attr(755,root,root) %{py_sitedir}/hawkey/_hawkeymodule.so
%{py_sitedir}/hawkey/__init__.py[co]

%if %{with python3}
%files -n python3-hawkey
%defattr(644,root,root,755)
%dir %{py3_sitedir}/hawkey
%attr(755,root,root) %{py3_sitedir}/hawkey/_hawkey.so
%{py3_sitedir}/hawkey/__init__.py
%endif
