%define	major 5
%define libname %mklibname mysqlcppconn %{major}
%define develname %mklibname mysqlcppconn -d

Summary:	A MySQL database connector for C++
Name:		mysql-connector-c++
Version:	1.1.0
Release:	%mkrel 1
Group:		System/Libraries
License:	GPL
URL:		http://dev.mysql.com/downloads/connector/cpp/
Source0:	http://mirrors.dotsrc.org/mysql/Downloads/Connector-C++/mysql-connector-c++-%{version}.tar.gz
Source1:	http://mirrors.dotsrc.org/mysql/Downloads/Connector-C++/mysql-connector-c++-%{version}.tar.gz.asc
Patch0:		mysql-connector-cpp-1.0.4-beta-cmake-paths-fix.patch
Patch1:		mysql-connector-cpp-1.0.5-gcc44.patch
Patch2:		mysql-connector-c++-1.0.5-no_examples.diff
Patch3:		mysql-connector-c++-1.1.0.bzr895.diff
BuildRequires:	cmake
BuildRequires:	mysql-devel
BuildRequires:	boost-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Connector/C++ is a tool that enables easy deployment and management of MySQL
server and database through your C++ application. 

%package -n	%{libname}
Summary:	The shared mysql-connector-cpp library
Group:          System/Libraries

%description -n	%{libname}
Connector/C++ is a tool that enables easy deployment and management of MySQL
server and database through your C++ application.

This package provides the shared mysql-connector-cpp library.


%package -n	%{develname}
Summary:	Development library and header files for development with mysql-connector-cpp
Group:          Development/C++
Requires:	%{libname} = %{version}
Provides:	mysql-connector-c++-devel = %{version}-%{release}

%description -n	%{develname}
Connector/C++ is a tool that enables easy deployment and management of MySQL
server and database through your C++ application. 

This package is only needed if you plan to develop or compile applications
which requires the mysql-connector-cpp library.

%prep
%setup -q -n mysql-connector-c++-%{version}
%patch0 -p1 -b .build
%patch1 -p1
%patch2 -p0
%patch3 -p1

%{__sed} -i -e 's/lib$/%{_lib}/' driver/CMakeLists.txt
%{__chmod} -x examples/*.cpp examples/*.txt

# fix dynload
find -name "*.cpp" | xargs perl -pi -e "s|libmysqlclient_r\.so|libmysqlclient\.so\.18|g"

%build
%serverbuild
cmake \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
    -DCMAKE_INSTALL_LIB_DIR:PATH=%{_libdir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DMYSQL_CONFIG_EXECUTABLE=%{_bindir}/mysql_config \
    -DMYSQLCPPCONN_DYNLOAD_MYSQL_LIB=%{_libdir}/libmysqlclient.so.18 \
    .

%make

%install
rm -rf %{buildroot}

%makeinstall_std

# cleanup
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_prefix}/ANNOUNCEMENT
rm -f %{buildroot}%{_prefix}/COPYING
rm -f %{buildroot}%{_prefix}/README

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README ANNOUNCEMENT COPYING CHANGES
%attr(0755,root,root) %{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/mysql-connector
%dir %{_includedir}/mysql-connector/cppconn
%attr(0644,root,root) %{_includedir}/mysql-connector/*.h
%attr(0644,root,root) %{_includedir}/mysql-connector/cppconn/*.h
%attr(0644,root,root) %{_libdir}/*.so



%changelog
* Mon Mar 21 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-1mdv2011.0
+ Revision: 647352
- sync slightly with fedora
- make it build (friggin cmake!)
- make it use the correct mysql lib all over the place
- fix deps
- 1.1.0

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-7mdv2011.0
+ Revision: 612974
- the mass rebuild of 2010.1 packages

* Tue Apr 20 2010 Funda Wang <fwang@mandriva.org> 1.0.5-6mdv2010.1
+ Revision: 536927
- specify libdir
- use cmake standard macro

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-1mdv2010.1
+ Revision: 507862
- import mysql-connector-c++


* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-1mdv2010.0
- initial Mandriva package (inspired by opensuse)
