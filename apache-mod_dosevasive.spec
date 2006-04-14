# TODO: cp spec name to apache-mod_evasive.spec as it is now official name
# see http://www.nuclearelephant.com/projects/dosevasive/
%define		mod_name	evasive
%define 	apxs		/usr/sbin/apxs
Summary:	Apache DoS Evasive Maneuvers Module
Summary(pl):	Modu³ manewrów omijaj±cych ataki DoS dla Apache
Name:		apache-mod_%{mod_name}
Version:	1.10.1
Release:	1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://www.nuclearelephant.com/projects/mod_evasive/mod_%{mod_name}_%{version}.tar.gz
# Source0-md5:	784fca4a124f25ccff5b48c7a69a65e5
Source1:	%{name}.conf
URL:		http://www.nuclearelephant.com/projects/mod_evasive/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires:	apache(modules-api) = %apache_modules_api
Provides:	apache-mod_dosevasive
Obsoletes:	apache-mod_dosevasive
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_(dos)evasive is an evasive maneuvers module for Apache to provide
evasive action in the event of an HTTP DoS or DDoS attack or brute
force attack. It is also designed to be a detection and network
management tool, and can be easily configured to talk to ipchains,
firewalls, routers, and etcetera. mod_dosevasive presently reports
abuses via email and syslog facilities.

%description -l pl
mod_(dos)evasive to modu³ manewrów omijaj±cych dla Apache, zapewniaj±cy
akcje omijaj±ce w przypadku ataków DoS, DDoS lub brute force na us³ugê
HTTP. Zosta³ zaprojektowany tak¿e jako narzêdzie do wykrywania i
zarz±dzania sieci±, mo¿e byæ ³atwo skonfigurowany do wspó³pracy z
ipchains, firewallami, routerami itp. mod_dosevasive obecnie raportuje
nadu¿ycia poczt± elektroniczn± i poprzez sysloga.

%prep
%setup -q -n mod_%{mod_name}

%build
%{apxs} -c mod_%{mod_name}20.c -lz

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

install .libs/mod_%{mod_name}20.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/80_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
