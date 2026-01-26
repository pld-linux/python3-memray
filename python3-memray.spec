#
# Conditional build:
%bcond_with	doc	# API documentation (not in sdist)
%bcond_with	tests	# unit tests (not in sdist)

Summary:	A memory profiler for Python applications
Summary(pl.UTF-8):	Profilter pamięciowy dla aplikacji w Pythonie
Name:		python3-memray
Version:	1.19.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/memray/
Source0:	https://files.pythonhosted.org/packages/source/m/memray/memray-%{version}.tar.gz
# Source0-md5:	2142af623ddf0bd4b46944d9940d0dc7
URL:		https://pypi.org/project/memray/
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	lz4-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-Cython
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-greenlet
BuildRequires:	python3-ipython
BuildRequires:	python3-jinja2 >= 2.9
BuildRequires:	python3-packaging
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-textual-snapshot
BuildRequires:	python3-rich >= 11.2.0
BuildRequires:	python3-textual >= 0.43
%if "%{py3_ver}" == "3.7"
BuildRequires:	python3-typing_extensions
%endif
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-ipython
BuildRequires:	python3-sphinx_argparse
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Memray is a memory profiler for Python. It can track memory
allocations in Python code, in native extension modules, and in the
Python interpreter itself. It can generate several different types of
reports to help you analyze the captured memory usage data. While
commonly used as a CLI tool, it can also be used as a library to
perform more fine-grained profiling tasks.

%description -l pl.UTF-8
Memray to profiler pamięciowy dla Pythona. Potrafi śledzić
przydzielanie pamięci w kodzie w Pythonie, w modułach rozszerzeń
natywnych oraz samym interpreterze Pythona. Potrafi generować kilka
różnych typów raportów, pomagających analizować przechwycone dane o
wykorzystaniu pamięci. Zwykle jest używany jako narzędzie CLI, ale
może być używany także jako biblioteka do wykonywania większej liczby
bardziej dopasowanych zadań profilujących.

%package apidocs
Summary:	API documentation for Python memray module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona memray
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python memray module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona memray.

%prep
%setup -q -n memray-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/memray/*.pyx

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS.rst README.md
%attr(755,root,root) %{_bindir}/memray
%attr(755,root,root) %{_bindir}/memray%{py3_ver}
%dir %{py3_sitedir}/memray
%{py3_sitedir}/memray/_inject.abi3.so
%{py3_sitedir}/memray/_memray.cpython-*.so
%{py3_sitedir}/memray/_test_utils.cpython-*.so
%{py3_sitedir}/memray/py.typed
%{py3_sitedir}/memray/*.py
%{py3_sitedir}/memray/*.pyi
%{py3_sitedir}/memray/__pycache__
%{py3_sitedir}/memray/_ipython
%{py3_sitedir}/memray/commands
%{py3_sitedir}/memray/reporters
%{py3_sitedir}/memray-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
