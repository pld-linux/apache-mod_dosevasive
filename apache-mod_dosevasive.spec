%define		mod_name	dosevasive
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: DoS Evasive Maneuvers Module
Summary(pl):	Modu³ do apache:  -
Name:		apache-mod_%{mod_name}
Version:	1.5.1
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.networkdweebs.com/stuff/mod_%{mod_name}.tar.gz
# Source0-md5:	e2c96678c1c8262e12e7ecb8bdf43550
URL:		http://www.networkdweebs.com/stuff/security.html
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
Requires(post,preun):	%{apxs}
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
Apache module: DoS Evasive Maneuvers Module

%description -l pl
Modu³ do apache: -

%prep
%setup -q -n %{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lz

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

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
