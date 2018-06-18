%define major 7
%define libname %mklibname mysqlcppconn %{major}
%define devname %mklibname mysqlcppconn -d

Summary:	A MySQL database connector for C++
Name:		mysql-connector-c++
Version:	1.1.6
Release:	2
Group:		System/Libraries
License:	GPLv2
Url:		http://dev.mysql.com/downloads/connector/cpp/
Source0:	http://cdn.mysql.com/Downloads/Connector-C++/%{name}-%{version}.tar.gz
Patch1:		mariadb_api.patch
BuildRequires:	cmake
BuildRequires:	mariadb-devel mariadb-common
BuildRequires:	boost-devel

%description
Connector/C++ is a tool that enables easy deployment and management of MySQL
server and database through your C++ application.

%package -n	%{libname}
Summary:	The shared mysql-connector-cpp library
Group:		System/Libraries

%description -n	%{libname}
Connector/C++ is a tool that enables easy deployment and management of MySQL
server and database through your C++ application.

This package provides the shared mysql-connector-cpp library.

%package -n	%{devname}
Summary:	Development library and header files for development with mysql-connector-cpp
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	mysql-connector-c++-devel = %{version}-%{release}

%description -n	%{devname}
Connector/C++ is a tool that enables easy deployment and management of MySQL
server and database through your C++ application.

This package is only needed if you plan to develop or compile applications
which requires the mysql-connector-cpp library.

%prep
%setup -q
sed  -i -e 's/lib$/%{_lib}/' driver/CMakeLists.txt
chmod  -x examples/*.cpp examples/*.txt

# Save examples to keep directory clean (for doc)
mkdir _doc_examples
cp -pr examples _doc_examples

%apply_patches

%build
%cmake -DMYSQLCPPCONN_BUILD_EXAMPLES:BOOL=OFF
%make

%install
cp build/cppconn/config.h  cppconn/config.h
%makeinstall_std -C build
rm -fr %{buildroot}%{_prefix}/COPYING
rm -fr %{buildroot}%{_prefix}/INSTALL
rm -fr %{buildroot}%{_prefix}/README
rm -fr %{buildroot}%{_prefix}/ANNOUNCEMENT
rm -fr %{buildroot}%{_prefix}/Licenses_for_Third-Party_Components.txt

rm -fr %{buildroot}%{_libdir}/*.a

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%doc README CHANGES COPYING ANNOUNCEMENT Licenses_for_Third-Party_Components.txt
%{_includedir}/*.h
%{_includedir}/cppconn
%{_libdir}/*.so
