%{?!ros_distro:%global ros_distro rolling}
%global pkg_name rqt_service_caller
%global normalized_pkg_name %{lua:return (string.gsub(rpm.expand('%{pkg_name}'), '_', '-'))}

Name:           ros-rolling-rqt-service-caller
Version:        1.2.1
Release:        2%{?dist}
Summary:        ROS %{pkg_name} package

License:        BSD
URL:            http://wiki.ros.org/rqt_service_caller
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  bloom-rpm-macros
BuildRequires:  python%{python3_pkgversion}-devel

%{?bloom_package}

%description
rqt_service_caller provides a GUI plugin for calling arbitrary services.


%package devel
Release:        %{release}%{?release_suffix}
Summary:        %{summary}
Provides:       %{name} = %{version}-%{release}
Requires:       %{name}-runtime = %{version}-%{release}

%description devel
rqt_service_caller provides a GUI plugin for calling arbitrary services.


%package runtime
Release:        %{release}
Summary:        %{summary}

%description runtime
rqt_service_caller provides a GUI plugin for calling arbitrary services.


%prep
%autosetup -p1


%generate_buildrequires
%bloom_buildrequires


%build
%py3_build


%install
%py3_install -- --prefix "%{bloom_prefix}"
install -m0644 -p -D package.xml %{buildroot}%{bloom_prefix}/share/%{pkg_name}/package.xml


%if 0%{?with_tests}
%check
# Look for a directory with a name indicating that it contains tests
TEST_TARGET=$(ls -d * | grep -m1 "^\(test\|tests\)" ||:)
if [ -n "$TEST_TARGET" ] && %__python3 -m pytest --version; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
%__python3 -m pytest $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif


%files devel
%dir %{bloom_prefix}
%ghost %{bloom_prefix}/share/%{pkg_name}/package.xml


%files runtime
%{bloom_prefix}


%changelog
* Fri Mar 22 2024 Brandon Ong <brandon@openrobotics.org> - 1.2.1-2
- Autogenerated by Bloom
