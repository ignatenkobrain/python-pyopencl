%global srcname pyopencl

Name:           python-%{srcname}
Version:        2015.2
Release:        1%{?dist}
Summary:        Python wrapper for OpenCL

# https://bugzilla.redhat.com/show_bug.cgi?id=1219819#c16
# Boost (boost):
# pyopencl/cl/pyopencl-bessel-j.cl
# pyopencl/cl/pyopencl-bessel-y.cl
# pyopencl/cl/pyopencl-eval-tbl.cl
# GPLv2 (cephes):
# pyopencl/cl/pyopencl-airy.cl
# ASL 2.0 (ranluxcl):
# pyopencl/cl/pyopencl-ranluxcl.cl
License:        MIT and Boost and ASL 2.0 and GPLv2
URL:            http://mathema.tician.de/software/pyopencl
Source0:        https://github.com/pyopencl/pyopencl/archive/v%{version}/%{name}-%{version}.tar.gz
# https://github.com/inducer/compyte/pull/24
# Upstream maintainer not interested to unbundle compyte
Patch0:         0001-use-system-compyte.patch
Patch1:         0002-disable-executing-git-submodule.patch
# Have not asked upstream, but they want to enforce CFLAGS/LDFLAGS
Patch2:         0003-don-t-hack-distutils-with-C-LDFLAGS.patch

# pyopencl/cl/pyopencl-bessel-[j,y].cl and
# pyopencl/cl/pyopencl-eval-tbl.cl contain snippets taken from boost
# and cephes. pyopencl/cl/pyopencl-airy.cl contains code taken from
# cephes.
Provides:       bundled(boost-math)
Provides:       bundled(cephes) = 2.8
# pyopencl/cl/pyopencl-ranluxcl.cl contains a modified version of the
# ranluxcl library
Provides:       bundled(ranluxcl) = 1.3.1

BuildRequires:  git-core
BuildRequires:  boost-devel
BuildRequires:  opencl-headers ocl-icd-devel
BuildRequires:  atlas-devel blas-devel
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(gl)
# Testing requires opencl support
BuildRequires:  pocl

%description
PyOpenCL makes it possible to access GPUs and other massively 
parallel compute devices from Python. Specifically, PyOpenCL 
provides Pythonic access to the OpenCL parallel computation 
API in a manner similar to the sister project `PyCUDA`.

%package -n python2-%{srcname}
Summary:        Python 2 wrapper for OpenCL
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python2-devel
BuildRequires:  numpy
# Test deps
BuildRequires:  scipy
BuildRequires:  python-mako
BuildRequires:  python2-compyte
BuildRequires:  python2-pytools
BuildRequires:  python2-pytest
BuildRequires:  python-six
BuildRequires:  python-cffi%{?_isa}
Requires:       python2-compyte
Requires:       python2-pytools
Requires:       python2-pytest
Requires:       python-decorator
Requires:       python2-appdirs
Requires:       python-mako
Requires:       python-cffi%{?_isa}

%description -n python2-%{srcname}
PyOpenCL makes it possible to access GPUs and other massively 
parallel compute devices from Python. Specifically, PyOpenCL 
provides Pythonic access to the OpenCL parallel computation 
API in a manner similar to the sister project `PyCUDA`.

%package -n python3-%{srcname}
Summary:        Python 3 wrapper for OpenCL
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
# Test deps
BuildRequires:  python3-mako
BuildRequires:  python3-compyte
BuildRequires:  python3-scipy
BuildRequires:  python3-pytools
BuildRequires:  python3-pytest
BuildRequires:  python3-six
BuildRequires:  python3-cffi%{?_isa}
Requires:       python3-compyte
Requires:       python3-pytools
Requires:       python3-pytest
Requires:       python3-decorator
Requires:       python3-appdirs
Requires:       python3-mako
Requires:       python3-cffi%{?_isa}

%description -n python3-%{srcname}
PyOpenCL makes it possible to access GPUs and other massively 
parallel compute devices from Python. Specifically, PyOpenCL 
provides Pythonic access to the OpenCL parallel computation 
API in a manner similar to the sister project `PyCUDA`.

%prep
%autosetup -n %{srcname}-%{version} -S git

rm -f examples/{.gitignore,download-examples-from-wiki.py}

# generate html docs 
#sphinx-build doc/source html
# remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}

rm -rf %{py3dir}
mkdir -p %{py3dir}
cp -a . %{py3dir}

%build
%{__python2} configure.py --cl-enable-gl
%py2_build

pushd %{py3dir}
%{__python3} configure.py --cl-enable-gl
%py3_build
popd

%install
%py2_install
pushd %{py3dir}
%py3_install
popd

find %{buildroot}%{python2_sitearch}/%{srcname} -name '*.so' -exec chmod 755 {} ';'
find %{buildroot}%{python3_sitearch}/%{srcname} -name '*.so' -exec chmod 755 {} ';'

%check
pushd test/
  export PYTHONPATH=%{buildroot}%{python2_sitearch}
  find -name '*.py' -exec py.test-%{python2_version} -v {} ';'
popd
pushd %{py3dir}/test/
  export PYTHONPATH=%{buildroot}%{python3_sitearch}
  find -name '*.py' -exec py.test-%{python3_version} -v {} ';'
popd

%files -n python2-%{srcname}
%license LICENSE
%doc examples
%{python2_sitearch}/%{srcname}
%{python2_sitearch}/%{srcname}-%{version}-*egg-info

%files -n python3-%{srcname}
%license LICENSE
%doc examples
%{python3_sitearch}/%{srcname}
%{python3_sitearch}/%{srcname}-%{version}-*egg-info

%changelog
* Thu Nov 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2015.2-1
- Update to 2015.2
- Add some description to bundled libs providing
- Provide exact version of bundled cephes
- Force tests passed
- Fixed dependencies list

* Wed Nov 04 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2015.1-4
- Fixed license tag
- Run tests
- Add license

* Sat Oct 24 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2015.1-3
- Fix errors during review

* Sat Oct 24 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2015.1-2
- Trivial fixes in spec

* Fri May 08 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2015.1-1
- Initial package
