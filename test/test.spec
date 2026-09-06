Name:           test-rpm
Version:        0.0.1
Release:        1%{?dist}
Summary:        Python test script

License:        GPLv3
Source0:        file://%{name}.tar

BuildRequires:  gcc

%description
Simple python script to test RPM packaging.

%prep
%autosetup -c

%build
gcc -g -o %{name} %{name}.c

%install

mkdir -p %{buildroot}%{_bindir}

install -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files

%{_bindir}/%{name}
