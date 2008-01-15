%define dname %{name}_%version

Summary:	Lists files open by processes
Name:		lsof
Version:	4.78
Release:	%mkrel 2
License:	Free
Url:		ftp://vic.cc.purdue.edu/pub/tools/unix/lsof/
Group:		Monitoring
Source0:	ftp://vic.cc.purdue.edu/pub/tools/unix/%name/%dname.tar.bz2
Patch0:		lsof_4.64-perl-example-fix.patch
Patch1:		lsof_4.60-has-security.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{version}-buildroot

%description
Lsof's name stands for LiSt Open Files, and it does just that. It lists
information about files that are open by the processes running on a UNIX
system.

%prep
%setup -q -c -n %{dname}

#
# Sort out whether this is the wrapped or linux specific tar ball.
#
[ -d %{dname} ] && cd %{dname}
[ -f %{dname}_src.tar ] && tar xf %{dname}_src.tar
[ -d %{dname}.linux -a ! -d %{dname} ] && \
	mv %{dname}.linux %{dname}
[ -d %{dname}_src ] && cd %{dname}_src
%patch0 -p1
%patch1 -p1

%build
[ -d %{dname}/%{dname}_src ] && cd %{dname}/%{dname}_src

LINUX_BASE=/proc
export LINUX_BASE
./Configure -n linux

%make DEBUG="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
[ -d %{dname}/%{dname}_src ] && cd %{dname}/%{dname}_src
install -s %{name} -D $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -m644 lsof.8 -D $RPM_BUILD_ROOT%{_mandir}/man8/lsof.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{dname}/00*
%attr(0755,root,kmem) %{_sbindir}/%{name}
%{_mandir}/man8/lsof.8*


