%define major 7
%define libname %mklibname mysqlcppconn %{major}
%define devname %mklibname mysqlcppconn -d

Summary:	A MySQL database connector for C++
Name:		mysql-connector-c++
Version:	1.1.11
Release:	2
Group:		System/Libraries
License:	GPLv2
Url:		http://dev.mysql.com/downloads/connector/cpp/
Source0:	http://cdn.mysql.com/Downloads/Connector-C++/%{name}-%{version}.tar.gz
#Patch0:		mysql-connector-c++-1.1.11-detect-mariadb.patch
#Patch1:		mysql-connector-c++-1.1.11-mariadb.patch
BuildRequires:	cmake
BuildRequires:	mariadb-devel mariadb-common
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libcrypto)

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
Requires:	mariadb-devel
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
%cmake -DMYSQLCPPCONN_BUILD_EXAMPLES:BOOL=OFF \
	-DRPM_LAYOUT:BOOL=ON \
	-DCMAKE_ENABLE_C++11:BOOL=ON \
        -DMYSQL_INCLUDE_DIR=%{_includedir}/mysql \
        -DMYSQL_LIB=%{_libdir}/libmysqlclient.so
        
%make

%install
cp build/cppconn/config.h  cppconn/config.h
%makeinstall_std -C build

rm -fr %{buildroot}%{_libdir}/*.a

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%license %{_docdir}/%{name}-%{version}/LICENSE
%doc %{_docdir}/%{name}-%{version}
%{_includedir}/*.h
%{_includedir}/cppconn
%{_libdir}/*.so
