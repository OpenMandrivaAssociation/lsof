%define dname %{name}_%{version}

Summary:	Lists files open by processes
Name:		lsof
Version:	4.99.0
Release:	1
License:	Free
Group:		Monitoring
Url:		https://people.freebsd.org/~abe/
Source0:	https://github.com/lsof-org/lsof/archive/%{version}.tar.gz
BuildRequires:	pkgconfig(libselinux)
BuildRequires:	pkgconfig(libtirpc)
# For soelim
BuildRequires:	groff

%description
Lsof's name stands for LiSt Open Files, and it does just that. It lists
information about files that are open by the processes running on a UNIX
system.

%prep
%setup -q
%autopatch -p1


%build
./Configure -n linux
%make_build DEBUG="%{optflags} -I/usr/include/tirpc" LSOF_CC="%{__cc}" CFGL="%{ldflags} -L./lib -llsof -lselinux -ltirpc"
# rebase to 4.93 introduced change in Lsof.8 with unhandled .so inclusion
soelim -r Lsof.8 > lsof.1

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
install -p -m 0755 lsof ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
install -p -m 0644 lsof.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/lsof.1

%files
%doc 00README 00CREDITS 00FAQ 00LSOF-L 00QUICKSTART
%{_bindir}/lsof
%{_mandir}/man*/*

