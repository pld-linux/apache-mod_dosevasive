%define		mod_name	dosevasive
%define 	apxs		/usr/sbin/apxs
Summary:	Apache DoS Evasive Maneuvers Module
Summary(pl):	Modu³ manewrów omijaj±cych ataki DoS dla Apache
Name:		apache-mod_%{mod_name}
Version:	1.10
Release:	1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://www.nuclearelephant.com/projects/dosevasive/mod_%{mod_name}_%{version}.tar.gz
# Source0-md5:	5e5eee54b3fba64c83898828693931ff
Source1:	%{name}.conf
URL:		http://www.nuclearelephant.com/projects/dosevasive/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2
BuildRequires:	zlib-devel
Requires(post,preun):	%{apxs}
Requires:	apache >= 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
mod_dosevasive is an evasive maneuvers module for Apache to provide
evasive action in the event of an HTTP DoS or DDoS attack or brute
force attack. It is also designed to be a detection and network
management tool, and can be easily configured to talk to ipchains,
firewalls, routers, and etcetera. mod_dosevasive presently reports
abuses via email and syslog facilities.

%description -l pl
mod_dosevasive to modu³ manewrów omijaj±cych dla Apache, zapewniaj±cy
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
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf

install .libs/mod_%{mod_name}20.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/80_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_pkglibdir}/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/httpd.conf/*
