## MR -- enable this if want create debuginfo
%define  debug_package %{nil}

Summary:	An advanced and secure webserver for Unix
Name:		hiawatha
Version:	9.5
Release:	3%{?dist}
Source0:	http://www.hiawatha-webserver.org/files/%{name}-%{version}.tar.gz
Source1:	%{name}-sysvscript
Patch0: 	hiawatha-maxuploadsize.patch
Patch1: 	polarssl-1.3.6.patch
License:	GPLv2+
Group:		System Environment/Daemons
URL:		http://www.hiawatha-webserver.org/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libxslt-devel
#BuildRequires:	polarssl-devel
BuildRequires:	cmake >= 2.8.4

%description
Hiawatha is an advanced and secure webserver for Unix. It has been written
with 'being secure' as its main goal. This resulted in a webserver which
has for example DoS protection, connection control and traffic throttling.
It has of course also thoroughly been checked and tested for buffer overflows.

%prep
%setup -q
#sed -i -e '/add_subdirectory(polarssl)/d' -e 's| polarssl/include||' -e 's|${POLARSSL_LIBRARY}||' CMakeLists.txt
#sed -i '/^\tpolarssl/d' CMakeFiles.txt

%patch0
%patch1 -p1

%build
%cmake	-DENABLE_CHROOT:BOOL=ON \
	-DENABLE_MONITOR:BOOL=ON \
	-DUSE_PKCS11_HELPER_LIBRARY:BOOL=ON \
	-DCMAKE_SKIP_RPATH:BOOL=OFF \
	-DCMAKE_INSTALL_LOCALSTATEDIR:PATH=/var \
	-DCMAKE_INSTALL_PREFIX:PATH="/usr" \
	-DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
	-DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
	-DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
	-DCMAKE_INSTALL_MANDIR:PATH=%{_mandir}
make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
#make install INSTALL_ROOT=%{buildroot}

mkdir -p %{buildroot}/var/log/%{name}
install -D -m 644 logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
perl -pi -e 's|/usr/var/log/hiawatha/|/var/log/hiawatha/|' %{buildroot}%{_sysconfdir}/%{name}/hiawatha.conf
install -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

%files
%defattr(-,root,root)
%dir /var/log/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_sbindir}/%{name}
%{_mandir}/*/*.*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_localstatedir}/www/%{name}/
%{_initrddir}/%{name}
%{_bindir}/ssi-cgi
%{_sbindir}/cgi-wrapper
%{_sbindir}/wigwam
%{_libdir}/%{name}

%changelog
* Sun Apr 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.5-3
- use patch for aesni.c for workaround 'old' binutils

* Sat Apr 26 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.5-2
- recompile without patch (because compile bnutils 2.24 for Centos 5 64bit)

* Thu Apr 24 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.5-1
- update to 9.5 (with patch because the same touble like 9.5 with new polarssl)

* Sun Mar 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.4-1
- update to 9.4 with patch

* Thu Dec 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 9.3.1-1
- update to 9.3.1

* Mon Dec 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 9.3-2
- patch maxuploadsize from 100 to 2048MB

* Mon Nov 18 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 9.3-1
- update to 9.3
- make simple release

* Fri Aug 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 9.2-7.2
- fix hiawatha init (hiawatha-sysvscript) where change gprinf to 'echo -n'

* Sun Jul 28 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 9.2-7.1
- compile for Centos 5/6
- taken from http://download.opensuse.org/repositories/home:/akauffman/CentOS_CentOS-6/src/
- modified .spec for centos 5 compatilibity
