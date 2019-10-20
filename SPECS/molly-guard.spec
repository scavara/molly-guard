%define _mandir		%{_datadir}/man 

Name:           molly-guard
Version:        0.7.2
Release:        0
Summary:        Protects machines from accidental shutdowns/reboots.
Group:          Applications/Internet
License:        GPL
URL:            http://ftp.debian.org/debian/pool/main/m/molly-guard/
Vendor:         Martin F. Krafft <madduck@madduck.net>
Source0:	http://deb.debian.org/debian/pool/main/m/molly-guard/%{name}_%{version}.tar.gz
Source1:	http://deb.debian.org/debian/pool/main/m/molly-guard/%{name}_%{version}.dsc
Patch0:		Makefile.patch
Patch1:		shutdown.patch
Patch2:		rc-enable-hostname-query.patch
Prefix:         %{_prefix}
Packager: 	scavara
BuildRoot:      %{_tmppath}/%{name}-root

%description
The package installs a shell script that overrides the existing
shutdown/reboot/halt/poweroff/coldreboot/pm-hibernate/pm-suspend* commands
and first runs a set of scripts, which all have to exit successfully,
before molly-guard invokes the real command.

One of the scripts checks for existing SSH sessions. If any of the four
commands are called interactively over an SSH session, the shell script
prompts you to enter the name of the host you wish to shut down. This should
adequately prevent you from accidental shutdowns and reboots.

molly-guard diverts the real binaries to /lib/molly-guard/.  You can bypass
molly-guard by running those binaries directly.

%prep
cd $RPM_BUILD_DIR
rm -rf * 
gzip -dc $RPM_SOURCE_DIR/molly-guard_0.7.2.tar.gz | tar -xvvf -
if [ $? -ne 0 ]; then
  exit $?
fi
mv $RPM_BUILD_DIR/%{name}_%{version}/%{name}-%{version}/* .
rm -rf %{name}_%{version} 
chown -R root.root .
chmod -R a+rX,g-w,o-w .
%patch0 -p0
%patch1 -p0
%patch2 -p0

%build
make all prefix=%{_prefix} etc_prefix=/

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
install -m755 -oroot -groot -d ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name}
install -m644 -oroot -groot debian/changelog debian/copyright ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post
st=()
alternatives="alternatives --install /sbin/halt halt /lib/molly-guard/molly-guard 999 "
for c in halt reboot shutdown poweroff coldreboot pm-hibernate pm-suspend pm-suspend-hybrid
do
  if [ -e /sbin/$c ]
  then
    cmd_list+=($c)
  fi
done
for l in ${cmd_list[@]}
do 
 alternatives+="--slave /sbin/$l $l /lib/molly-guard/molly-guard "
   if [ $l == "pm*" ]
   then
     ln -s /usr/lib64/pm-utils/bin/pm-action /lib/molly-guard/$l
   else
     ln -s /bin/systemctl /lib/molly-guard/$l
   fi
done
eval $alternatives
alternatives --set halt /lib/molly-guard/molly-guard

%files
/etc/molly-guard/rc
/etc/molly-guard/run.d/10-print-message
/etc/molly-guard/run.d/30-query-hostname
/lib/molly-guard/molly-guard
/usr/share/doc/molly-guard/changelog
/usr/share/doc/molly-guard/copyright
%{_mandir}/man8/molly-guard.8.gz

%changelog
* 20.10.2019 scavara <scavara@gmail.com> 0.7.2
- First attempt to port from Debian repo to run on RHEL/CentOS versions 7

