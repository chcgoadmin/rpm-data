%define debug_package %{nil}
Name: logstash-forwarder
Version: 0.4.0
Release: 2%{?dist}
Summary: Logstash forwarding agent	
Group: System Environment/Daemons
License: Apache License, Version 2.0	
URL: https://github.com/elasticsearch/logstash-forwarder
Source0: %{name}-%{version}.tar.gz	
#Source: https://github.com/elasticsearch/logstash-forwarder
Vendor: ELK Stack - Elasticsearch.org
Packager: chcgoadmin@gmail.com 


BuildRequires: golang	
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel, /usr/sbin/groupdel, /usr/bin/getent 

%description
Logstash forwarer agent for shipping logs to a logstash server.

%pre
# create logstash-forwarder group
if ! getent group logstash-forwarder >/dev/null; then
  groupadd -r logstash-forwarder
fi

# create logstash-forwarder user
if ! getent passwd logstash-forwarder >/dev/null; then
  useradd -r -g logstash-forwarder -d /opt/logstash-forwarder -s /sbin/nologin -c "logstash-forwarder" logstash-forwarder
fi


%prep
%setup -q
%build
go build -o %{name} .

%install
install -d %{buildroot}/opt/%{name}/bin/
install -d %{buildroot}/etc/%{name}/
install -d %{buildroot}/etc/init.d/
install -d %{buildroot}/etc/sysconfig/
install -d %{buildroot}/var/log/%{name}/

install -m 755 ./%{name} %{buildroot}/opt/%{name}/bin/%{name}
install -m 644 ./%{name}.conf.example  %{buildroot}/etc/%{name}/%{name}.conf.example
install -m 755 ./%{name}.init %{buildroot}/etc/init.d/%{name}
install -m 644 ./%{name}.sysconf %{buildroot}/etc/sysconfig/%{name}

%files
/opt/%{name}/bin/%{name}
/etc/%{name}/%{name}.conf.example
/etc/init.d/%{name}
/etc/sysconfig/%{name}
/var/log/%{name}/


%post
chkconfig --add %{name}
chown -Rv logstash-forwarder:logstash-forwarder /opt/%{name}/
chown -Rv logstash-forwarder:logstash-forwarder /var/log/%{name}/ 

%preun
# Verify its and actuall uninstall and not an upgrade.
if [[ $1 -eq 0 ]]
then
  # stop the service 
  /etc/init.d/%{name} stop 2>&1 /dev/null
fi

%postun
# Verify its and actuall uninstall and not an upgrade.
if [[ $1 -eq 0 ]]
then
  # remove user and group 
  /sbin/chkconfig --del logstash-forwarder
  if getent passwd logstash-forwarder >/dev/null ; then
    /usr/sbin/userdel logstash-forwarder
  fi

  if getent group logstash-forwarder > /dev/null ; then
    /usr/sbin/groupdel logstash-forwarder
  fi

fi

