# NOTE: deprecated in favour of libdnf.spec
#
# Conditional build:
%bcond_with	python		# Python bindings (any) [python*-hawkey* modules are built from libdnf.spec now]
%bcond_without	python3		# Python 3.x bindings

%if %{without python}
%undefine	with_python3
%endif
Summary:	High-level API for the libsolv library
Summary(pl.UTF-8):	Wysokopoziomowe API dla biblioteki libsolv
Name:		hawkey
Version:	0.6.4
%define	gitrel	1
Release:	3
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/rpm-software-management/hawkey/releases
Source0:	https://github.com/rpm-software-management/hawkey/archive/%{name}-%{version}-%{gitrel}.tar.gz
# Source0-md5:	abc0179de2cb162c170c1fce17ed7f50
URL:		https://github.com/rpm-software-management/hawkey
BuildRequires:	check-devel
BuildRequires:	cmake >= 2.4
BuildRequires:	expat-devel
BuildRequires:	libsolv-devel >= 0.6.5
%{?with_python:BuildRequires:	python-devel >= 2}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpm-devel
BuildRequires:	rpmbuild(macros) >= 1.612
BuildRequires:	sphinx-pdg
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	libsolv >= 0.6.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# hawkey(3) man page shared between python-hawkey and python3-hawkey
%define		_duplicate_files_terminate_build	0

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
Requires:	libsolv-devel >= 0.6.5
Requires:	rpm-devel
Requires:	zlib-devel
Obsoletes:	hawkey-static

%description devel
Header files for hawkey library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki hawkey.

%package -n python-hawkey
Summary:	Python 2.x bindings for hawkey library
Summary(pl.UTF-8):	Wiązania Pythona 2.x do biblioteki hawkey
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-hawkey
Python 2.x bindings for hawkey library.

%description -n python-hawkey -l pl.UTF-8
Wiązania Pythona 2.x do biblioteki hawkey.

%package -n python-hawkey-test
Summary:	Test module for hawkey library
Summary(pl.UTF-8):	Moduł testowy dla biblioteki hawkey
Group:		Development/Libraries
Requires:	python-hawkey = %{version}-%{release}

%description -n python-hawkey-test
Test module for hawkey library.

%description -n python-hawkey-test -l pl.UTF-8
Moduł testowy dla biblioteki hawkey.

%package -n python3-hawkey
Summary:	Python 3.x bindings for hawkey library
Summary(pl.UTF-8):	Wiązania Pythona 3.x do biblioteki hawkey
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-hawkey
Python 3.x bindings for hawkey library.

%description -n python3-hawkey -l pl.UTF-8
Wiązania Pythona 3.x do biblioteki hawkey.

%package -n python-hawkey-apidocs
Summary:	API documentation for Python hawkey module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona hawkey
Group:		Documentation
Obsoletes:	hawkey-apidocs < 0.6.4-2
BuildArch:	noarch

%description -n python-hawkey-apidocs
API documentation for Python hawkey module.

%description -n python-hawkey-apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona hawkey.

%prep
%setup -q -n %{name}-%{name}-%{version}-%{gitrel}
: > cmake/modules/FindPythonInstDir.cmake

%build
install -d build %{?with_python3:build-py3}
cd build
%cmake .. \
	-DPYTHON_INSTALL_DIR=%{py_sitedir}

%{__make}

%{__make} doc%{!?with_python:-man}

%if %{with python3}
cd ../build-py3
%cmake .. \
	-DPYTHON_INSTALL_DIR=%{py3_sitedir} \
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

%if %{with python}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}/hawkey
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/hawkey
%py_postclean
%if %{with python3}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}/hawkey
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}/hawkey
%endif
%else
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/hawkey.3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%attr(755,root,root) %{_libdir}/libhawkey.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhawkey.so
%{_includedir}/hawkey
%{_pkgconfigdir}/hawkey.pc

%if %{with python}
%files -n python-hawkey
%defattr(644,root,root,755)
%dir %{py_sitedir}/hawkey
%attr(755,root,root) %{py_sitedir}/hawkey/_hawkeymodule.so
%{py_sitedir}/hawkey/*.py[co]
%{_mandir}/man3/hawkey.3*

%files -n python-hawkey-test
%defattr(644,root,root,755)
%dir %{py_sitedir}/hawkey/test
%{py_sitedir}/hawkey/test/*.py[co]
%attr(755,root,root) %{py_sitedir}/hawkey/test/_hawkey_testmodule.so

%if %{with python3}
%files -n python3-hawkey
%defattr(644,root,root,755)
%dir %{py3_sitedir}/hawkey
%attr(755,root,root) %{py3_sitedir}/hawkey/_hawkey.so
%{py3_sitedir}/hawkey/*.py
%{py3_sitedir}/hawkey/__pycache__
%{_mandir}/man3/hawkey.3*
%endif

%files -n python-hawkey-apidocs
%defattr(644,root,root,755)
%doc build/doc/{*.html,*.js,_static}
%endif
