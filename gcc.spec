%define _buildid .87

%global DATE 20131212
%global SVNREV 205936
%global gcc_version 4.8.2

# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 7
#global _unpackaged_files_terminate_build 0

%global gccv 48

%global libstdcplusplus_ver 6.0.19
%global libquadmath_ver 0.0.0
%global libitm_ver 1.0.0
%global libgo_ver 0.0.0

# triggers and obsoletes for these old versions to ensure upgradeability
%global hard_obsolete_ver 4.6.2-2

%global multilib_64_archs sparc64 ppc64 s390x x86_64

# define for obsoleteing the old gcc builds
#global obsolete_gcc 1

# for the alternatives setup
%if 0%{?gccv:1}
%global gcc_prio 482
%endif

%ifarch %{ix86} x86_64 ia64 ppc ppc64 alpha
%global build_ada 1
%else
%global build_ada 0
%endif

%global build_fortran 1

%if 0%{?rhel} || 0%{?amzn}
%global build_java 0
%else
%global build_java 1
%endif

%ifarch %{ix86} x86_64 ppc ppc64 s390 s390x %{arm}
%global build_go 1
%else
%global build_go 0
%endif

%ifarch %{ix86} x86_64 ia64
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif

%ifarch %{ix86} x86_64 ppc ppc64
%global build_libasan 1
%else
%global build_libasan 0
%endif
%ifarch x86_64
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 s390 s390x %{arm}
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 s390 s390x
%global build_libitm 1
%else
%global build_libitm 0
%endif

%if 0%{?rhel} >= 7 || 0%{?amzn}
%global build_cloog 0
%else
%global build_cloog 0
%endif

%if 0%{?rhel} == 5 || 0%{?rhel} == 6
%global build_libstdcxx_docs 0
%else
%global build_libstdcxx_docs 1
%endif
# If you don't have already a usable gcc-java and libgcj for your arch,
# do on some arch which has it rpmbuild -bc --with java_tar gcc.spec
# which creates libjava-classes-%{version}-%{release}.tar.bz2
# With this then on the new arch do rpmbuild -ba -v --with java_bootstrap gcc.spec
%global bootstrap_java %{?_with_java_bootstrap:%{build_java}}%{!?_with_java_bootstrap:0}
%global build_java_tar %{?_with_java_tar:%{build_java}}%{!?_with_java_tar:0}
%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%global multilib_32_arch i686
%endif

%if 0%{?gccv}
%global build_cloog 0
%global build_java 0
%endif

# Amazon overrides
%if 0%{?amzn:1} || 0%{?rhel:1}
# we have the "real" golang
%global build_go 0
# no support for objc by unpopular non-demand
%global build_objc 0
# no support for gcj of any kind
%global build_java 0
# others, just to make sure
%global build_cloog 0
%endif

%global _skip_check 1

Summary: Various compilers (C, C++, Objective-C, ...)
Name: gcc%{?gccv}
Version: %{gcc_version}
Release: %{gcc_release}%{?_buildid}%{?dist}
%if 0%{?gccv:1}
Provides: gcc = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc < %{version}-%{release}}
%endif
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-4_7-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
%global isl_version 0.11.1
Source1: ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
%global cloog_version 0.18.0
Source2: ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-%{cloog_version}.tar.gz
%global fastjar_ver 0.97
Source4: http://download.savannah.nongnu.org/releases/fastjar/fastjar-%{fastjar_ver}.tar.gz
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
# Need binutils >= 2.23.51.0.1 for better GOLD support
BuildRequires: binutils >= 2.23.51.0.1
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, sharutils
BuildRequires: texinfo, texinfo-tex, /usr/bin/pod2man
BuildRequires: systemtap-sdt-devel >= 1.3
%if %{build_go}
BuildRequires: /bin/hostname
%endif
# For VTA guality testing
BuildRequires: gdb
%if %{build_java}
BuildRequires: /usr/share/java/eclipse-ecj.jar, zip, unzip
%if %{bootstrap_java}
Source10: libjava-classes-%{version}-%{release}.tar.bz2
%else
BuildRequires: gcc-java, libgcj
%endif
%endif
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
%if %{build_libstdcxx_docs}
BuildRequires: doxygen >= 1.7.1
BuildRequires: graphviz, docbook5-style-xsl
#BuildRequires: dblatex, texlive-collection-latex
BuildRequires: texlive-latex
%endif
# these are required to make this compiler functional
Requires: cpp%{?gccv}%{?_isa} = %{version}-%{release}
Requires: libgcc%{?gccv}%{?_isa} = %{version}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
# Need binutils that support %gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
# Need binutils with complete GOLD support
Requires: binutils >= 2.23.51.0.1
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel%{?_isa} >= 2.2.90-12
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7 || 0%{?amzn}
%ifarch %{arm}
Requires: glibc >= 2.16
%endif
%endif
Requires: libgcc%{?_isa} >= %{version}-%{release}
Requires: libgomp%{?_isa} >= %{version}-%{release}

%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
Obsoletes: libgnat < %{version}-%{release}
%endif
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
AutoReq: true
Provides: bundled(libiberty)

%if 0%{?gccv:1}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
%endif

Patch0: gcc48-hack.patch
Patch1: gcc48-java-nomulti.patch
Patch2: gcc48-ppc32-retaddr.patch
Patch3: gcc48-rh330771.patch
Patch4: gcc48-i386-libgomp.patch
Patch5: gcc48-sparc-config-detection.patch
Patch6: gcc48-libgomp-omp_h-multilib.patch
Patch7: gcc48-libtool-no-rpath.patch
Patch8: gcc48-cloog-dl.patch
Patch9: gcc48-cloog-dl2.patch
Patch10: gcc48-pr38757.patch
Patch11: gcc48-libstdc++-docs.patch
Patch12: gcc48-no-add-needed.patch
Patch13: gcc48-pr56564.patch
Patch14: gcc48-pr56493.patch
Patch15: gcc48-color-auto.patch
Patch16: gcc48-pr58956.patch

Patch1000: fastjar-0.97-segfault.patch
Patch1001: fastjar-0.97-len1.patch
Patch1002: fastjar-0.97-filename0.patch
Patch1003: fastjar-CVE-2010-0831.patch
Patch1004: fastjar-man.patch
Patch1005: fastjar-0.97-aarch64-config.patch

Patch1100: isl-%{isl_version}-aarch64-config.patch

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%global _gnu %{nil}
%endif
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparcv9 ppc
%global gcc_target_platform %{_target_platform}
%endif

%description
The gcc package contains the GNU Compiler Collection version 4.8.
You'll need this package in order to compile C code.

%package -n libgcc%{?gccv}
Summary: GCC version 4.8 shared support library
Group: System Environment/Libraries
## older packages used to avoid auto generated deps for libgcc due to the
## circular dependency between libgcc and glibc. We hope the newer yum is smart
## enough to handle it.
#Autoreq: false
%if 0%{?gccv:1}
Provides: libgcc = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: libgcc < %{version}-%{release}}
#Obsoletes: libgcc < %{hard_obsolete_ver}
Provides: libgcc%{?_isa} = %{version}-%{release}
%endif

%description -n libgcc%{?gccv}
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc%{?gccv}%{?_isa} = %{version}-%{release}
Requires: libstdc++%{?gccv}%{?_isa} = %{version}-%{release}
Requires: libstdc++%{?gccv}-devel%{?_isa} = %{version}-%{release}
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-c++ = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc-c++ < %{version}-%{release}}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
%endif

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++%{?gccv}
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Autoreq: true
Requires: glibc%{?_isa} >= 2.10.90-7
%if 0%{?gccv:1}
Provides: libstdc++ = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: libstdc++ < %{version}-%{release}}
#Obsoletes: libstdc++ < %{hard_obsolete_ver}
Provides: libstdc++%{?_isa} = %{version}-%{release}
%endif

%description -n libstdc++%{?gccv}
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++%{?gccv}-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++%{?gccv}%{?_isa} = %{version}-%{release}
Autoreq: true
%if 0%{?gccv:1}
Provides: libstdc++-devel = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: libstdc++-devel < %{version}-%{release}}
#Obsoletes: libstdc++-devel < %{hard_obsolete_ver}
Provides: libstdc++-devel%{?_isa} = %{version}-%{release}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
%endif

%description -n libstdc++%{?gccv}-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++%{?gccv}-static
Summary: Static libraries for the GNU standard C++ library
Group: Development/Libraries
Requires: libstdc++%{?gccv}-devel%{?_isa} = %{version}-%{release}
Autoreq: true
%if 0%{?gccv:1}
Provides: libstdc++-static = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: libstdc++-static < %{version}-%{release}}
#Obsoletes: libstdc++-static < %{hard_obsolete_ver}
Provides: libstdc++-static%{?_isa} = %{version}-%{release}
%endif

%description -n libstdc++%{?gccv}-static
Static libraries for the GNU standard C++ library.

%package -n libstdc++-docs
Summary: Documentation for the GNU standard C++ library
Group: Development/Libraries
Autoreq: true

%description -n libstdc++-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%if %{build_objc}
%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc%{?gccv}%{?_isa} = %{version}-%{release}
Requires: libobjc%{?gccv}%{?_isa} = %{version}-%{release}
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-objc = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc-objc < %{version}-%{release}}
%endif

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: gcc%{?gccv}-c++%{?_isa} = %{version}-%{release}
Requires: gcc%{?gccv}-objc%{?_isa} = %{version}-%{release}
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-objc++ = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc-objc++ < %{version}-%{release}}
%endif

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc%{?gccv}
Summary: Objective-C runtime
Group: System Environment/Libraries
Autoreq: true
%if 0%{?gccv:1}
Provides: libobjc = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: libobjc < %{version}-%{release}}
Provides: libobjc%{?_isa} = %{version}-%{release}
%endif

%description -n libobjc%{?gccv}
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%endif # build_objc

%package gfortran
Summary: Fortran support
Group: Development/Languages
Requires: gcc%{?gccv}%{?_isa} = %{version}-%{release}
# rely on automatic rpm dependencies
#Requires: libgfortran >= %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath%{?gccv}-devel%{?_isa} = %{version}-%{release}
%endif
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-gfortran = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc-gfortran < %{version}-%{release}}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
%endif

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Group: System Environment/Libraries
Autoreq: true
%if %{build_libquadmath}
Requires: %{_prefix}/%{_lib}/libquadmath.so.%{libquadmath_ver}
%endif

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%if ! 0%{?gccv:1}
%package -n libgfortran-static
Summary: Static Fortran libraries
Group: Development/Libraries
Requires: gcc%{?gccv}%{?_isa} = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath%{?gccv}-static%{?_isa} = %{version}-%{release}
%endif

%description -n libgfortran-static
This package contains static Fortran libraries.
%endif

%package -n libgomp
Summary: GCC OpenMP v3.0 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v3.0 support.

%package -n libmudflap
Summary: GCC mudflap shared support library
Group: System Environment/Libraries

%description -n libmudflap
This package contains GCC shared support library which is needed
for mudflap support.

%package -n libmudflap%{?gccv}-devel
Summary: GCC mudflap support
Group: Development/Libraries
Requires: libmudflap%{?_isa} >= %{version}-%{release}
Requires: gcc%{?gccv}%{?_isa} = %{version}-%{release}
%if 0%{?gccv:1}
Provides: libmudflap-devel = %{version}-%{release}
%endif

%description -n libmudflap%{?gccv}-devel
This package contains headers for building mudflap-instrumented programs.

To instrument a non-threaded program, add -fmudflap
option to GCC and when linking add -lmudflap, for threaded programs
also add -fmudflapth and -lmudflapth.

%package -n libmudflap%{?gccv}-static
Summary: Static libraries for mudflap support
Group: Development/Libraries
Requires: libmudflap%{?gccv}-devel%{?_isa} = %{version}-%{release}
%if 0%{?gccv:1}
Provides: libmudflap-static = %{version}-%{release}
%endif

%description -n libmudflap%{?gccv}-static
This package contains static libraries for building mudflap-instrumented
programs.

%package -n libquadmath
Summary: GCC __float128 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n libquadmath%{?gccv}-devel
Summary: GCC __float128 support
Group: Development/Libraries
Requires: %{_prefix}/%{_lib}/libquadmath.so.%{libquadmath_ver}
%if 0%{?gccv:1}
Provides: libquadmath-devel = %{version}-%{release}
Obsoletes: libquadmath-devel <= %{version}
%endif

%description -n libquadmath%{?gccv}-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libquadmath%{?gccv}-static
Summary: Static libraries for __float128 support
Group: Development/Libraries
Requires: libquadmath%{?gccv}-devel%{?_isa} = %{version}-%{release}
%if 0%{?gccv:1}
Provides: libquadmath-static = %{version}-%{release}
Obsoletes: libquadmath-static <= %{version}
%endif

%description -n libquadmath%{?gccv}-static
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%package -n libitm
Summary: The GNU Transactional Memory library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libitm%{?gccv}-devel
Summary: The GNU Transactional Memory support
Group: Development/Libraries
#Requires: libitm = %{version}-%{release}
Requires: %{_prefix}/%{_lib}/libitm.so.%{libitm_ver}
%if 0%{?gccv:1}
Provides: libitm-devel = %{version}-%{release}
%endif

%description -n libitm%{?gccv}-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package -n libitm%{?gccv}-static
Summary: The GNU Transactional Memory static library
Group: Development/Libraries
Requires: libitm%{?gccv}-devel%{?_isa} = %{version}-%{release}
%if 0%{?gccv:1}
Provides: libitm-static = %{version}-%{release}
%endif

%description -n libitm%{?gccv}-static
This package contains GNU Transactional Memory static libraries.

%package -n libatomic
Summary: The GNU Atomic library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n libatomic%{?gccv}-static
Summary: The GNU Atomic static library
Group: Development/Libraries
Requires: libatomic = %{version}-%{release}
%if 0%{?gccv:1}
Provides: libatomic-static = %{version}-%{release}
%endif

%description -n libatomic%{?gccv}-static
This package contains GNU Atomic static libraries.

%package -n libasan
Summary: The Address Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libasan
This package contains the Address Sanitizer library
which is used for -fsanitize=address instrumented programs.

%package -n libasan%{?gccv}-static
Summary: The Address Sanitizer static library
Group: Development/Libraries
Requires: libasan = %{version}-%{release}
%if 0%{?gccv:1}
Provides: libasan-static = %{version}-%{release}
%endif

%description -n libasan%{?gccv}-static
This package contains Address Sanitizer static runtime library.

%package -n libtsan
Summary: The Thread Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libtsan
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

%package -n libtsan%{?gccv}-static
Summary: The Thread Sanitizer static library
Group: Development/Libraries
Requires: libtsan = %{version}-%{release}
%if 0%{?gccv:1}
Provides: libtsan-static = %{version}-%{release}
%endif

%description -n libtsan%{?gccv}-static
This package contains Thread Sanitizer static runtime library.

%package java
Summary: Java support for GCC
Group: Development/Languages
Requires: gcc%{?gccv} = %{version}-%{release}
Requires: libgcj = %{version}-%{release}
Requires: libgcj-devel = %{version}-%{release}
Requires: /usr/share/java/eclipse-ecj.jar
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description java
This package adds support for compiling Java(tm) programs and
bytecode into native code.

%package -n libgcj
Summary: Java runtime library for gcc
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: zip >= 2.1
Requires: gtk2 >= 2.4.0
Requires: glib2 >= 2.4.0
Requires: libart_lgpl >= 2.1.0
%if %{build_java}
BuildRequires: gtk2-devel >= 2.4.0
BuildRequires: glib2-devel >= 2.4.0
BuildRequires: libart_lgpl-devel >= 2.1.0
BuildRequires: alsa-lib-devel
BuildRequires: libXtst-devel
BuildRequires: libXt-devel
%endif
Autoreq: true

%description -n libgcj
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%package -n libgcj-devel
Summary: Libraries for Java development using GCC
Group: Development/Languages
Requires: libgcj%{?_isa} = %{version}-%{release}
Requires: zlib-devel%{?_isa}
Requires: /bin/awk
Autoreq: false
Autoprov: false

%description -n libgcj-devel
The Java(tm) static libraries and C header files. You will need this
package to compile your Java programs using the GCC Java compiler (gcj).

%package -n libgcj-src
Summary: Java library sources from GCC4 preview
Group: System Environment/Libraries
Requires: libgcj = %{version}-%{release}
Autoreq: true

%description -n libgcj-src
The Java(tm) runtime library sources for use in Eclipse.

%package -n cpp%{?gccv}
Summary: The C Preprocessor
Group: Development/Languages
#Requires: filesystem >= 3
Provides: /lib/cpp
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true
%if 0%{?gccv:1}
Provides: cpp = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: cpp < %{version}-%{release}}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
%endif

%description -n cpp%{?gccv}
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package gnat
Summary: Ada 95 support for GCC
Group: Development/Languages
Requires: gcc%{?gccv}%{?_isa} = %{version}-%{release}
Requires: libgnat%{?gccv}%{?_isa} = %{version}-%{release}
Requires: libgnat%{?gccv}-devel%{?_isa} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-gnat = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc-gnat < %{version}-%{release}}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
%endif

%description gnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes development tools,
the documents and Ada 95 compiler.

%package -n libgnat%{?gccv}
Summary: GNU Ada 95 runtime shared libraries
Group: System Environment/Libraries
Autoreq: true
%if 0%{?gccv:1}
Provides: libgnat = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: libgnat < %{version}-%{release}}
Provides: libgnat%{?_isa} = %{version}-%{release}
%endif

%description -n libgnat%{?gccv}
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared libraries,
which are required to run programs compiled with the GNAT.

%package -n libgnat%{?gccv}-devel
Summary: GNU Ada 95 libraries
Group: Development/Languages
Autoreq: true
%if 0%{?gccv:1}
Provides: libgnat-devel = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: libgnat-devel < %{version}-%{release}}
Provides: libgnat-devel%{?_isa} = %{version}-%{release}
%endif

%description -n libgnat%{?gccv}-devel
GNAT is a GNU Ada 95 front-end to GCC. This package includes libraries,
which are required to compile with the GNAT.

%package -n libgnat%{?gccv}-static
Summary: GNU Ada 95 static libraries
Group: Development/Languages
Requires: libgnat%{?gccv}-devel%{?_isa} = %{version}-%{release}
Autoreq: true
%if 0%{?gccv:1}
Provides: libgnat-static = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: libgnat-static < %{version}-%{release}}
Provides: libgnat-static%{?_isa} = %{version}-%{release}
%endif

%description -n libgnat%{?gccv}-static
GNAT is a GNU Ada 95 front-end to GCC. This package includes static libraries.

%package go
Summary: Go support
Group: Development/Languages
Requires: gcc%{?gccv}%{?_isa} = %{version}-%{release}
Requires: libgo%{?gccv}-devel%{?_isa} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-go = %{version}-%{release}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
%endif

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%package -n libgo
Summary: Go runtime
Group: System Environment/Libraries
Autoreq: true
%if 0%{?gccv:1}
Provides: libgo = %{version}-%{release}
Provides: libgo%{?_isa} = %{version}-%{release}
%endif

%description -n libgo
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%package -n libgo%{?gccv}-devel
Summary: Go development libraries
Group: Development/Languages
Requires: %{_prefix}/%{_lib}/libgo.so.%{libgo_ver}
Autoreq: true
%if 0%{?gccv:1}
Provides: libgo-devel = %{version}-%{release}
Provides: libgo-devel%{?_isa} = %{version}-%{release}
%endif

%description -n libgo%{?gccv}-devel
This package includes libraries and support files for compiling
Go programs.

%package -n libgo%{?gccv}-static
Summary: Static Go libraries
Group: Development/Libraries
Requires: gcc%{?gccv}%{?_isa} = %{version}-%{release}
%if 0%{?gccv:1}
Provides: libgo-static = %{version}-%{release}
Provides: libgo-static%{?_isa} = %{version}-%{release}
%endif

%description -n libgo%{?gccv}-static
This package contains static Go libraries.

%package plugin-devel
Summary: Support for compiling GCC plugins
Group: Development/Languages
Requires: gcc%{?gccv} = %{version}-%{release}
Requires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1

%description plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%if 0%{?_enable_debug_packages}
%define debug_package %{nil}
%global __debug_package 1
%global __debug_install_post \
   %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/gcc-%{version}-%{DATE}"\
    %{_builddir}/gcc-%{version}-%{DATE}/split-debuginfo.sh\
%{nil}

%package debuginfo
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: 0
Requires: gcc%{?gccv}-base-debuginfo%{?_isa} = %{version}-%{release}
%if 0%{?gccv:1}
Provides: gcc-debuginfo = %{version}-%{release}
%endif

%description debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%files debuginfo -f debugfiles.list
%defattr(-,root,root)

%package base-debuginfo
Summary: Debug information for libraries from package %{name}
Group: Development/Debug
AutoReqProv: 0
%if 0%{?gccv:1}
Provides: gcc-base-debuginfo = %{version}-%{release}
%endif

%description base-debuginfo
This package provides debug information for libgcc_s, libgomp and
libstdc++ libraries from package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%files base-debuginfo -f debugfiles-base.list
%defattr(-,root,root)
%endif

%prep
%setup -q -n gcc-%{version}-%{DATE} -a 1 -a 2
%patch0 -p0 -b .hack~
%patch1 -p0 -b .java-nomulti~
%patch2 -p0 -b .ppc32-retaddr~
%patch3 -p0 -b .rh330771~
%patch4 -p0 -b .i386-libgomp~
%patch5 -p0 -b .sparc-config-detection~
%patch6 -p0 -b .libgomp-omp_h-multilib~
%patch7 -p0 -b .libtool-no-rpath~
%if %{build_cloog}
%patch8 -p0 -b .cloog-dl~
%patch9 -p0 -b .cloog-dl2~
%endif
%patch10 -p0 -b .pr38757~
%if %{build_libstdcxx_docs}
%patch11 -p0 -b .libstdc++-docs~
%endif
%patch12 -p0 -b .no-add-needed~
%patch13 -p0 -b .pr56564~
%patch14 -p0 -b .pr56493~
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
%patch15 -p0 -b .color-auto~
%endif
%patch16 -p0 -b .pr58956~

%if 0%{?_enable_debug_packages}
cat > split-debuginfo.sh <<\EOF
#!/bin/sh
BUILDDIR="%{_builddir}/gcc-%{version}-%{DATE}"
if [ -f "${BUILDDIR}"/debugfiles.list \
     -a -f "${BUILDDIR}"/debuglinks.list ]; then
  > "${BUILDDIR}"/debugsources-base.list
  > "${BUILDDIR}"/debugfiles-base.list
  cd "${RPM_BUILD_ROOT}"
  for f in `find usr/lib/debug -name \*.debug \
	    | egrep 'lib[0-9]*/lib(gcc|gomp|stdc|quadmath|itm)'`; do
    echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
    if [ -f "$f" -a ! -L "$f" ]; then
      cp -a "$f" "${BUILDDIR}"/test.debug
      /usr/lib/rpm/debugedit -b "${RPM_BUILD_DIR}" -d /usr/src/debug \
			     -l "${BUILDDIR}"/debugsources-base.list \
			     "${BUILDDIR}"/test.debug
      rm -f "${BUILDDIR}"/test.debug
    fi
  done
  for f in `find usr/lib/debug/.build-id -type l`; do
    ls -l "$f" | egrep -q -- '->.*lib[0-9]*/lib(gcc|gomp|stdc|quadmath|itm)' \
      && echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
  done
  grep -v -f "${BUILDDIR}"/debugfiles-base.list \
    "${BUILDDIR}"/debugfiles.list > "${BUILDDIR}"/debugfiles.list.new
  mv -f "${BUILDDIR}"/debugfiles.list.new "${BUILDDIR}"/debugfiles.list
  for f in `LC_ALL=C sort -z -u "${BUILDDIR}"/debugsources-base.list \
	    | grep -E -v -z '(<internal>|<built-in>)$' \
	    | xargs --no-run-if-empty -n 1 -0 echo \
	    | sed 's,^,usr/src/debug/,'`; do
    if [ -f "$f" ]; then
      echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
      echo "%%exclude /$f" >> "${BUILDDIR}"/debugfiles.list
    fi
  done
  mv -f "${BUILDDIR}"/debugfiles-base.list{,.old}
  echo "%%dir /usr/lib/debug" > "${BUILDDIR}"/debugfiles-base.list
  awk 'BEGIN{FS="/"}(NF>4&&$NF){d="%%dir /"$2"/"$3"/"$4;for(i=5;i<NF;i++){d=d"/"$i;if(!v[d]){v[d]=1;print d}}}' \
    "${BUILDDIR}"/debugfiles-base.list.old >> "${BUILDDIR}"/debugfiles-base.list
  cat "${BUILDDIR}"/debugfiles-base.list.old >> "${BUILDDIR}"/debugfiles-base.list
  rm -f "${BUILDDIR}"/debugfiles-base.list.old
fi
EOF
chmod 755 split-debuginfo.sh
%endif

# This testcase doesn't compile.
rm libjava/testsuite/libjava.lang/PR35020*

tar xzf %{SOURCE4}

%patch1000 -p0 -b .fastjar-0.97-segfault~
%patch1001 -p0 -b .fastjar-0.97-len1~
%patch1002 -p0 -b .fastjar-0.97-filename0~
%patch1003 -p0 -b .fastjar-CVE-2010-0831~
%patch1004 -p0 -b .fastjar-man~
%patch1005 -p0 -b .fastjar-0.97-aarch64-config~

%if %{bootstrap_java}
tar xjf %{SOURCE10}
%endif

%patch1100 -p0 -b .isl-aarch64~

sed -i -e 's/4\.8\.3/4.8.2/' gcc/BASE-VER
echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
# Default to -gdwarf-4 -fno-debug-types-section rather than -gdwarf-2
sed -i '/UInteger Var(dwarf_version)/s/Init(2)/Init(4)/' gcc/common.opt
sed -i '/flag_debug_types_section/s/Init(1)/Init(0)/' gcc/common.opt
sed -i '/dwarf_record_gcc_switches/s/Init(0)/Init(1)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)2\./\14./' gcc/doc/invoke.texi
%else
# Default to -gdwarf-3 rather than -gdwarf-2
sed -i '/UInteger Var(dwarf_version)/s/Init(2)/Init(3)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)2\./\13./' gcc/doc/invoke.texi
sed -i 's/#define[[:blank:]]*EMIT_ENTRY_VALUE[[:blank:]].*$/#define EMIT_ENTRY_VALUE 0/' gcc/{var-tracking,dwarf2out}.c
sed -i 's/#define[[:blank:]]*EMIT_TYPED_DWARF_STACK[[:blank:]].*$/#define EMIT_TYPED_DWARF_STACK 0/' gcc/dwarf2out.c
sed -i 's/#define[[:blank:]]*EMIT_DEBUG_MACRO[[:blank:]].*$/#define EMIT_DEBUG_MACRO 0/' gcc/dwarf2out.c
%endif

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

# Hack to avoid building multilib libjava
perl -pi -e 's/^all: all-redirect/ifeq (\$(MULTISUBDIR),)\nall: all-redirect\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-redirect/ifeq (\$(MULTISUBDIR),)\ninstall: install-redirect\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-redirect/ifeq (\$(MULTISUBDIR),)\ncheck: check-redirect\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^all: all-recursive/ifeq (\$(MULTISUBDIR),)\nall: all-recursive\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-recursive/ifeq (\$(MULTISUBDIR),)\ninstall: install-recursive\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-recursive/ifeq (\$(MULTISUBDIR),)\ncheck: check-recursive\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

%build

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

%if %{build_java}
export GCJ_PROPERTIES=jdt.compiler.useSingleThread=true
# gjar isn't usable, so even when GCC source tree no longer includes
# fastjar, build it anyway.
mkdir fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
cd fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
../configure CFLAGS="%{optflags}" --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir}
make %{?_smp_mflags}
export PATH=`pwd`${PATH:+:$PATH}
cd ../../
%endif

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_java}
%if !%{bootstrap_java}
# If we don't have gjavah in $PATH, try to build it with the old gij
mkdir java_hacks
cd java_hacks
cp -a ../../libjava/classpath/tools/external external
mkdir -p gnu/classpath/tools
cp -a ../../libjava/classpath/tools/gnu/classpath/tools/{common,javah,getopt} gnu/classpath/tools/
cp -a ../../libjava/classpath/tools/resource/gnu/classpath/tools/common/messages.properties gnu/classpath/tools/common
cp -a ../../libjava/classpath/tools/resource/gnu/classpath/tools/getopt/messages.properties gnu/classpath/tools/getopt
cd external/asm; for i in `find . -name \*.java`; do gcj --encoding ISO-8859-1 -C $i -I.; done; cd ../..
for i in `find gnu -name \*.java`; do gcj -C $i -I. -Iexternal/asm/; done
gcj -findirect-dispatch -O2 -fmain=gnu.classpath.tools.javah.Main -I. -Iexternal/asm/ `find . -name \*.class` -o gjavah.real
cat > gjavah <<EOF
#!/bin/sh
export CLASSPATH=`pwd`${CLASSPATH:+:$CLASSPATH}
exec `pwd`/gjavah.real "\$@"
EOF
chmod +x `pwd`/gjavah
cat > ecj1 <<EOF
#!/bin/sh
exec gij -cp /usr/share/java/eclipse-ecj.jar org.eclipse.jdt.internal.compiler.batch.GCCMain "\$@"
EOF
chmod +x `pwd`/ecj1
export PATH=`pwd`${PATH:+:$PATH}
cd ..
%endif
%endif

%if %{build_cloog}
mkdir isl-build isl-install
%ifarch s390 s390x
ISL_FLAG_PIC=-fPIC
%else
ISL_FLAG_PIC=-fpic
%endif
cd isl-build
../../isl-%{isl_version}/configure --disable-shared \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags} $ISL_FLAG_PIC" --prefix=`cd ..; pwd`/isl-install
make %{?_smp_mflags}
make install
cd ..

mkdir cloog-build cloog-install
cd cloog-build
cat >> ../../cloog-%{cloog_version}/source/isl/constraints.c << \EOF
#include <isl/flow.h>
static void __attribute__((used)) *s1 = (void *) isl_union_map_compute_flow;
static void __attribute__((used)) *s2 = (void *) isl_map_dump;
EOF
sed -i 's|libcloog|libgcc48privatecloog|g' \
  ../../cloog-%{cloog_version}/{,test/}Makefile.{am,in}
isl_prefix=`cd ../isl-install; pwd` \
../../cloog-%{cloog_version}/configure --with-isl=system \
  --with-isl-prefix=`cd ../isl-install; pwd` \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
   --prefix=`cd ..; pwd`/cloog-install
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
make %{?_smp_mflags} install
cd ../cloog-install/lib
rm libgcc48privatecloog-isl.so{,.4}
mv libgcc48privatecloog-isl.so.4.0.0 libcloog-isl.so.4
ln -sf libcloog-isl.so.4 libcloog-isl.so
ln -sf libcloog-isl.so.4 libcloog.so
cd ../..
%endif

CC=gcc
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
%endif
%ifarch ppc64
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
fi
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables/' \
      ../gcc/Makefile.in
    ;;
esac
enablelgo=
enablelada=
enablefortran=
enablejava=
enableobjc=
%if %{build_ada}
enablelada=,ada
%endif
%if %{build_go}
enablelgo=,go
%endif
%if %{build_java}
enablejava=,java
%endif
%if %{build_fortran}
enablefortran=,fortran
%endif
%if %{build_objc}
enableobjc=,objc,obj-c++
%endif
CC="$CC" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object --enable-linker-build-id --with-linker-hash-style=gnu \
	--enable-languages=c,c++${enableobjc}${enablejava}${enablefortran}${enablelada}${enablelgo},lto \
	--enable-plugin --enable-initfini-array \
%if !%{build_java}
	--disable-libgcj \
%else
	--enable-java-awt=gtk --disable-dssi \
	--with-java-home=%{_prefix}/lib/jvm/java-1.5.0-gcj-1.5.0.0/jre \
	--enable-libgcj-multifile \
%if !%{bootstrap_java}
	--enable-java-maintainer-mode \
%endif
	--with-ecj-jar=/usr/share/java/eclipse-ecj.jar \
	--disable-libjava-multilib \
%endif #buildjava
%if %{build_cloog}
	--with-isl=`pwd`/isl-install --with-cloog=`pwd`/cloog-install \
%else
	--without-isl --without-cloog \
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc ppc64
%if 0%{?rhel} >= 7
	--with-cpu-32=power7 --with-tune-32=power7 --with-cpu-64=power7 --with-tune-64=power7 \
%endif
%if 0%{?rhel} == 6
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%if 0%{?rhel} >= 7
%ifarch %{ix86}
	--with-arch=x86-64 \
%endif
%ifarch x86_64
	--with-arch_32=x86-64 \
%endif
%else
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
%endif
%ifarch s390 s390x
%if 0%{?rhel} >= 7
	--with-arch=z10 --with-tune=zEC12 --enable-decimal-float \
%else
	--with-arch=z9-109 --with-tune=z10 --enable-decimal-float \
%endif
%endif
%ifarch armv7hl
	--with-cpu=cortex-a8 --with-tune=cortex-a8 --with-arch=armv7-a \
	--with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform}
%endif

%ifarch %{arm} sparc sparcv9 sparc64
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
%else
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
%endif

%if %{build_cloog}
cp -a cloog-install/lib/libcloog-isl.so.4 gcc/
%endif

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc
mkdir -p rpm.doc/boehm-gc rpm.doc/fastjar rpm.doc/libffi rpm.doc/libjava
mkdir -p rpm.doc/go rpm.doc/libgo rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp,libatomic,libsanitizer}

for i in {gcc,gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp,libatomic,libsanitizer}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
(cd boehm-gc; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/boehm-gc/$i.gc
done)
(cd fastjar-%{fastjar_ver}; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/fastjar/$i.fastjar
done)
(cd libffi; for i in ChangeLog* README* LICENSE; do
	cp -p $i ../rpm.doc/libffi/$i.libffi
done)
(cd libjava; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/libjava/$i.libjava
done)
cp -p libjava/LIBGCJ_LICENSE rpm.doc/libjava/
%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif
%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif
%if %{build_go}
(cd gcc/go; for i in README* ChangeLog*; do
	cp -p $i ../../rpm.doc/go/$i
done)
(cd libgo; for i in LICENSE* PATENTS* README; do
	cp -p $i ../rpm.doc/libgo/$i.libgo
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%if %{build_java_tar}
find libjava -name \*.h -type f | xargs grep -l '// DO NOT EDIT THIS FILE - it is machine generated' > libjava-classes.list
find libjava -name \*.class -type f >> libjava-classes.list
find libjava/testsuite -name \*.jar -type f >> libjava-classes.list
tar cf - -T libjava-classes.list | bzip2 -9 > $RPM_SOURCE_DIR/libjava-classes-%{version}-%{release}.tar.bz2
%endif

%install
rm -fr %{buildroot}

cd obj-%{gcc_target_platform}

%if %{build_java}
export GCJ_PROPERTIES=jdt.compiler.useSingleThread=true
export PATH=`pwd`/../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}${PATH:+:$PATH}
%if !%{bootstrap_java}
export PATH=`pwd`/java_hacks${PATH:+:$PATH}
%endif
%endif

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
%if %{build_java}
make DESTDIR=%{buildroot} -C %{gcc_target_platform}/libjava install-src.zip
%endif
%if %{build_ada}
chmod 644 %{buildroot}%{_infodir}/gnat*
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}

%if %{build_cloog}
cp -a cloog-install/lib/libcloog-isl.so.4 $FULLPATH/
%endif

# xxx: these are now handled by the alternatives setup
# fix some things
#ln -sf gcc %{buildroot}%{_prefix}/bin/cc
#rm -f %{buildroot}%{_prefix}/lib/cpp
#ln -sf ../bin/cpp %{buildroot}/%{_prefix}/lib/cpp
#ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
rm -f %{buildroot}%{_infodir}/dir
%if %{build_ada}
# target will be renamed to a gccv-base suffix if needed later on in this sspec file
ln -sf gcc%{?gccv} %{buildroot}%{_prefix}/bin/gnatgcc
%endif

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/*.h.gch dirs
# 1) there is no bits/*.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}/man3
cp -r -p $libstdcxx_doc_builddir/man/man3/* %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

%ifarch sparcv9 ppc
FULLLPATH=$FULLPATH/lib32
%endif
%ifarch sparc64 ppc64
FULLLPATH=$FULLPATH/lib64
%endif
if [ -n "$FULLLPATH" ]; then
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f
%if %{build_java}
# gcj -static doesn't work properly anyway, unless using --whole-archive
# and saving 35MB is not bad.
find %{buildroot} -name libgcj.a -o -name libgtkpeer.a \
		     -o -name libgjsmalsa.a -o -name libgcj-tools.a -o -name libjvm.a \
		     -o -name libgij.a -o -name libgcj_bc.a -o -name libjavamath.a \
  | xargs rm -f

mv %{buildroot}%{_prefix}/lib/libgcj.spec $FULLPATH/
sed -i -e 's/lib: /&%%{static:%%eJava programs cannot be linked statically}/' \
  $FULLPATH/libgcj.spec
%endif

%if %{build_fortran}
mv %{buildroot}%{_prefix}/%{_lib}/libgfortran.spec $FULLPATH/
%endif
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_version}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1 $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
%ifarch ppc
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif
%ifarch ppc64
rm -f $FULLPATH/32/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%endif
%ifarch %{arm}
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-littlearm)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so %{buildroot}%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -dD -xc /dev/null | grep __LONG_MAX__.*2147483647; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

%if %{build_java}
pushd ../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
make install DESTDIR=%{buildroot}
popd

if [ "%{_lib}" != "lib" ]; then
  mkdir -p %{buildroot}%{_prefix}/%{_lib}/pkgconfig
  sed '/^libdir/s/lib$/%{_lib}/' %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-*.pc \
    > %{buildroot}%{_prefix}/%{_lib}/pkgconfig/`basename %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-*.pc`
fi
%endif

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
pushd ../libstdc++-v3/python
for i in `find . -name \*.py`; do
  touch -r $i %{buildroot}%{_prefix}/share/gcc-%{gcc_version}/python/$i
done
touch -r hook.in %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc++*gdb.py
popd

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
%if %{build_objc}
ln -sf ../../../libobjc.so.4 libobjc.so
%endif
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
%if %{build_fortran}
ln -sf ../../../libgfortran.so.3.* libgfortran.so
%endif
ln -sf ../../../libgomp.so.1.* libgomp.so
ln -sf ../../../libmudflap.so.0.* libmudflap.so
ln -sf ../../../libmudflapth.so.0.* libmudflapth.so
%if %{build_go}
ln -sf ../../../libgo.so.4.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libitm}
ln -sf ../../../libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../libasan.so.0.* libasan.so
mv ../../../libasan_preinit.o libasan_preinit.o
%endif
%if %{build_java}
ln -sf ../../../libgcj.so.14.* libgcj.so
ln -sf ../../../libgcj-tools.so.14.* libgcj-tools.so
ln -sf ../../../libgij.so.14.* libgij.so
%endif
else
%if %{build_objc}
ln -sf ../../../../%{_lib}/libobjc.so.4 libobjc.so
%endif
ln -sf ../../../../%{_lib}/libstdc++.so.6.*[0-9] libstdc++.so
%if %{build_fortran}
ln -sf ../../../../%{_lib}/libgfortran.so.3.* libgfortran.so
%endif
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
ln -sf ../../../../%{_lib}/libmudflap.so.0.* libmudflap.so
ln -sf ../../../../%{_lib}/libmudflapth.so.0.* libmudflapth.so
%if %{build_go}
ln -sf ../../../../%{_lib}/libgo.so.4.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../../%{_lib}/libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libitm}
ln -sf ../../../../%{_lib}/libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../../%{_lib}/libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../../%{_lib}/libasan.so.0.* libasan.so
mv ../../../../%{_lib}/libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libtsan}
rm -f libtsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/libtsan.so.0.* | sed 's,^.*libt,libt,'`' )' > libtsan.so
%endif
%if %{build_java}
ln -sf ../../../../%{_lib}/libgcj.so.14.* libgcj.so
ln -sf ../../../../%{_lib}/libgcj-tools.so.14.* libgcj-tools.so
ln -sf ../../../../%{_lib}/libgij.so.14.* libgij.so
%endif
fi
%if %{build_java}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcj_bc.so $FULLLPATH/
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a $FULLLPATH/
%if %{build_fortran}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a $FULLLPATH/
%endif
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libmudflap{,th}.*a $FULLLPATH/
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_prefix}/%{_lib}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libasan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan.*a $FULLLPATH/
%endif
%if %{build_libtsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLLPATH/
%endif
%if %{build_go}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgo.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgobegin.*a $FULLLPATH/
%endif

%if %{build_ada}
%ifarch sparcv9 ppc
rm -rf $FULLPATH/64/ada{include,lib}
%endif
%ifarch %{multilib_64_archs}
rm -rf $FULLPATH/32/ada{include,lib}
%endif
if [ "$FULLPATH" != "$FULLLPATH" ]; then
mv -f $FULLPATH/ada{include,lib} $FULLLPATH/
pushd $FULLLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../../libgnarl-*.so libgnarl-4.8.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-4.8.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-4.8.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-4.8.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-4.8.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-4.8.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-4.8.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-4.8.so
fi
popd
fi
%endif

%ifarch sparcv9 ppc
%if %{build_objc}
ln -sf ../../../../../lib64/libobjc.so.4 64/libobjc.so
%endif
ln -sf ../`echo ../../../../lib/libstdc++.so.6.*[0-9] | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.3.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
rm -f libmudflap.so libmudflapth.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflap.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflapth.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > 64/libmudflap.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > 64/libmudflapth.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgo.so.4.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgo.so.4.* | sed 's,^.*libg,libg,'`' )' > 64/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 64/libquadmath.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 64/libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 64/libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libasan.so.0.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libasan.so.0.* | sed 's,^.*liba,liba,'`' )' > 64/libasan.so
mv ../../../../lib64/libasan_preinit.o 64/libasan_preinit.o
%endif
%if %{build_java}
ln -sf ../`echo ../../../../lib/libgcj.so.14.* | sed s~/lib/~/lib64/~` 64/libgcj.so
ln -sf ../`echo ../../../../lib/libgcj-tools.so.14.* | sed s~/lib/~/lib64/~` 64/libgcj-tools.so
ln -sf ../`echo ../../../../lib/libgij.so.14.* | sed s~/lib/~/lib64/~` 64/libgij.so
ln -sf lib32/libgcj_bc.so libgcj_bc.so
ln -sf ../lib64/libgcj_bc.so 64/libgcj_bc.so
%endif
%if %{build_fortran}
ln -sf lib32/libgfortran.a libgfortran.a
ln -sf ../lib64/libgfortran.a 64/libgfortran.a
%endif
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/lib64/libobjc.*a 64/
%endif
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libsupc++.a libsupc++.a
ln -sf ../lib64/libsupc++.a 64/libsupc++.a
ln -sf lib32/libmudflap.a libmudflap.a
ln -sf ../lib64/libmudflap.a 64/libmudflap.a
ln -sf lib32/libmudflapth.a libmudflapth.a
ln -sf ../lib64/libmudflapth.a 64/libmudflapth.a
%if %{build_libquadmath}
ln -sf lib32/libquadmath.a libquadmath.a
ln -sf ../lib64/libquadmath.a 64/libquadmath.a
%endif
%if %{build_libitm}
ln -sf lib32/libitm.a libitm.a
ln -sf ../lib64/libitm.a 64/libitm.a
%endif
%if %{build_libatomic}
ln -sf lib32/libatomic.a libatomic.a
ln -sf ../lib64/libatomic.a 64/libatomic.a
%endif
%if %{build_libasan}
ln -sf lib32/libasan.a libasan.a
ln -sf ../lib64/libasan.a 64/libasan.a
%endif
%if %{build_go}
ln -sf lib32/libgo.a libgo.a
ln -sf ../lib64/libgo.a 64/libgo.a
ln -sf lib32/libgobegin.a libgobegin.a
ln -sf ../lib64/libgobegin.a 64/libgobegin.a
%endif
%if %{build_ada}
ln -sf lib32/adainclude adainclude
ln -sf ../lib64/adainclude 64/adainclude
ln -sf lib32/adalib adalib
ln -sf ../lib64/adalib 64/adalib
%endif
%endif # sparcv9 ppc

%ifarch %{multilib_64_archs}
mkdir -p 32
%if %{build_objc}
ln -sf ../../../../libobjc.so.4 32/libobjc.so
%endif
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.*[0-9] | sed s~/../lib64/~/~` 32/libstdc++.so
%if %{build_fortran}
ln -sf ../`echo ../../../../lib64/libgfortran.so.3.* | sed s~/../lib64/~/~` 32/libgfortran.so
%endif
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
rm -f libmudflap.so libmudflapth.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflap.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflapth.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflap.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflapth.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgo.so.4.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgo.so.4.* | sed 's,^.*libg,libg,'`' )' > 32/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 32/libquadmath.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 32/libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 32/libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libasan.so.0.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libasan.so.0.* | sed 's,^.*liba,liba,'`' )' > 32/libasan.so
mv ../../../../lib/libasan_preinit.o 32/libasan_preinit.o
%endif
%if %{build_java}
ln -sf ../`echo ../../../../lib64/libgcj.so.14.* | sed s~/../lib64/~/~` 32/libgcj.so
ln -sf ../`echo ../../../../lib64/libgcj-tools.so.14.* | sed s~/../lib64/~/~` 32/libgcj-tools.so
ln -sf ../`echo ../../../../lib64/libgij.so.14.* | sed s~/../lib64/~/~` 32/libgij.so
%endif
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
%endif
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%endif # multilib_64_archs

%ifarch sparc64 ppc64
ln -sf ../lib32/libgfortran.a 32/libgfortran.a
ln -sf lib64/libgfortran.a libgfortran.a
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libsupc++.a 32/libsupc++.a
ln -sf lib64/libsupc++.a libsupc++.a
ln -sf ../lib32/libmudflap.a 32/libmudflap.a
ln -sf lib64/libmudflap.a libmudflap.a
ln -sf ../lib32/libmudflapth.a 32/libmudflapth.a
ln -sf lib64/libmudflapth.a libmudflapth.a
%if %{build_libquadmath}
ln -sf ../lib32/libquadmath.a 32/libquadmath.a
ln -sf lib64/libquadmath.a libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../lib32/libitm.a 32/libitm.a
ln -sf lib64/libitm.a libitm.a
%endif
%if %{build_libatomic}
ln -sf ../lib32/libatomic.a 32/libatomic.a
ln -sf lib64/libatomic.a libatomic.a
%endif
%if %{build_libasan}
ln -sf ../lib32/libasan.a 32/libasan.a
ln -sf lib64/libasan.a libasan.a
%endif
%if %{build_go}
ln -sf ../lib32/libgo.a 32/libgo.a
ln -sf lib64/libgo.a libgo.a
ln -sf ../lib32/libgobegin.a 32/libgobegin.a
ln -sf lib64/libgobegin.a libgobegin.a
%endif
%if %{build_java}
ln -sf ../lib32/libgcj_bc.so 32/libgcj_bc.so
ln -sf lib64/libgcj_bc.so libgcj_bc.so
%endif
%if %{build_ada}
ln -sf ../lib32/adainclude 32/adainclude
ln -sf lib64/adainclude adainclude
ln -sf ../lib32/adalib 32/adalib
ln -sf lib64/adalib adalib
%endif

%else # sparc64 ppc64

%ifarch %{multilib_64_archs}
%if %{build_fortran}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgfortran.a 32/libgfortran.a
%endif
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libsupc++.a 32/libsupc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflap.a 32/libmudflap.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflapth.a 32/libmudflapth.a
%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libquadmath.a 32/libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libitm.a 32/libitm.a
%endif
%if %{build_libatomic}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libatomic.a 32/libatomic.a
%endif
%if %{build_libasan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libasan.a 32/libasan.a
%endif
%if %{build_go}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgo.a 32/libgo.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgobegin.a 32/libgobegin.a
%endif
%if %{build_java}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgcj_bc.so 32/libgcj_bc.so
%endif
%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adalib 32/adalib
%endif
%endif # multilib_64_archs

%endif # sparc64 ppc64

## Strip debug info from Fortran/ObjC/Java static libraries
#strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
#		    -o -name libmudflap.a -o -name libmudflapth.a \
#		    -o -name libgcc.a -o -name libgcov.a -o -name libquadmath.a \
#		    -o -name libitm.a -o -name libgo.a -o -name libcaf\*.a \
#		    -o -name libatomic.a -o -name libasan.a -o -name libtsan.a \) \
#		 -a -type f`
popd

%if %{build_fortran}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.3.*
%endif
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmudflap{,th}.so.0.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1.*
%endif
%if %{build_libasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.0.*
%endif
%if %{build_libtsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0.*
%endif
%if %{build_go}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgo.so.4.*
%endif
%if %{build_objc}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.4.*
%endif

%if %{build_ada}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnat*so*
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > %{buildroot}%{_prefix}/bin/%{?gccv:%{name}-}c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec %{name} $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_prefix}/bin/%{?gccv:%{name}-}c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec %{name} $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_prefix}/bin/%{?gccv:%{name}-}c?9

cd ..
%find_lang gcc
%find_lang cpplib
%find_lang libstdc++
# packaging lang files via alternatives is somewhat of a pain, so....
# thou shalt speak english
for p in gcc cpplib libstdc++ ; do
    awk '{printf "%{buildroot}%s\n", $2;}' < $p.lang | xargs -r rm -f
    >$p.lang
done

%if 0%{?gccv:1}
# rename binaries in user directories to avoid conflicts
%if %{build_ada}
for i in %{buildroot}%{_prefix}/bin/gnat* ; do
  mv -f $i ${i}%{gccv}
done
for i in %{buildroot}%{_infodir}/gnat*.info ; do
    sed -i -e "/^START-INFO-DIR-ENTRY/,/^END-INFO-DIR-ENTRY/s|gnat|gnat%{gccv}|gi" $i
    g=${i##*gnat}
    mv $i %{buildroot}%{_infodir}/gnat%{gccv}${g}
done
%endif
%if %{build_fortran}
mv %{buildroot}%{_mandir}/man1/gfortran.1 %{buildroot}%{_mandir}/man1/gfortran%{gccv}.1
mv %{buildroot}%{_infodir}/gfortran.info %{buildroot}%{_infodir}/gfortran%{gccv}.info
%endif
%if %{build_go}
mv %{buildroot}%{_mandir}/man1/gccgo.1 %{buildroot}%{_mandir}/man1/gccgo%{gccv}.1
mv %{buildroot}%{_infodir}/gccgo.info %{buildroot}%{_infodir}/gccgo%{gccv}.info
%endif
for i in $(ls %{buildroot}%{_prefix}/bin/{*gcc,*++,gcov,cpp,*gccgo,*gfortran} 2>/dev/null) ; do
  mv -f $i ${i}%{gccv}
done
for i in $(ls %{buildroot}%{_prefix}/bin/*gcc-{ar,nm,ranlib} 2>/dev/null) ; do
  mv -f $i ${i/gcc-/gcc%{gccv}-}
done
# rename man pages to match: gcc.1* -> gccXX.1*
for i in %{buildroot}%{_mandir}/man1/{gcc,gcov,g++,cpp}.1* ; do
  in="${i%%.1*}"
  mv -f $i ${in}%{gccv}${i##${in}}
done
# rename info files
mv -f %{buildroot}%{_infodir}/cpp.info %{buildroot}%{_infodir}/cpp%{gccv}.info
mv -f %{buildroot}%{_infodir}/cppinternals.info %{buildroot}%{_infodir}/cpp%{gccv}internals.info
mv -f %{buildroot}%{_infodir}/gcc.info %{buildroot}%{_infodir}/gcc%{gccv}.info
mv -f %{buildroot}%{_infodir}/gccint.info %{buildroot}%{_infodir}/gcc%{gccv}int.info
# fix up the info files
for info in gfortran cpp gcc \
%if %{build_go}
            gccgo \
%endif
; do
    sed -i -e "/^START-INFO-DIR-ENTRY/,/^END-INFO-DIR-ENTRY/s|${info}|${info}%{gccv}|gi" %{buildroot}%{_infodir}/${info}%{gccv}.info
done
sed -i -e "/^START-INFO-DIR-ENTRY/,/^END-INFO-DIR-ENTRY/s|g++|g++%{gccv}|g" %{buildroot}%{_infodir}/gcc%{gccv}.info
sed -i -e "/^START-INFO-DIR-ENTRY/,/^END-INFO-DIR-ENTRY/s|cpp|cpp%{gccv}|gi" %{buildroot}%{_infodir}/cpp%{gccv}internals.info
sed -i -e "/^START-INFO-DIR-ENTRY/,/^END-INFO-DIR-ENTRY/s|gcc|gcc%{gccv}|gi" %{buildroot}%{_infodir}/gcc%{gccv}int.info
%endif # gccv binary rename

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
#rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :
#rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gccgo || :
rm -rf $FULLPATH/install-tools $FULLEPATH/install-tools
rm -rf $FULLPATH/include-fixed $FULLPATH/include/ssp
%if !%{build_ada}
rm -f $FULLEPATH/gnat*
%endif
%if 0%{?gccv:1}
rm -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.so{,.?}
rm %{buildroot}/%{_lib}/libgcc_s.so.1 #%{buildroot}/%{_prefix}/%{_lib}/libgcc_s*
rm -f %{buildroot}%{_infodir}/gccinstall*
%if !%{build_java}
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcj || :
#check-me
#rm -f %{buildroot}%{_prefix}/bin/gappletviewer || :
#rm -f %{buildroot}%{_prefix}/bin/{gcj,jcf-dump}
#rm -f %{buildroot}%{_infodir}/gcj*
#rm -f %{buildroot}%{_mandir}/man1/{gcj,jcf-dump,jv-convert,rebuild-gcj-db,aot-compile,gc-analyze,gij,grmic}*
#rm -f $FULLEPATH/{jc1,jvgenmain}
%endif
rm -f %{buildroot}%{_mandir}/man7/*
# the file from the %{_lib} was installed, get rid of the other copy
rm -f %{buildroot}%{_prefix}/lib*/{libgomp,libgfortran,libitm}.spec
# for now we don't expose the .so libs to the general public for these internal shared libs
rm -f %{buildroot}%{_prefix}/%{_lib}/lib{gcc_s,gomp,mudflap,mudflapth,objc,quadmath,stdc++,go,gfortran,itm}.so
%endif #?gccv
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc%{?gccv}-ar || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc%{?gccv}-nm || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc%{?gccv}-ranlib || :

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
rm -f %{buildroot}/lib/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib/go/%{gcc_version}/%{gcc_target_platform}
%ifnarch sparc64 ppc64
ln -sf %{multilib_32_arch}-%{_vendor}-%{_target_os} %{buildroot}%{_prefix}/lib/go/%{gcc_version}/%{gcc_target_platform}
%endif
%endif
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
rm -f %{buildroot}/lib64/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib64/go/%{gcc_version}/%{gcc_target_platform}
%endif
%endif
%endif

%if %{build_java}
mkdir -p %{buildroot}%{_prefix}/share/java/gcj-endorsed \
	 %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
chmod 755 %{buildroot}%{_prefix}/share/java/gcj-endorsed \
	  %{buildroot}%{_prefix}/%{_lib}/gcj-%{version} \
	  %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
touch %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db
%endif

## not shipping ffi.... we have a separate libffi package for this
rm -f $FULLPATH/include/ffi*
rm -f %{buildroot}%{_mandir}/man3/ffi*

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

%check
%if !0%{?_skip_check}
cd obj-%{gcc_target_platform}

%if %{build_java}
export PATH=`pwd`/../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}${PATH:+:$PATH}
%if !%{bootstrap_java}
export PATH=`pwd`/java_hacks${PATH:+:$PATH}
%endif
%endif

# run the tests.
make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ \
%if 0%{?fedora} >= 20
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector-strong}'" || :
%else
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
%endif
echo ====================TESTING=========================
( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
## why was this junk here?! Just to fill build logs with an uuencode dump?!
#tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
#  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}
%endif # _skip_check

%clean
rm -rf %{buildroot}

%post
if [ -f %{_infodir}/gcc%{?gccv}.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gcc%{?gccv}.info.gz || :
fi
%if 0%{?gccv:1}
%{_sbindir}/alternatives --install %{_bindir}/gcc gcc %{_bindir}/gcc%{gccv} %{gcc_prio} \
    --slave %{_bindir}/cc cc %{_bindir}/gcc%{gccv} \
    --slave %{_bindir}/c89 c89 %{_bindir}/gcc%{gccv}-c89 \
    --slave %{_bindir}/c99 c99 %{_bindir}/gcc%{gccv}-c99 \
    --slave %{_bindir}/gcov gcov %{_bindir}/gcov%{gccv} \
    --slave %{_mandir}/man1/gcc.1.gz gcc.1 %{_mandir}/man1/gcc%{gccv}.1.gz \
    --slave %{_mandir}/man1/gcov.1.gz gcov.1 %{_mandir}/man1/gcov%{gccv}.1.gz
%endif

%preun
if [ $1 = 0 ]; then
if [ -f %{_infodir}/gcc%{?gccv}.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcc%{?gccv}.info.gz || :
fi
%if 0%{?gccv:1}
%{_sbindir}/alternatives --remove gcc %{_bindir}/gcc%{gccv}
%endif
fi

%posttrans
%if 0%{?gccv:1}
%{_sbindir}/alternatives --auto gcc
%endif
exit 0

%post -n cpp%{?gccv}
if [ -f %{_infodir}/cpp%{?gccv}.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cpp%{?gccv}.info.gz || :
fi
if [ -f %{_infodir}/cpp%{?gccv}internals.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cpp%{?gccv}internals.info.gz || :
fi
%if 0%{?gccv:1}
%{_sbindir}/alternatives --install %{_bindir}/cpp cpp %{_bindir}/cpp%{gccv} %{gcc_prio} \
    --slave /lib/cpp libcpp %{_bindir}/cpp%{gccv} \
    --slave %{_mandir}/man1/cpp.1.gz cpp.1 %{_mandir}/man1/cpp%{gccv}.1.gz
%endif

%preun -n cpp%{?gccv}
if [ $1 = 0 ] ; then
if [ -f %{_infodir}/cpp%{?gccv}.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cpp%{?gccv}.info.gz || :
fi
%if 0%{?gccv:1}
%{_sbindir}/alternatives --remove cpp %{_bindir}/cpp%{gccv}
%endif
fi

%posttrans -n cpp%{?gccv}
%if 0%{?gccv:1}
%{_sbindir}/alternatives --auto cpp
%endif
exit 0

%post c++
%if 0%{?gccv:1}
%{_sbindir}/alternatives --install %{_bindir}/g++ g++ %{_bindir}/g++%{gccv} %{gcc_prio} \
    --slave %{_bindir}/c++ c++ %{_bindir}/g++%{gccv} \
    --slave %{_mandir}/man1/g++.1.gz g++.1 %{_mandir}/man1/g++%{gccv}.1.gz \
    --slave %{_mandir}/man1/c++.1.gz c++.1 %{_mandir}/man1/g++%{gccv}.1.gz
%endif
exit 0

%preun c++
%if 0%{?gccv:1}
if [ $1 = 0 ] ; then
    %{_sbindir}/alternatives --remove g++ %{_bindir}/g++%{gccv}
fi
%endif
exit 0

%posttrans c++
%if 0%{?gccv:1}
%{_sbindir}/alternatives --auto g++
%endif
exit 0

%post gfortran
if [ -f %{_infodir}/gfortran%{?gccv}.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gfortran%{?gccv}.info.gz || :
fi
%if 0%{?gccv:1}
%{_sbindir}/alternatives --install %{_bindir}/gfortran gfortran %{_bindir}/gfortran%{gccv} %{gcc_prio} \
    --slave %{_bindir}/f95 f95 %{_bindir}/gfortran%{gccv} \
    --slave %{_mandir}/man1/gfortran.1.gz gfortran.1 %{_mandir}/man1/gfortran%{gccv}.1.gz
%endif

%preun gfortran
if [ $1 = 0 ] ; then
if [ -f %{_infodir}/gfortran%{?gccv}.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran%{?gccv}.info.gz || :
fi
%if 0%{?gccv:1}
%{_sbindir}/alternatives --remove gfortran %{_bindir}/gfortran%{gccv}
%endif
fi

%posttrans gfortran
%if 0%{?gccv:1}
%{_sbindir}/alternatives --auto gfortran
%endif
exit 0

%post java
if [ -f %{_infodir}/gcj.info.gz ]; then
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gcj.info.gz || :
fi

%preun java
if [ $1 = 0 -a -f %{_infodir}/gcj.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcj.info.gz || :
fi

%post gnat
if [ -f %{_infodir}/gnat%{?gccv}_rm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat%{?gccv}_rm.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat%{?gccv}_ugn.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat%{?gccv}-style.info.gz || :
fi
%if 0%{?gccv:1}
%{_sbindir}/alternatives --install %{_bindir}/gnat gnat %{_bindir}/gnat%{gccv} %{gcc_prio} \
    --slave %{_bindir}/gnatbind gnatbind %{_bindir}/gnatbind%{gccv} \
    --slave %{_bindir}/gnatchop gnatchop %{_bindir}/gnatchop%{gccv} \
    --slave %{_bindir}/gnatclean gnatclean %{_bindir}/gnatclean%{gccv} \
    --slave %{_bindir}/gnatfind gnatfind %{_bindir}/gnatfind%{gccv} \
    --slave %{_bindir}/gnatgcc gnatgcc %{_bindir}/gnatgcc%{gccv} \
    --slave %{_bindir}/gnatkr gnatkr %{_bindir}/gnatkr%{gccv} \
    --slave %{_bindir}/gnatlink gnatlink %{_bindir}/gnatlink%{gccv} \
    --slave %{_bindir}/gnatls gnatls %{_bindir}/gnatls%{gccv} \
    --slave %{_bindir}/gnatmake gnatmake %{_bindir}/gnatmake%{gccv} \
    --slave %{_bindir}/gnatname gnatname %{_bindir}/gnatname%{gccv} \
    --slave %{_bindir}/gnatprep gnatprep %{_bindir}/gnatprep%{gccv} \
    --slave %{_bindir}/gnatxref gnatxref %{_bindir}/gnatxref%{gccv}
%endif

%preun gnat
if [ $1 = 0 ] ; then
if [ -f %{_infodir}/gnat%{?gccv}_rm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat%{?gccv}_rm.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat%{?gccv}_ugn.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat%{?gccv}-style.info.gz || :
fi
%if 0%{?gccv:1}
%{_sbindir}/alternatives --remove gnat %{_bindir}/gnat%{gccv}
%endif
fi

%posttrans gnat
%if 0%{?gccv:1}
%{_sbindir}/alternatives --auto gnat
%endif
exit 0

# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc%{?gccv} -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%postun -n libgcc%{?gccv} -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%triggerpostun -n libgcc%{?gccv} -p <lua> -- libgcc < %{hard_obsolete_ver}
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%post -n libstdc++%{?gccv} -p /sbin/ldconfig

%postun -n libstdc++%{?gccv} -p /sbin/ldconfig

%triggerpostun -n libstdc++%{?gccv} -- libstdc++ < %{hard_obsolete_ver}
/sbin/ldconfig
exit 0

%if 0%{?gccv:1}
%post -n libstdc++%{?gccv}-devel
%{_sbindir}/alternatives --install %{_libdir}/libstdc++.so libstdc++.so %{_libdir}/libstdc++.so.%{libstdcplusplus_ver} %{gcc_prio}

%preun -n libstdc++%{?gccv}-devel
if [ $1 = 0 ] ; then
    %{_sbindir}/alternatives --remove libstdc++.so %{_libdir}/libstdc++.so.%{libstdcplusplus_ver}
fi
exit 0

%posttrans -n libstdc++%{?gccv}-devel
%{_sbindir}/alternatives --auto libstdc++.so
exit 0
%endif # ?gccv

%if %{build_objc}
%post -n libobjc%{?gccv} -p /sbin/ldconfig

%postun -n libobjc%{?gccv} -p /sbin/ldconfig
%endif

%if %{build_java}
%post -n libgcj
/sbin/ldconfig
if [ -f %{_infodir}/cp-tools.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cp-tools.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz || :
fi

%preun -n libgcj
if [ $1 = 0 -a -f %{_infodir}/cp-tools.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cp-tools.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz || :
fi

%postun -n libgcj -p /sbin/ldconfig
%endif

%if %{build_fortran}
%post -n libgfortran -p /sbin/ldconfig

%postun -n libgfortran -p /sbin/ldconfig
%endif

%if %{build_ada}
%post -n libgnat%{?gccv} -p /sbin/ldconfig

%postun -n libgnat%{?gccv} -p /sbin/ldconfig
%endif

%post -n libgomp
/sbin/ldconfig
if [ -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%preun -n libgomp
if [ $1 = 0 -a -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%postun -n libgomp -p /sbin/ldconfig

%post -n libmudflap -p /sbin/ldconfig

%postun -n libmudflap -p /sbin/ldconfig

%post -n libquadmath
/sbin/ldconfig
if [ -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%preun -n libquadmath
if [ $1 = 0 -a -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%postun -n libquadmath -p /sbin/ldconfig

%post -n libitm
/sbin/ldconfig
if [ -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%preun -n libitm
if [ $1 = 0 -a -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%postun -n libitm -p /sbin/ldconfig

%post -n libatomic -p /sbin/ldconfig

%postun -n libatomic -p /sbin/ldconfig

%post -n libasan -p /sbin/ldconfig

%postun -n libasan -p /sbin/ldconfig

%post -n libtsan -p /sbin/ldconfig

%postun -n libtsan -p /sbin/ldconfig

%post -n libgo -p /sbin/ldconfig

%postun -n libgo -p /sbin/ldconfig

%post go
if [ -f %{_infodir}/gccgo%{?gccv}.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gccgo%{?gccv}.info.gz || :
fi
%if 0%{?gccv:1}
%{_sbindir}/alternatives --install %{_bindir}/gccgo gccgo %{_bindir}/gccgo%{gccv} %{gcc_prio} \
    --slave %{_mandir}/man1/gccgo.1.gz gccgo.1 %{_mandir}/man1/gccgo%{gccv}.1.gz
%endif

%preun go
if [ $1 = 0 ] ; then
if [ -f %{_infodir}/gccgo%{?gccv}.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gccgo%{?gccv}.info.gz || :
fi
%if 0%{?gccv:1}
%{_sbindir}/alternatives --remove gccgo %{_bindir}/gccgo%{gccv}
%endif
fi

%posttrans go
%if 0%{?gccv:1}
%{_sbindir}/alternatives --auto gccgo
%endif
exit 0

%files -f gcc.lang
%defattr(-,root,root,-)
%{_prefix}/bin/%{?gccv:%{name}-}c89
%{_prefix}/bin/%{?gccv:%{name}-}c99
%{_prefix}/bin/gcc%{?gccv}
%{_prefix}/bin/gcov%{?gccv}

%{_prefix}/bin/gcc%{?gccv}-ar
%{_prefix}/bin/gcc%{?gccv}-nm
%{_prefix}/bin/gcc%{?gccv}-ranlib

%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc%{?gccv}
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc%{?gccv}
%endif
%ifarch ppc64
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc%{?gccv}
%endif
%{_prefix}/bin/%{_target_platform}-gcc%{?gccv}
%{_prefix}/bin/%{_target_platform}-gcc-%{gcc_version}
%{_mandir}/man1/gcc%{?gccv}.1*
%{_mandir}/man1/gcov%{?gccv}.1*
%{_infodir}/gcc%{?gccv}.info*
%{_infodir}/gcc%{?gccv}int.info*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/liblto_plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdnoreturn.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia64intrin.h
%endif
%ifarch ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spe.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/paired.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/vec_types.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmxlintrin.h
%endif
%ifarch %{arm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%endif
%ifarch sparc sparcv9 sparc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/visintrin.h
%endif
%ifarch s390 s390x
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/s390intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmxlintrin.h
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.spec
%endif
%if %{build_cloog}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcloog-isl.so.*
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan_preinit.o
%endif
%endif #sparcv9 ppc
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan_preinit.o
%endif
%endif #%{multilib_64_archs}
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan_preinit.o
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.so
%endif
%else #sparcv9 sparc64 ppc ppc64
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan_preinit.o
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.so
%endif
%endif #sparcv9 sparc64 ppc ppc64
%dir %{_prefix}/libexec/getconf
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* gcc/COPYING* COPYING.RUNTIME

%files -n cpp%{?gccv} -f cpplib.lang
%defattr(-,root,root,-)
%{_prefix}/bin/cpp%{?gccv}
%{_mandir}/man1/cpp%{?gccv}.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1

%files -n libgcc%{?gccv}
%defattr(-,root,root,-)
/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
%if ! 0%{?gccv:1}
/%{_lib}/libgcc_s.so.1
%endif
%doc gcc/COPYING* COPYING.RUNTIME

%files c++
%defattr(-,root,root,-)
%{_prefix}/bin/%{gcc_target_platform}-*++%{?gccv}
%{_prefix}/bin/g++%{?gccv}
%{_prefix}/bin/c++%{?gccv}
%{_mandir}/man1/g++%{?gccv}.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++%{?gccv} -f libstdc++.lang
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libstdc++.so.6.*
%if ! 0%{?gccv:1}
%{_prefix}/%{_lib}/libstdc++.so.6
%endif
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%dir %{_prefix}/share/gcc-%{gcc_version}
%dir %{_prefix}/share/gcc-%{gcc_version}/python
%{_prefix}/share/gcc-%{gcc_version}/python/libstdcxx

%files -n libstdc++%{?gccv}-devel
%defattr(-,root,root,-)
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[^gjos]*
%{_prefix}/include/c++/%{gcc_version}/os*
%{_prefix}/include/c++/%{gcc_version}/s[^u]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++%{?gccv}-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libsupc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%defattr(-,root,root)
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%if %{build_objc}
%files objc
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%defattr(-,root,root,-)
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1objplus

%files -n libobjc%{?gccv}
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libobjc.so.4*
%endif #build_objc

%if %{build_fortran}
%files gfortran
%defattr(-,root,root,-)
%{_prefix}/bin/gfortran%{?gccv}
%{_prefix}/bin/%{_target_platform}-gfortran%{?gccv}
%{_mandir}/man1/gfortran%{gccv}.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib_kinds.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcaf_single.a
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.so
%endif
%doc rpm.doc/gfortran/*

%if ! 0%{?gccv:1}
%files -n libgfortran-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgfortran.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgfortran.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%endif

%files -n libgfortran
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgfortran.so.3*

%endif # build_fortran

%if %{build_java}
%files java
%defattr(-,root,root,-)
%{_prefix}/bin/gcj
%{_prefix}/bin/gjavah
%{_prefix}/bin/gcjh
%{_prefix}/bin/jcf-dump
%{_mandir}/man1/gcj.1*
%{_mandir}/man1/jcf-dump.1*
%{_mandir}/man1/gjavah.1*
%{_mandir}/man1/gcjh.1*
%{_infodir}/gcj*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ecj1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jvgenmain
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj-tools.so
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgij.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgij.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgij.so
%endif
%doc rpm.doc/changelogs/gcc/java/ChangeLog*

%files -n libgcj
%defattr(-,root,root,-)
%{_prefix}/bin/jv-convert
%{_prefix}/bin/gij
%{_prefix}/bin/gjar
%{_prefix}/bin/fastjar
%{_prefix}/bin/gnative2ascii
%{_prefix}/bin/grepjar
%{_prefix}/bin/grmic
%{_prefix}/bin/grmid
%{_prefix}/bin/grmiregistry
%{_prefix}/bin/gtnameserv
%{_prefix}/bin/gkeytool
%{_prefix}/bin/gorbd
%{_prefix}/bin/gserialver
%{_prefix}/bin/gcj-dbtool
%{_prefix}/bin/gjarsigner
%{_mandir}/man1/fastjar.1*
%{_mandir}/man1/grepjar.1*
%{_mandir}/man1/gjar.1*
%{_mandir}/man1/gjarsigner.1*
%{_mandir}/man1/jv-convert.1*
%{_mandir}/man1/gij.1*
%{_mandir}/man1/gnative2ascii.1*
%{_mandir}/man1/grmic.1*
%{_mandir}/man1/grmiregistry.1*
%{_mandir}/man1/gcj-dbtool.1*
%{_mandir}/man1/gkeytool.1*
%{_mandir}/man1/gorbd.1*
%{_mandir}/man1/grmid.1*
%{_mandir}/man1/gserialver.1*
%{_mandir}/man1/gtnameserv.1*
%{_infodir}/fastjar.info*
%{_infodir}/cp-tools.info*
%{_prefix}/%{_lib}/libgcj.so.*
%{_prefix}/%{_lib}/libgcj-tools.so.*
%{_prefix}/%{_lib}/libgcj_bc.so.*
%{_prefix}/%{_lib}/libgij.so.*
%dir %{_prefix}/%{_lib}/gcj-%{version}
%{_prefix}/%{_lib}/gcj-%{version}/libgtkpeer.so
%{_prefix}/%{_lib}/gcj-%{version}/libgjsmalsa.so
%{_prefix}/%{_lib}/gcj-%{version}/libjawt.so
%{_prefix}/%{_lib}/gcj-%{version}/libjvm.so
%{_prefix}/%{_lib}/gcj-%{version}/libjavamath.so
%dir %{_prefix}/share/java
%{_prefix}/share/java/[^sl]*
%{_prefix}/share/java/libgcj-%{version}.jar
%dir %{_prefix}/%{_lib}/security
%config(noreplace) %{_prefix}/%{_lib}/security/classpath.security
%{_prefix}/%{_lib}/logging.properties
%dir %{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_prefix}/%{_lib}/gcj-%{version}/classmap.db

%files -n libgcj-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/gcj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jvmpi.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.spec
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgcj_bc.so
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgcj_bc.so
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[gj]*
%{_prefix}/include/c++/%{gcc_version}/org
%{_prefix}/include/c++/%{gcc_version}/sun
%{_prefix}/%{_lib}/pkgconfig/libgcj-*.pc
%doc rpm.doc/boehm-gc/* rpm.doc/fastjar/* rpm.doc/libffi/*
%doc rpm.doc/libjava/*

%files -n libgcj-src
%defattr(-,root,root,-)
%dir %{_prefix}/share/java
%{_prefix}/share/java/src*.zip
%{_prefix}/share/java/libgcj-tools-%{version}.jar
%endif

%if %{build_ada}
%files gnat
%defattr(-,root,root,-)
%{_prefix}/bin/gnat%{?gccv}
%{_prefix}/bin/gnatfind%{?gccv}
%{_prefix}/bin/gnatname%{?gccv}
%{_prefix}/bin/gnatlink%{?gccv}
%{_prefix}/bin/gnatgcc%{?gccv}
%{_prefix}/bin/gnatmake%{?gccv}
%{_prefix}/bin/gnatxref%{?gccv}
%{_prefix}/bin/gnatkr%{?gccv}
%{_prefix}/bin/gnatchop%{?gccv}
%{_prefix}/bin/gnatls%{?gccv}
%{_prefix}/bin/gnatbind%{?gccv}
%{_prefix}/bin/gnatprep%{?gccv}
%{_prefix}/bin/gnatclean%{?gccv}
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adalib
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adalib
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat%{?gccv}
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat%{?gccv}-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnarl.a
%endif

%files -n libgnat%{?gccv}-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnarl.a
%endif
%endif

%files -n libgomp
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%files -n libmudflap
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libmudflap.so.0*
%{_prefix}/%{_lib}/libmudflapth.so.0*

%files -n libmudflap%{?gccv}-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mf-runtime.h
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%endif
%if ! 0%{?gccv:1}
%{_libdir}/libmud*.so
%endif
%doc rpm.doc/changelogs/libmudflap/ChangeLog*

%files -n libmudflap%{?gccv}-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflapth.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflapth.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%endif

%if %{build_libquadmath}
%files -n libquadmath
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libquadmath.so.0
%{_prefix}/%{_lib}/libquadmath.so.%{libquadmath_ver}
%{_infodir}/libquadmath.info*
%doc rpm.doc/libquadmath/COPYING*

%files -n libquadmath%{?gccv}-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%doc rpm.doc/libquadmath/ChangeLog*

%files -n libquadmath%{?gccv}-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libquadmath.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libquadmath.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%endif
%endif # build_libquadmath

%if %{build_libitm}
%files -n libitm
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*

%files -n libitm%{?gccv}-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/itm.h
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/itm_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
%endif
%doc rpm.doc/libitm/ChangeLog*

%files -n libitm%{?gccv}-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libitm.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libitm.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%endif
%endif

%if %{build_libatomic}
%files -n libatomic
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libatomic.so
%{_prefix}/%{_lib}/libatomic.so.1*

%files -n libatomic%{?gccv}-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libatomic.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libatomic.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.a
%endif
%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif

%if %{build_libasan}
%files -n libasan
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libasan.so
%{_prefix}/%{_lib}/libasan.so.0*

%files -n libasan%{?gccv}-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libasan.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libasan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
%files -n libtsan
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libtsan.so
%{_prefix}/%{_lib}/libtsan.so.0*

%files -n libtsan%{?gccv}-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%if %{build_go}
%files go
%defattr(-,root,root,-)
%{_prefix}/bin/gccgo%{?gccv}
%{_prefix}/bin/%{_target_platform}-gccgo%{?gccv}
%{_mandir}/man1/gccgo%{?gccv}.1*
%{_infodir}/gccgo%{?gccv}.info*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/go1
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgobegin.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgobegin.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgobegin.a
%endif
%doc rpm.doc/go/*

%files -n libgo
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgo.so.4*
%doc rpm.doc/libgo/*

%files -n libgo%{?gccv}-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/%{_lib}/go
%dir %{_prefix}/%{_lib}/go/%{gcc_version}
%{_prefix}/%{_lib}/go/%{gcc_version}/%{gcc_target_platform}
%ifarch %{multilib_64_archs}
%ifnarch sparc64 ppc64
%dir %{_prefix}/lib/go
%dir %{_prefix}/lib/go/%{gcc_version}
%{_prefix}/lib/go/%{gcc_version}/%{gcc_target_platform}
%endif
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgobegin.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgobegin.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.so
%endif

%files -n libgo%{?gccv}-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgo.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgo.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.a
%endif
%endif

%files plugin-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/plugin

%changelog
* Tue Mar 25 2014 Cristian Gafton <gafton@amazon.com>
- enable libgcc auto reqs to aid in libgcc/glibc system upgrades

* Thu Mar 20 2014 Cristian Gafton <gafton@amazon.com>
- ugh.... do not uuencode and dump out test run results....

* Wed Mar 19 2014 Cristian Gafton <gafton@amazon.com>
- require recent binutils for operation and building
- gcc-go info files are only available if the go backend is built
- re-enable make check
- disable backends: objc, java, go for Amazon Linux

* Wed Mar 12 2014 Cristian Gafton <gafton@amazon.com>
- disable objc backend
- make objc a build conditional
- update build conditional sections for fortran, ada, java

* Fri Mar 7 2014 Cristian Gafton <gafton@amazon.com>
- update texlive/latex build requirements
- add whitespace and some comments to improve the spec file readability
- add stray .so files for libatomic, libasan and libtsan
- version the -static package names for libatomic, libasan and libtsan

* Thu Mar 6 2014 Cristian Gafton <gafton@amazon.com>
- minor build fixes or latest imports
- import source package F19/gcc-4.8.2-7.fc19
- import source package F19/gcc-4.8.2-1.fc19
- import source package F19/gcc-4.8.1-1.fc19
- import source package F18/gcc-4.7.2-8.fc18
- import source package F18/gcc-4.7.2-3.fc18
- import source package F17/gcc-4.7.2-2.fc17
- import source package F17/gcc-4.7.0-5.fc17
- import source package F16/gcc-4.6.3-2.fc16
- import source package F16/gcc-4.6.2-1.fc16
- import source package F15/gcc-4.6.1-9.fc15
- import source package F15/gcc-4.6.0-10.fc15
- import source package F15/gcc-4.6.0-9.fc15
- import source package F15/gcc-4.6.0-7.fc15
- import source package F15/gcc-4.6.0-6.fc15
- import source package F14/gcc-4.5.1-4.fc14
- import source package F14/gcc-4.5.0-3.fc14
- import source package F13/gcc-4.4.5-2.fc13

* Thu Dec 12 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-7
- update from the 4.8 branch
  - PRs libgomp/59467, rtl-optimization/58295, target/56807,
	testsuite/59442
  - fix LRA coalescing for real (PR middle-end/59470)

* Wed Dec 11 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-6
- temporarily revert PR middle-end/58956 to avoid libstdc++
  miscompilation on i?86 (PR middle-end/59470)

* Mon Dec  9 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-5
- update from the 4.8 branch
  - PRs ada/59382, bootstrap/57683, c++/58162, c++/59031, c++/59032,
	c++/59044, c++/59052, c++/59268, c++/59297, c/59280, c/59351,
	fortran/57445, fortran/58099, fortran/58471, fortran/58771,
	middle-end/58742, middle-end/58941, middle-end/58956,
	middle-end/59011, middle-end/59037, middle-end/59138,
	rtl-optimization/58726, target/50751, target/51244, target/56788,
	target/58854, target/58864, target/59021, target/59088,
	target/59101, target/59153, target/59163, target/59207,
	target/59343, target/59405, tree-optimization/57517,
	tree-optimization/58137, tree-optimization/58143,
	tree-optimization/58653, tree-optimization/58794,
	tree-optimization/59014, tree-optimization/59047,
	tree-optimization/59139, tree-optimization/59164,
	tree-optimization/59288, tree-optimization/59330,
	tree-optimization/59334, tree-optimization/59358,
	tree-optimization/59388
- aarch64 gcj enablement (#1023789)
- look for libgfortran.spec and libitm.spec in %%{_lib} rather than lib
  subdirs (#1023789)

* Mon Nov 11 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-4
- update from the 4.8 branch
  - PRs plugins/52872, regression/58985, target/59034

* Wed Nov  6 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-3
- update from the 4.8 branch
  - PRs c++/58282, c++/58979, fortran/58355, fortran/58989, libstdc++/58839,
	libstdc++/58912, libstdc++/58952, lto/57084, middle-end/58789,
	rtl-optimization/58079, rtl-optimization/58831, rtl/58542,
	target/58690, target/58779, target/58792, target/58838,
	tree-optimization/57488, tree-optimization/58805,
	tree-optimization/58984
- fix ICEs in get_bit_range (PR middle-end/58970)
- fix ICEs in RTL loop unswitching (PR rtl-optimization/58997)

* Sun Oct 20 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-2
- update from the 4.8 branch
  - PRs c++/58596, libstdc++/58800
- power8 TImode fix (#1014053, PR target/58673)

* Thu Oct 17 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-1
- update from the 4.8 branch
  - GCC 4.8.2 release
  - PRs c++/57850, c++/58633, libstdc++/58191

* Thu Oct 10 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-12
- update from the 4.8 branch
  - PRs c++/58568, fortran/55469, fortran/57697, fortran/58469,
	libstdc++/57465, libstdc++/57641, libstdc++/58659, target/58460,
	tree-optimization/58539
  - fix asm goto handling (#1017704, PR middle-end/58670)

* Wed Oct  2 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-11
- update from the 4.8 branch
  - PRs c++/58535, libstdc++/58437, libstdc++/58569, middle-end/56791,
	middle-end/58463, middle-end/58564, target/58330,
	tree-optimization/56716
  - fix s390x z10+ chunkification (#1012870, PR target/58574)
- disable ppc{,64} -mvsx-timode by default (#1014053, PR target/58587)

* Fri Sep 20 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-10
- update from the 4.8 branch
  - PRs ada/58264, c++/58457, c++/58458, libstdc++/58358,
	tree-optimization/58088
- on RHEL7, configure on ppc/ppc64 with default -mcpu=power7,
  on s390/s390x with default -march=z10 -mtune=zEC12 and
  on i?86 default to -march=x86-64 -mtune=generic (#805157)
- on Fedora 20+ and RHEL7 default to -fdiagnostics-color=auto
  rather than -fdiagnostics-color=never, if GCC_COLORS isn't
  in the environment; to turn it off by default, set GCC_COLORS=
  in the environment

* Sun Sep 15 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-9
- update from the 4.8 branch
  - PRs c++/58273, libstdc++/58415, middle-end/58377, rtl-optimization/58365,
	target/58314, target/58361, target/58382, tree-optimization/58385
- add arm_neon.h on aarch64 (#1007490)

* Mon Sep  9 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-8
- update from the 4.8 branch
  - PRs c++/58325, libstdc++/58302, libstdc++/58341, middle-end/57656,
	other/12081, target/57735, tree-optimization/57521,
	tree-optimization/57685, tree-optimization/58010,
	tree-optimization/58223, tree-optimization/58228,
	tree-optimization/58246, tree-optimization/58277,
	tree-optimization/58364

* Thu Aug 29 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-7
- update from the 4.8 branch
  - PRs c++/58083, c++/58119, c++/58190, fortran/57798, fortran/58185,
	middle-end/56977, middle-end/57381, middle-end/58257, target/56979,
	target/57865, target/57927, target/58218, tree-optimization/57343,
	tree-optimization/57396, tree-optimization/57417,
	tree-optimization/58006, tree-optimization/58164,
	tree-optimization/58165, tree-optimization/58209
- fix up x86-64 -mcmodel=large -fpic TLS GD and LD model
  (#994244, PR target/58067)
- power8 fusion support fixes (#731884, PR target/58160)

* Wed Aug 14 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-6
- update from the 4.8 branch
  - PRs c++/57825, c++/57901, c++/57981, c++/58022, fortran/57435,
	fortran/58058, libstdc++/56627, libstdc++/57914, libstdc++/58098,
	middle-end/58041, rtl-optimization/57459, rtl-optimization/57708,
	rtl-optimization/57878, sanitizer/56417, target/51784, target/57516,
	target/58067, target/58132, tree-optimization/57980
- power8 fusion support (#731884)
- fix up ABI alignment patch (#947197)
- fix up SRA with volatile struct accesses (PR tree-optimization/58145)

* Wed Jul 17 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-5
- update from the 4.8 branch
  - PRs target/55656, target/55657
  - update to Go 1.1.1
- backport power8 HTM support from trunk (#731884)
- backport s390 zEC12 HTM support from trunk

* Mon Jul 15 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-4
- update from the 4.8 branch
  - PRs c++/57437, c++/57526, c++/57532, c++/57545, c++/57550, c++/57551,
	c++/57645, c++/57771, c++/57831, fortran/57785,
	rtl-optimization/57829, target/56102, target/56892, target/56987,
	target/57506, target/57631, target/57736, target/57744,
	target/57777, target/57792, target/57844
- backport some raw-string literal handling fixes (#981029,
  PRs preprocessor/57757, preprocessor/57824)
- improve convert_to_* (PR c++/56493)
- tune for power7 on RHEL7

* Fri Jun 28 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-3
- update from the 4.8 branch
  - PRs c++/53211, c++/56544, driver/57652, libstdc++/57619, libstdc++/57666,
	libstdc++/57674, rtl-optimization/57518, target/57623, target/57655,
	tree-optimization/57358, tree-optimization/57537
  - fix up gcc-{ar,nm,ranlib} (#974853, PR driver/57651)
- fix two libitm HTM handling bugs (PR libitm/57643)
- speed up __popcount[sdt]i2 library function (PR middle-end/36041)
- backport power8 support from trunk (#731884, PR target/57615)
- for Fedora 20+ test -fstack-protector-strong during %%check instead
  of -fstack-protector

* Wed Jun 12 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-2
- update from the 4.8 branch
  - PRs fortran/57364, fortran/57508, target/56547, target/57379, target/57568
- backport backwards compatible alignment ABI fixes (#947197, PR target/56564)
- fix up widening multiplication vectorization on big-endian
  (PR tree-optimization/57537)

* Mon Jun  3 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-1
- update from the 4.8 branch
  - GCC 4.8.1 release
  - PRs c++/56930, c++/57319, fortran/57217, target/49146, target/56742
- backport Intel Silvermont enablement and tuning from trunk
- backport 3 small AMD improvement patches from trunk

* Sun May 26 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-8
- update from the 4.8 branch
  - std::chrono::steady_clock ABI fixes from 4.8.0-7

* Fri May 24 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-7
- update from the 4.8 branch
  - PRs c++/57016, c++/57317, c++/57325, c++/57388, libffi/56033,
	libstdc++/57336, middle-end/57344, middle-end/57347, plugins/56754,
	rtl-optimization/57341, target/56732, target/57356,
	tree-optimization/57303, tree-optimization/57318,
	tree-optimization/57321, tree-optimization/57330, tree-ssa/57385
  - std::chrono::steady_clock now really steady

* Fri May 17 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-6
- update from the 4.8 branch
  - PRs c++/56782, c++/56998, c++/57041, c++/57196, c++/57243, c++/57252,
	c++/57253, c++/57254, c++/57274, c++/57279, middle-end/57251,
	rtl-optimization/57281, rtl-optimization/57300, target/45359,
	target/46396, target/57264
- backport color diagnostics support from trunk, enable with
  -fdiagnostics-color=auto, -fdiagnostics-color=always or
  having non-empty GCC_COLORS variable in environment
- backport -fstack-protector-strong support from trunk

* Fri May 10 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-5
- update from the 4.8 branch
  - PRs bootstrap/54281, bootstrap/54659, c++/57047, c++/57068, c++/57222,
	fortran/57142, libstdc++/57212, middle-end/56988, target/55033,
	target/57237, tree-optimization/57200, tree-optimization/57214
- fix up strlen pass (PR tree-optimization/57230)

* Tue May  7 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-4
- update from the 4.8 branch
  - PRs ada/56474, c++/50261, c++/56450, c++/56859, c++/56970, c++/57064,
	c++/57092, c++/57183, debug/57184, fortran/51825, fortran/52512,
	fortran/53685, fortran/56786, fortran/56814, fortran/56872,
	fortran/56968, fortran/57022, libfortran/51825, libfortran/52512,
	libfortran/56786, libstdc++/57010, middle-end/57103,
	rtl-optimization/56605, rtl-optimization/56847,
	rtl-optimization/57003, rtl-optimization/57130,
	rtl-optimization/57131, rtl-optimizations/57046, sanitizer/56990,
	target/44578, target/55445, target/56797, target/56866, target/57018,
	target/57091, target/57097, target/57098, target/57106, target/57108,
	target/57150, tree-optimization/57051, tree-optimization/57066,
	tree-optimization/57083, tree-optimization/57104,
	tree-optimization/57149, tree-optimization/57185
  - fix gcj with -fsection-anchors (#952673, PR libgcj/57074)
- enable libitm on s390{,x}
- error when linking with both -fsanitize=address and -fsanitize=thread
  (#957778)

* Fri Apr 19 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-3
- update from the 4.8 branch
  - PRs c++/56388, fortran/56816, fortran/56994, rtl-optimization/56992,
	target/56890, target/56903, target/56948, tree-optimization/56962,
	tree-optimization/56984
- fix up LRA caused miscompilation of xulrunner on i?86
  (#949553, PR rtl-optimization/56999)
- reassoc fix for -Ofast -frounding-math (PR tree-optimization/57000)

* Fri Apr 12 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-2
- update from the 4.8 branch
  - PRs c++/35722, c++/45282, c++/52014, c++/52374, c++/52748, c++/54277,
	c++/54359, c++/54764, c++/55532, c++/55951, c++/55972, c++/56039,
	c++/56447, c++/56582, c++/56646, c++/56692, c++/56699, c++/56722,
	c++/56728, c++/56749, c++/56772, c++/56774, c++/56793, c++/56794,
	c++/56821, c++/56895, c++/56913, debug/56819, fortran/54932,
	fortran/56696, fortran/56735, fortran/56737, fortran/56782,
	libstdc++/55977, libstdc++/55979, libstdc++/56002, libstdc++/56678,
	libstdc++/56834, lto/56777, middle-end/56694, middle-end/56768,
	middle-end/56883, other/55274, rtl-optimization/48182,
	rtl-optimization/56745, sanitizer/55702, target/54805, target/55487,
	target/56560, target/56720, target/56771, tree-optimization/48184,
	tree-optimization/48186, tree-optimization/48762,
	tree-optimization/56407, tree-optimization/56501,
	tree-optimization/56817, tree-optimization/56837,
	tree-optimization/56899, tree-optimization/56918,
	tree-optimization/56920

* Fri Mar 22 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-1
- update from the 4.8 branch
  - GCC 4.8.0 release
  - PRs c++/56607, other/43620
  - fix length in .debug_aranges in some cases
- improve debug info for optimized away global vars (PR debug/56608)
- don't warn about signed 1-bit enum bitfields containing values 0 and -1
  or just -1 (PR c/56566)

* Wed Mar 20 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.18
- update from the 4.8 branch
  - PRs libstdc++/56468, target/56640, tree-optimization/56635,
	tree-optimization/56661
- package libasan_preinit.o

* Tue Mar 19 2013 Cristian Gafton <gafton@amazon.com>
- fix requires for libitm

* Mon Mar 18 2013 Cristian Gafton <gafton@amazon.com>
- decorate inter-package dependencies with _isa

* Sat Mar 16 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.17
- update from trunk and the 4.8 branch
  - PRs ada/52123, c++/51412, c++/51494, c++/51884, c++/52183, c++/56222,
	c++/56346, c++/56565, c++/56567, c++/56611, c++/56614, debug/56307,
	fortran/56575, fortran/56615, libstdc++/56492, libstdc++/56609,
	libstdc++/56613, lto/56557, middle-end/56524, middle-end/56571,
	target/40797, target/49880, target/56470, target/56591, target/56619,
	testsuite/54119, tree-optimization/53265, tree-optimization/56478,
	tree-optimization/56570, tree-optimization/56608

* Thu Mar  7 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.16
- updated from trunk
  - PRs bootstrap/56509, c++/54383, c++/55135, c++/56464, c++/56530,
	c++/56534, c++/56543, debug/55364, debug/56510, libquadmath/55473,
	lto/50293, lto/56515, middle-end/50494, middle-end/56294,
	middle-end/56525, middle-end/56526, middle-end/56548,
	rtl-optimization/56484, rtl-optimization/56494, target/56529,
	tree-optimization/56270, tree-optimization/56521,
	tree-optimization/56539, tree-optimization/56559
  - include arm-cores.def in gcc-python-plugin on arm (#910926)
- include vxworks-dummy.h in gcc-python-plugin where needed (PR plugins/45078)

* Mon Mar  4 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.15
- updated from trunk
  - PRs c++/10291, c++/40405, c++/52688, c++/55632, c++/55813, c++/56243,
	c++/56358, c++/56359, c++/56377, c++/56395, c++/56403, c++/56419,
	c++/56438, c++/56481, fortran/54730, fortran/56385, fortran/56416,
	fortran/56477, fortran/56491, libfortran/30162, libstdc++/56011,
	libstdc++/56012, middle-end/45472, middle-end/56077,
	middle-end/56108, middle-end/56420, middle-end/56461,
	rtl-optimization/50339, rtl-optimization/56466, sanitizer/56393,
	sanitizer/56454, target/48901, target/52500, target/52501,
	target/52550, target/54639, target/54640, target/54662, target/56444,
	target/56445, target/56455, testsuite/52641, tree-optimization/55481,
	tree-optimization/56175, tree-optimization/56294,
	tree-optimization/56310, tree-optimization/56415,
	tree-optimization/56426, tree-optimization/56443,
	tree-optimization/56448
- fnsplit fix (PR tree-optimization/56424)

* Wed Feb 20 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.14
- updated from trunk
  - PRs asan/56330, c++/51242, c++/54276, c++/56373, libquadmath/56379,
	middle-end/55889, middle-end/56349, pch/54117,
	rtl-optimization/56348, target/52555, target/54685, target/56214,
	target/56347, tree-optimization/55334, tree-optimization/56321,
	tree-optimization/56350, tree-optimization/56366,
	tree-optimization/56381, tree-optimization/56384,
	tree-optimization/56396, tree-optimization/56398
- add BuildRequires: /usr/bin/pod2man to fix man pages generation
- don't ICE on bogus inline asm in kernel (#912857, PR inline-asm/56405)
- fix up info page building with texinfo 5.0 (PR bootstrap/56258)
- devirtualization ICE fix (PR tree-optimization/56265)

* Fri Feb 15 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.13
- updated from trunk
  - PRs bootstrap/56327, c++/52026, c++/54922, c++/55003, c++/55220,
	c++/55223, c++/55232, c++/55582, c++/55670, c++/55680, c++/56323,
	c++/56343, fortran/53818, fortran/56224, fortran/56318,
	libstdc++/56111, lto/50494, target/55431, target/55941,
	testsuite/56138
- asan fixes (PR sanitizer/56330)
- asan speedup - use 0x7fff8000 shadow offset instead of 1LL << 44 on
  x86_64

* Wed Feb 13 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.12
- updated from trunk
  - PRs c++/55710, c++/55879, c++/55993, c++/56135, c++/56155, c++/56285,
	c++/56291, c/44938, fortran/46952, fortran/56204, inline-asm/56148,
	libitm/55693, lto/56295, lto/56297, middle-end/56288,
	sanitizer/56128, target/52122, testsuite/56082
  - fix IRA bug that caused reload ICE on ARM (#910153, target/56184)
  - attempt harder to fold "n" constrainted asm input operands in C++
    with -O0 (#910421, c++/56302)

* Mon Feb 11 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.11
- updated from trunk
  - PRs c++/56238, c++/56247, c++/56268, fortran/55362, libstdc++/56267,
	libstdc++/56278, libstdc++/56282, rtl-optimization/56246,
	rtl-optimization/56275, target/56043, tree-optimization/56264,
	tree-optimization/56273
- improve expansion of mem1 op= mem2 (PR rtl-optimization/56151)

* Fri Feb  8 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.10
- updated from trunk
  - PRs bootstrap/56227, c++/56235, c++/56237, c++/56239, c++/56241,
	debug/53363, fortran/54339, fortran/55789, libstdc++/56193,
	libstdc++/56216, lto/56231, middle-end/56181,
	rtl-optimization/56195, rtl-optimization/56225, target/50678,
	target/54009, target/54131, tree-optimization/56250
  - fix Ada frontend miscompilation with profiledbootstrap (#906516,
    PR rtl-optimization/56178)
- restore parsing of ppc inline asm dialects (#909298, PR target/56256)
- fix up libiberty old regex (PR other/56245)
- fix IRA -O0 -g code debug regression (PR debug/53948)

* Wed Feb  6 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.9
- updated from trunk
  - PRs c++/54122, c++/56177, c++/56208, debug/54793, fortran/47517,
	fortran/50627, fortran/54195, fortran/56008, fortran/56054,
	libstdc++/56202, lto/56168, middle-end/56113, middle-end/56167,
	middle-end/56217, rtl-optimization/56131, sanitizer/55617,
	target/52123, target/54601, target/55146, target/56186,
	tree-optimization/53185, tree-optimization/53342,
	tree-optimization/54386, tree-optimization/55789,
	tree-optimization/56188
  - fix up stdarg pass (PR tree-optimization/56205, #906367)
  - remove unused thread_local bitfield (#907882)
- fix cselim pass on calls that might free memory (PR tree-optimization/52448)
- fix libgfortran internal_pack (PR fortran/55978)
- fix up .debug_loc for first function in CU, if it contains empty ranges
  at the beginning of the function (PR debug/56154, #904252)
- fix ppc64 indirect calls (PR target/56228, #908388)

* Thu Jan 31 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.8
- updated from trunk
  - PRs c++/56162, debug/54410, debug/54508, debug/55059, fortran/54107,
	fortran/56138, libgomp/55561, libstdc++/54314, lto/56147,
	middle-end/53073, other/53413, other/54620, rtl-optimization/56144,
	sanitizer/55374, target/39064, target/56121, tree-optimization/55270,
	tree-optimization/56064, tree-optimization/56113,
	tree-optimization/56150, tree-optimization/56157

* Tue Jan 29 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.7
- updated from trunk
  - PRs c++/56095, c++/56104, c/56078, fortran/53537, fortran/55984,
	fortran/56047, inline-asm/55934, libstdc++/56085, libstdc++/56112,
	other/54814, other/56076, rtl-optimization/56117, target/54663,
	target/56114, testsuite/56053, tree-optimization/55927,
	tree-optimization/56034, tree-optimization/56035,
	tree-optimization/56094, tree-optimization/56098,
	tree-optimization/56125

* Thu Jan 24 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.6
- updated from trunk
  - PRs c++/53609, c++/55944, c++/56067, c++/56071, fortran/56081,
	libgomp/51376, libgomp/56073, libquadmath/56072, middle-end/56074,
	sanitizer/55989, target/49069, target/54222, target/55686,
	target/56028
- update TeX related BuildRequires (#891460)

* Tue Jan 22 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.5
- updated from trunk
  - PRs c++/56059, fortran/55919, rtl-optimization/56023,
	tree-optimization/56051
- fix up cloog dlopen patches for upgrade to cloog-0.18.0
- fix Fortran OpenMP OOP ICE (PR fortran/56052)

* Mon Jan 21 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.4
- updated from trunk
  - PRs ada/864, bootstrap/55792, bootstrap/55961, c++/52343, c++/55663,
	c++/55753, c++/55801, c++/55878, c++/55893, c/48418, debug/49888,
	debug/53235, debug/53671, debug/54114, debug/54402, debug/55579,
	debug/56006, driver/55470, driver/55884, fortran/42769, fortran/45836,
	fortran/45900, fortran/47203, fortran/52865, fortran/53876,
	fortran/54286, fortran/54678, fortran/54990, fortran/54992,
	fortran/55072, fortran/55341, fortran/55618, fortran/55758,
	fortran/55763, fortran/55806, fortran/55852, fortran/55868,
	fortran/55935, fortran/55983, libmudflap/53359, libstdc++/51007,
	libstdc++/55043, libstdc++/55233, libstdc++/55594, libstdc++/55728,
	libstdc++/55847, libstdc++/55861, libstdc++/55908, lto/45375,
	middle-end/55114, middle-end/55851, middle-end/55882,
	middle-end/55890, middle-end/56015, other/55973, other/55982,
	rtl-optimization/52573, rtl-optimization/53827,
	rtl-optimization/55153, rtl-optimization/55547,
	rtl-optimization/55672, rtl-optimization/55829,
	rtl-optimization/55833, rtl-optimization/55845,
	rtl-optimization/56005, sanitizer/55488, sanitizer/55679,
	sanitizer/55844, target/42661, target/43961, target/54461,
	target/54908, target/55301, target/55433, target/55565,
	target/55718, target/55719, target/55876, target/55897,
	target/55940, target/55948, target/55974, target/55981,
	target/56058, testsuite/54622, testsuite/55994,
	tree-optimization/44061, tree-optimization/48189,
	tree-optimization/48766, tree-optimization/52631,
	tree-optimization/53465, tree-optimization/54120,
	tree-optimization/54767, tree-optimization/55273,
	tree-optimization/55569, tree-optimization/55823,
	tree-optimization/55862, tree-optimization/55875,
	tree-optimization/55888, tree-optimization/55920,
	tree-optimization/55921, tree-optimization/55955,
	tree-optimization/55964, tree-optimization/55995,
	tree-optimization/56029, tree-optimization/55264
- fix up multiversioning (PR c++/55742)
- fix up ICE with target attribute (PR middle-end/56022)
- update isl to 0.11.1 and cloog to 0.18.0

* Fri Nov  9 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-8
- update from the 4.7 branch
  - PRs fortran/54917, libstdc++/28811, libstdc++/54482, libstdc++/55028,
	libstdc++/55215, middle-end/55219, target/55204,
	tree-optimization/54986
- further debug info quality improvements
- fix reassociation (PR c++/55137)
- fix range test optimization with -fwrapv (PR tree-optimization/55236)
- add BuildRequires hostname (#875001)
- __cxa_vec_new[23] overflow checking (#875009)

* Mon Nov  5 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-7
- update from the 4.7 branch
  - PRs c++/54984, c++/54988, debug/54828, libstdc++/55047, libstdc++/55123,
	libstdc++/55169, middle-end/54945, rtl-optimization/53701,
	rtl-optimization/54870, target/53975, target/54892, target/55019,
	target/55175, tree-optimization/53708, tree-optimization/54146,
	tree-optimization/54877, tree-optimization/54902,
	tree-optimization/54920, tree-optimization/54985
- backported s390{,x} zEC12 enablement (#805114)
- backport of selected debug info quality improvements
  - PRs debug/54402, debug/54693, debug/54953, debug/54970, debug/54971
- optimize away overflow checking for new char[n]; and similar cases
  where n is multiplied by 1

* Mon Oct 15 2012 Jon Ciesla <limburgher@gmail.com> 4.7.2-6
- Provides: bundled(libiberty)

* Mon Oct 15 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-5
- update from the 4.7 branch
  - PRs fortran/54784, libfortran/54736, libstdc++/54861

* Tue Oct 9 2012 Cristian Gafton <gafton@amazon.com>
- fix gcov typo in alternatives script
- update info files for clean removal on package uninstall
- build versioned names of libmudflap-devel and libmudflap-static subpackages
- fix uninstall errors in rpm scriplets
- tighten dependencies between subpackages to avoid indirection through the meta-gcc packages

* Tue Oct  9 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-4
- update from the 4.7 branch
  - PRs c++/54777, c++/54858, debug/53135, target/54741, target/54785,
	target/54854
- backport of selected debug info quality improvements (#851467)
  - PRs debug/48866, debug/52983, debug/53740, debug/53923, debug/54519,
	debug/54551

* Mon Oct 8 2012 Cristian Gafton <gafton@amazon.com>
- require the specific version of libgcc

* Mon Oct  1 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-3
- update from the 4.7 branch
  - PRs target/54083, target/54703, target/54746, testsuite/54007
- backport operator new[] overflow checking (#850911, PR c++/19351)

* Thu Sep 27 2012 Cristian Gafton <gafton@amazon.com>
- handle upgrading from old compiler builds for libstdc++ as well
- update trigger scripts o fire inside libgcc packages
- add triggerpostun for upgrading from older libgcc packages

* Fri Sep 21 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-2
- update from the 4.7 branch
  - PRs c/54103, c/54552, libstdc++/54102, middle-end/54638, other/43620

* Thu Sep 20 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-1
- update from the 4.7 branch
  - GCC 4.7.2 release
  - PRs c++/53661, lto/54312, tree-optimization/54563

* Mon Sep 17 2012 Cristian Gafton <gafton@amazon.com>
- avoid file conflicts on libgo betwenn gcc46 and gcc47
- use explicit dependencies for libgo in gcc-go
- version names of the libitm subpackages
- update handling of info doc files for multi-versioned gcc environment
- fix/update the preun scripts for alternatives-enabled packages
- add obsoletes for renamed libquadmath packages
- version subpackages libquatmath-{devel,static}

* Sun Sep 16 2012 Cristian Gafton <gafton@amazon.com>
- rely on automatic soname dependencies to bring in the proper libgfortran for gcc-gfortran
- fix libgfortran requires for a multi-compiler environment

* Sat Sep 15 2012 Cristian Gafton <gafton@amazon.com>
- version package names got libgo
- undo need for a new fedora-style filesystem layout

* Fri Sep 14 2012 Cristian Gafton <gafton@amazon.com>
- version the binary names for the gcc-ar, gcc-nm and gcc-ranlib binaries
- update for new lib versions in gcc47
- fix merge issues for gcc47

* Thu Sep 13 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-8
- update from the 4.7 branch
  - PRs c++/53836, c++/53839, c++/54086, c++/54197, c++/54253, c++/54341,
	c++/54506, c++/54511, c/54363, c/54428, c/54559, debug/54534,
	driver/54335, fortran/53306, fortran/54208, fortran/54225,
	fortran/54435, fortran/54443, fortran/54556, gcov-profile/54487,
	libstdc++/54172, libstdc++/54185, libstdc++/54297, libstdc++/54351,
	libstdc++/54376, libstdc++/54388, lto/53572, middle-end/53667,
	middle-end/53992, middle-end/54146, middle-end/54486,
	middle-end/54515, rtl-optimization/54088, rtl-optimization/54369,
	rtl-optimization/54455, target/45070, target/46254, target/54212,
	target/54220, target/54252, target/54436, target/54461,
	target/54476, target/54536, tree-opt/54494,
	tree-optimization/53922, tree-optimization/54498
- fix up _mm_f{,n}m{add,sub}_s{s,d} fma intrinsics (PR target/54564)

* Tue Sep 11 2012 Cristian Gafton <gafton@amazon.com>
- add missing dep and patch to get docs built correctly

* Mon Sep 10 2012 Cristian Gafton <gafton@amazon.com>
- fix libstdc++ posttrans script
- re-enable building of the libstdc++ docs
- skip checks for bootstraping compiler switch
- use the meta-package to switch the compilers around
- conditionalize obsoleting the old gcc package set

* Sat Sep 8 2012 Cristian Gafton <gafton@amazon.com>
- add posttrans scriplets to  enable alternatives setup upon installation
- fix gcov typo

* Fri Sep 7 2012 Cristian Gafton <gafton@amazon.com>
- keep debug infor symbols for static libs around
- add obsoletes to make the packages upgradeable
- do not version libmudflap packages
- add alternatives support to libstdc++-devel subpackage
- implement alternatives support
- enable gfortran builds
- update build spec in preparation for alternatives implementation

* Mon Aug 13 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-7
- update from the 4.7 branch
  - PR rtl-optimization/53942
- backport -mrdseed, -mprfchw and -madx support

* Mon Aug 13 2012 Cristian Gafton <gafton@amazon.com>
- fix package name typo: gcc46-c++46 -> gcc46-c++

* Fri Aug 10 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-6
- update from the 4.7 branch
  - PRs libstdc++/54036, libstdc++/54075, rtl-optimization/54157,
	target/33135, target/52530

* Fri Jul 20 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-5
- update from the 4.7 branch
  - PRs c++/54026, middle-end/54017, rtl-optimization/52250, target/53877,
	target/54029
  - fix endless hang of C++ compiler (#841814, PR c++/54038)

* Wed Jul 18 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-4
- update from the 4.7 branch
  - PRs c++/53549, c++/53989, c++/53995, libstdc++/53978

* Mon Jul 16 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-3
- update from the 4.7 branch
  - C++11 ABI change - std::list and std::pair in C++11 ABI compatible again
    with C++03, but ABI incompatible with C++11 in GCC 4.7.[01]
  - PRs bootstrap/52947, c++/53733, c++/53816, c++/53821, c++/53826,
	c++/53882, c++/53953, fortran/53732, libstdc++/49561,
	libstdc++/53578, libstdc++/53657, libstdc++/53830, libstdc++/53872,
	middle-end/38474, middle-end/50708, middle-end/52621,
	middle-end/52786, middle-end/53433, rtl-optimization/53908,
	target/53110, target/53811, target/53853, target/53961,
	testsuite/20771, tree-optimization/53693
- backport -mrtm and -mhle support (PRs target/53194, target/53201,
  target/53315)
- fix up ppc32 *movdi_internal32 pattern (#837630)
- apply ld.so arm hfp patch on all arm arches
- enable go support on arm

* Fri Jul 13 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-2
- change ld.so pathname for arm hfp for F18+

* Fri Jun 29 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-1
- update from the 4.7 branch
  - GCC 4.7.1 release
  - PRs ada/53592, c++/51214, c++/52637, c++/52841, c++/52988, c++/53202,
	c++/53305, c++/53498, c++/53524, c++/53594, c++/53599, c++/53602,
	c++/53616, c++/53651, c++/53752, debug/53682, fortran/50619,
	fortran/53597, fortran/53685, fortran/53691, gcov-profile/53744,
	libgomp/52993, libstdc++/53270, libstdc++/53678, middle-end/53470,
	middle-end/53580, middle-end/53790, preprocessor/37215,
	rtl-optimization/53589, rtl-optimization/53700, target/52908,
	target/53559, target/53595, target/53621, target/53759,
	tree-optimization/52558

* Mon Jun  4 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-7
- update from the 4.7 branch
  - PRs ada/53517, c++/52725, c++/52905, c++/52973, c++/53137, c++/53220,
	c++/53356, c++/53484, c++/53491, c++/53500, c++/53503,
	fortran/53521, libstdc++/52007, middle-end/47530, middle-end/48124,
	middle-end/48493, middle-end/52080, middle-end/52097,
	middle-end/52979, middle-end/53008, middle-end/53471,
	middle-end/53501, rtl-optimization/52528, rtl-optimization/53519,
	target/46261, target/52642, target/52667, tree-optimization/53438,
	tree-optimization/53505, tree-optimization/53516,
	tree-optimization/53550

* Fri May 25 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-6
- update from the 4.7 branch
  - PRs ada/52362, ada/52494, bootstrap/53183, c++/53209, c++/53301,
	c/53418, debug/52727, fortran/53310, fortran/53389, libstdc++/52700,
	middle-end/51071, middle-end/52584, middle-end/53460,
	rtl-optimization/52804, target/46098, target/53256, target/53272,
	target/53358, target/53385, target/53416, target/53435, target/53448,
	tree-optimization/53364, tree-optimization/53366,
	tree-optimization/53408, tree-optimization/53409,
	tree-optimization/53410, tree-optimization/53436,
	tree-optimization/53465

* Mon May  7 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-5
- update from the 4.7 branch
  - PRs fortran/53111, fortran/53255, target/48496, target/52999,
	target/53228, tree-optimization/52633, tree-optimization/52870,
	tree-optimization/53195, tree-optimization/53239

* Fri May  4 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-4
- update from the 4.7 branch
  - PRs c++/53186, fortran/52864, libstdc++/53193, lto/52605,
	target/52684, target/53199, tree-optimization/53144
  - fix up gcc-ar, gcc-nm and gcc-ranlib (#818311, PR plugins/53126)

* Wed May  2 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-3
- update from the 4.7 branch
  - PRs bootstrap/52840, c++/38543, c++/50303, c++/50830, c++/53003,
	c/51527, c/52880, c/53060, fortran/53148, libstdc++/52689,
	libstdc++/52839, libstdc++/53027, libstdc++/53067, libstdc++/53115,
	middle-end/52939, middle-end/52999, middle-end/53084,
	middle-end/53136, rtl-optimization/53160, target/52932,
	target/53020, target/53033, target/53065, target/53120,
	target/53138, testsuite/52641, testsuite/53046,
	tree-optimization/53085, tree-optimization/53163,
	tree-optimizations/52891
- fix ARM SELECT_CC_MODE ICE (#817086, PR target/53187)
- fix predictive commoning debug info ICE (PR debug/53174)

* Mon Apr 16 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-2
- update from the 4.7 branch
  - PRs c++/52292, c++/52380, c++/52465, c++/52487, c++/52596, c++/52671,
	c++/52672, c++/52685, c++/52718, c++/52743, c++/52746, c++/52759,
	c++/52796, c++/52824, c++/52906, c/52682, c/52862, fortran/52452,
	fortran/52668, fortran/52893, libgfortran/52758, libitm/52854,
	libstdc++/52433, libstdc++/52476, libstdc++/52540, libstdc++/52591,
	libstdc++/52699, libstdc++/52799, libstdc++/52822, libstdc++/52924,
	libstdc++/52942, middle-end/51893, middle-end/52493,
	middle-end/52547, middle-end/52580, middle-end/52640,
	middle-end/52691, middle-end/52693, middle-end/52720,
	middle-end/52750, middle-end/52894, other/52545,
	rtl-optimization/52543, target/48596, target/48806, target/50310,
	target/52461, target/52484, target/52488, target/52496, target/52499,
	target/52505, target/52506, target/52507, target/52508, target/52610,
	target/52692, target/52698, target/52717, target/52736, target/52737,
	target/52775, tree-optimization/52406, tree-optimization/52678,
	tree-optimization/52701, tree-optimization/52754,
	tree-optimization/52835, tree-optimization/52943,
	tree-optimization/52969
- avoid duplicate pointers in C++ debug info due to injected class name
  (PR debug/45088)
- libjava locale fixes (#712013)

* Thu Mar 22 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-1
- update from the 4.7 branch
  - GCC 25th Anniversary 4.7.0 release
  - fix up new auto mangling

* Thu Mar 15 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.20
- update from the 4.7 branch
  - PRs fortran/52469, libitm/52526, libstdc++/52456, target/52450
  - fix __builtin_ir{ound,int}{,f,l} expansion (#803689, PR middle-end/52592)
  - fix up devirtualization (#802731, PR c++/52582)
- fix up user defined literal operator"" lookup (PR c++/52521)
- avoid false positive -Wunused-but-set-* warnings with __builtin_shuffle
  (PR c/52577)

* Thu Mar  8 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.19
- update from trunk and the 4.7 branch
  - PRs libstdc++/51785, middle-end/52419, middle-end/52443,
	middle-end/52463, rtl-optimization/52417, target/49939,
	target/51417, target/52408, target/52437, target/52481,
	testsuite/52297, tree-opt/52242, tree-optimization/52424,
	tree-optimization/52429, tree-optimization/52445
  - fix up mangling of operator"" (PR c++/52521)
- decrease size of .debug_ranges by ~ 20% (PR debug/51902)
- add support for demangling operator""
- package %{_prefix}/bin/gcc-{ar,nm,ranlib} binaries for LTO

* Tue Mar  6 2012 Jakub Jelinek <jakub@redhat.com> 4.6.3-2
- backport PLUGIN_FINISH_DECL event support
- adjust 22_locale/num_put/put/char/9780-2.cc testcase for recent
  locale data changes in glibc

* Tue Mar  6 2012 Jakub Jelinek <jakub@redhat.com> 4.6.3-1
- update from the 4.6 branch
  - GCC 4.6.3 release
  - PRs ada/46192, boehm-gc/48514, boehm-gc/52179, bootstrap/49907,
	bootstrap/50888, bootstrap/51686, bootstrap/51969, c++/50608,
	c++/50870, c++/50901, c++/51150, c++/51161, c++/51248, c++/51265,
	c++/51331, c++/51344, c++/51406, c++/51416, c++/51669, c++/51854,
	c++/51868, c++/52247, c/51339, c/51360, c/52181, c/52290, debug/48190,
	debug/49951, debug/51410, debug/51517, debug/51695, debug/51950,
	debug/52260, driver/48306, fortran/47545, fortran/49050,
	fortran/50408, fortran/50684, fortran/50923, fortran/51075,
	fortran/51218, fortran/51310, fortran/51338, fortran/51435,
	fortran/51448, fortran/51502, fortran/51550, fortran/51800,
	fortran/51904, fortran/51913, fortran/51948, fortran/51966,
	fortran/52012, fortran/52022, fortran/52093, fortran/52151,
	fortran/52335, fortran/52386, libjava/48512, libmudflap/40778,
	libstdc++/50862, libstdc++/50880, libstdc++/51083, libstdc++/51133,
	libstdc++/51142, libstdc++/51540, libstdc++/51626, libstdc++/51711,
	libstdc++/51795, libstdc++/52300, libstdc++/52309, libstdc++/52317,
	lto/41159, middle-end/44777, middle-end/45678, middle-end/48071,
	middle-end/48660, middle-end/50074, middle-end/51077,
	middle-end/51323, middle-end/51510, middle-end/51768,
	middle-end/51994, middle-end/52074, middle-end/52140,
	middle-end/52230, rtl-opt/37451, rtl-opt/37782,
	rtl-optimization/38644, rtl-optimization/47918,
	rtl-optimization/48721, rtl-optimization/49720,
	rtl-optimization/50396, rtl-optimization/51187,
	rtl-optimization/51374, rtl-optimization/51469,
	rtl-optimization/51767, rtl-optimization/51821,
	rtl-optimization/52060, rtl-optimization/52139, target/30282,
	target/40068, target/45233, target/48108, target/48743,
	target/49641, target/49992, target/50313, target/50493,
	target/50678, target/50691, target/50875, target/50906,
	target/50945, target/50979, target/51002, target/51106,
	target/51287, target/51345, target/51393, target/51408,
	target/51623, target/51643, target/51756, target/51835,
	target/51921, target/51934, target/52006, target/52107,
	target/52129, target/52199, target/52205, target/52238,
	target/52294, target/52330, target/52408, target/52425,
	testsuite/51511, testsuite/52296, tree-optimization/46886,
	tree-optimization/49536, tree-optimization/49642,
	tree-optimization/50031, tree-optimization/50078,
	tree-optimization/50569, tree-optimization/50622,
	tree-optimization/50969, tree-optimization/51042,
	tree-optimization/51070, tree-optimization/51118,
	tree-optimization/51315, tree-optimization/51466,
	tree-optimization/51485, tree-optimization/51583,
	tree-optimization/51624, tree-optimization/51759,
	tree-optimization/52286
- don't look for lto plugin/lto-wrapper if -E/-S/-c or in cpp (#787345)
- debuginfo related backports from trunk (PRs pch/51722, debug/52165,
  debug/52132)
- fix up ccp from optimizing away non-pure/const builtin passthrough calls
  with constant first argument (PR tree-optimization/51683)

* Wed Feb 29 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.18
- update from trunk
  - PRs boehm-gc/48299, bootstrap/52397, bootstrap/52414, fortran/52386,
	libstdc++/52191, lto/52400, middle-end/51752, target/49448,
	target/51534, target/52148, target/52407, tree-optimization/52395,
	tree-optimization/52402, tree-optimization/53207
  - fix bootstrap on ppc*/arm/s390*

* Mon Feb 27 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.17
- update from trunk
  - PRs boehm-gc/52179, libffi/52223, libstdc++/52188, middle-end/52355,
	middle-end/52361, target/49263, target/49461, target/50580,
	target/52352, target/52375, target/52390, testsuite/52201,
	tree-optimization/52376

* Fri Feb 24 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.16
- update from trunk
  - fix vtable for std::num_get<char, std::istreambuf_iterator<char,
    std::char_traits<char> > > and vtable for std::num_get<wchar_t,
    std::istreambuf_iterator<wchar_t, std::char_traits<wchar_t> > >
    ABI breakage
  - PR bootstrap/52287

* Thu Feb 23 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.15
- update from trunk
  - PRs c/52290, fortran/52335, go/52349, libstdc++/50349, lto/50616,
	middle-end/52329, rtl-optimization/50063, target/18145, target/52330,
	tree-optimization/52019
- disable go on arm again, still not ready there

* Tue Feb 21 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.14
- update from trunk
  - PRs c++/51415, c++/52126, c++/52248, c++/52312, fortran/52295,
	libstdc++/47058, libstdc++/52189, libstdc++/52241, libstdc++/52300,
	libstdc++/52309, libstdc++/52317, middle-end/52141, middle-end/52314,
	rtl-optimization/52208, target/50166, target/51753, target/52137,
	target/52238, target/52294, testsuite/52229, translation/52232,
	translation/52234, translation/52245, translation/52246,
	translation/52262, translation/52273, tree-optimization/52285,
	tree-optimization/52286, tree-optimization/52298,
	tree-optimization/52318, tree-optimization/52324

* Fri Feb 17 2012 Cristian Gafton <gafton@amazon.com>
- add arch-specific provides for the generic names as well for versioned subpackages.
- disable fortran backend when building as a secondary compiler
- fix typo in conditionals used for building as a secondary compiler
- conditionalize fortran build support
- create versioned packages of libgcc and libstdc++ to avoid clobbering the ones from gcc-4.4

* Thu Feb 16 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.13
- update from trunk
  - PRs boehm-gc/48514, bootstrap/52172, c++/39055, c++/51910, c++/52215,
	c/52181, c/52190, debug/52165, debug/52260, driver/48524,
	fortran/32380, fortran/52151, go/48411, go/51874, libffi/52221,
	libitm/52042, libitm/52220, libstdc++/51368, lto/52178,
	middle-end/48600, middle-end/51867, middle-end/51929,
	middle-end/52140, middle-end/52142, middle-end/52177,
	middle-end/52209, middle-end/52214, middle-end/52230,
	rtl-optimization/52175, target/51921, target/52146, target/52199,
	target/52205, target/52261, testsuite/50076, translation/52193,
	translation/52211, translation/52264, tree-optimization/50031,
	tree-optimization/50561, tree-optimization/52210,
	tree-optimization/52244, tree-optimization/52255
  - fix asm goto handling in templates (#790221, PR c++/52247)
- reenable go on ppc/ppc64/s390/s390x/arm

* Sun Feb 12 2012 Cristian Gafton <gafton@amazon.com>
- update virtual provides for debuginfo packages when building as a secondary compiler
- do not split off the libgfortran-static when building as a secondary to avoid conflicts
- provide gcc-go when bulding as a secondary compiler
- create a versioned package name for libmudflap-static when building as a secondary compiler
- keep package for libstc++ standard named and version the -devel when building as a secondary compiler
- noop: update gnat dependencies
- version libmudflap-devel package to make it coexist with others when building as a secondary compiler
- update gfortran packages for building as a secondary compiler
- rename gnat binaries too when compiling as a secondary compiler.
- remove/don't package duplicate lang files when building as a secondary compiler.
- also ship a gcc-$version named binary
- use versioned requires for genetic package name instead of alternate compiler

* Sat Feb 11 2012 Cristian Gafton <gafton@amazon.com>
- fix requires for objc for building as a secondary compiler
- keep libgcc package unversioned
- fix requires for gfortran
- simplify the requires for the gcc-c++ package when built as an secondary compiler
- integrate cc1 into the gcc package when building as  a secondary compiler

* Wed Feb  8 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.12
- update from trunk
  - PRs c++/52035, fortran/51514, gcov-profile/52150, libstdc++/51296,
	libstdc++/51906, middle-end/24306, middle-end/51994,
	middle-end/52074, rtl-optimization/52139, rtl-optimization/52170,
	target/40068, target/52152, target/52154, target/52155,
	tree-optimization/46886
  - fix up build on ppc*
  - don't look for lto plugin/lto-wrapper if -E/-S/-c or in cpp
- move liblto_plugin.so* back into gcc subpackage

* Mon Feb  6 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.11
- update from trunk
  - PRs bootstrap/52039, bootstrap/52041, bootstrap/52058, c++/48680,
	c++/51327, c++/51370, c++/51852, c++/52043, c++/52088, c/52118,
	debug/52001, debug/52027, debug/52048, fortran/32373, fortran/41587,
	fortran/41600, fortran/46356, fortran/48705, fortran/48847,
	fortran/51754, fortran/51808, fortran/51870, fortran/51943,
	fortran/51946, fortran/51953, fortran/51958, fortran/51970,
	fortran/51972, fortran/51977, fortran/52012, fortran/52013,
	fortran/52016, fortran/52022, fortran/52024, fortran/52029,
	fortran/52038, fortran/52093, fortran/52102, go/47656, go/48501,
	libitm/51822, libjava/48512, libstdc++/49445, libstdc++/51649,
	libstdc++/51795, libstdc++/51798, libstdc++/51811, libstdc++/51956,
	libstdc++/52068, libstdc++/52104, libstdc++/52119, libstdc++/52128,
	middle-end/43967, middle-end/47982, middle-end/48071,
	middle-end/51389, middle-end/51959, middle-end/51998,
	middle-end/52047, rtl-optimization/49800, rtl-optimization/51374,
	rtl-optimization/51978, rtl-optimization/52092,
	rtl-optimization/52095, rtl-optimization/52113, target/51500,
	target/51835, target/51871, target/51920, target/51974, target/52079,
	target/52107, target/52125, target/52129, testsuite/51875,
	testsuite/52011, tree-optimization/48794, tree-optimization/50444,
	tree-optimization/50955, tree-optimization/50969,
	tree-optimization/51528, tree-optimization/51990,
	tree-optimization/52020, tree-optimization/52028,
	tree-optimization/52045, tree-optimization/52046,
	tree-optimization/52073, tree-optimization/52091,
	tree-optimization/52115
  - fix i?86 mem += reg; mem cmp 0 8-bit peephole2 (#786570, PR target/52086)
  - fix fortran ICE on elemental call (#785433, PR fortran/52059)
- fix up /lib/cpp symlink for UsrMove (#787460)
- move LTO plugin into cpp subpackage (#787345)
- fix debug ICE with i387 reg-stack (#787518, PR debug/52132)
- fix ARM combine bug (PR rtl-optimization/52060)
- fix a DWARF4 .debug_types DIE cloning bug (PR debug/51950)

* Sat Feb 4 2012 Cristian Gafton <gafton@amazon.com>
- build versioned subpackages for libobjc, libgnat and libgfortran

* Sat Feb  4 2012 Cristian Gafton <gafton@amazon.com> - 4.6.2-1%{?dist}
- update spec to create an alternate compile to the main system gcc

* Sat Feb 4 2012 Cristian Gafton <gafton@amazon.com>
- (re)enable go and ada support
- update spec file to create the gcc46 alternate compiler

* Thu Jan 26 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.10
- update from trunk
  - PRs bootstrap/51985, c++/51223, c++/51812, c++/51917, c++/51928,
	c++/51930, c++/51973, c++/51992, driver/47249, fortran/51966,
	fortran/51995, libstdc++/49829, lto/51698, middle-end/45678,
	middle-end/51986, rtl-optimization/48308, rtl-optimization/48374
  - fix data-ref handling of non-volatile inline asms (#784242,
    PR tree-optimization/51987)
- fix ARM ICE with invalid peephole (#784748, PR target/52006)

* Mon Jan 23 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.9
- update from trunk
  - PRs ada/46192, c++/51344, c++/51398, c++/51402, c++/51832, c++/51919,
	c++/51922, debug/45682, fortran/50556, fortran/51056, fortran/51904,
	fortran/51913, fortran/51948, libgcj/23182, libgfortran/51899,
	libitm/51830, libstdc++/50982, lto/51916, middle-end/45416,
	rtl-optimization/40761, rtl-optimization/51924, target/47096,
	target/49868, target/50313, target/50887, target/51106, target/51819,
	target/51900, target/51915, target/51931, target/51934,
	testsuite/51941, tree-optimization/51895, tree-optimization/51903,
	tree-optimization/51914, tree-optimization/51949
  - fix REE pass (#783481, PR rtl-optimization/51933)
  - further overload fixes with using decls (#783586, PR c++/51925)
- fix ICE during expansion with BLKmode MEM_REF (#782868, PR middle-end/51895)
- fix ppc64 profiledbootstrap (PR target/51957)
- revert broken stack layout change (PR tree-optimization/46590)
- fix ARM ICE on neon insn splitting (PR target/51968)

* Thu Jan 19 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.8
- update from trunk
  - PRs bootstrap/50237, c++/51225, c++/51889, fortran/48426, fortran/51634,
	go/50656, libmudflap/40778, libstdc++/51845, libstdc++/51866,
	lto/51280, middle-end/51192, rtl-optimization/48496,
	rtl-optimization/51505, tree-optimization/37997,
	tree-optimization/46590
- fix a reload bug on s390 (#773565, PR rtl-optimization/51856)

* Tue Jan 17 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.7
- update from trunk
  - PRs bootstrap/51860, c++/14179, c++/20681, c++/50012, c++/51403,
	c++/51620, c++/51633, c++/51714, c++/51777, c++/51813, c++/51827,
	c++/51854, c++/51868, c/12245, fortran/36755, fortran/48351,
	fortran/51800, fortran/51809, fortran/51816, fortran/51842,
	fortran/51869, libitm/51173, libitm/51855, middle-end/51782,
	middle-end/8081, other/51165, rtl-optimization/51821, target/47852,
	target/50925, target/51756, tree-optimization/51865
  - fix up ppc64 bootstrap with -mminimal-toc (#773040, PR bootstrap/51872)
  - fix up -ftree-tail-merge (#782231, PR tree-optimization/51877)
- package up arm and sparc specific headers (#781765)
- enable libitm and disable go on ppc/ppc64
- fix up big-endian libstdc++ miscompilation (PR middle-end/50325)
- fix up arm neon vectorization ICEs (PR target/51876)

* Thu Jan 12 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.6
- update from trunk
  - PRs ada/41929, bootstrap/51705, bootstrap/51796, c++/47450,
	c++/48051, c++/50855, c++/51322, c++/51433, c++/51565,
	c++/51613, c++/51614, c++/51818, c++/6057, debug/51471,
	fortran/51057, fortran/51578, fortran/51616, fortran/51652,
	fortran/51758, fortran/51791, fortran/51792, gcov-profile/50127,
	gcov-profile/51715, gcov-profile/51717, libstdc++/51673,
	middle-end/51516, middle-end/51806, preprocessor/33919,
	preprocessor/51776, rtl-optimization/51271, target/47333,
	rarget/49868, testsuite/51655, tree-optimization/49642,
	tree-optimization/50913, tree-optimization/51600,
	tree-optimization/51680, tree-optimization/51694,
	tree-optimization/51759, tree-optimization/51775,
	tree-optimization/51799, tree-optimization/51801

* Fri Jan  6 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.5
- update from trunk
  - PRs c++/51541, fortran/48946, libstdc++/51504, lto/51774,
	rtl-optimization/51771, target/51681, tree-optimization/51315
- disable go on s390{,x}
- disable profiledbootstrap on arm and sparc* for now

* Thu Jan  5 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.4
- update from trunk
  - PRs bootstrap/51072, bootstrap/51648, debug/51746, debug/51762,
	lto/41576, lto/50490, middle-end/44777, middle-end/49710,
	middle-end/51472, middle-end/51761, middle-end/51764,
	middle-end/51768, other/51171, rtl-optimization/51767,
	tree-optimization/51624, tree-optimization/51760
- disable go on arm (#771482)
- enable profiledbootstrap

* Wed Jan  4 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.3
- update from trunk
  - PRs bootstrap/51006, bootstrap/51734, c++/29273, c++/51064, c++/51738,
	debug/51695, fortran/49693, fortran/50981, middle-end/51696,
	middle-end/51750, other/51163, other/51164, tree-optimization/49651
- fix up libitm.so.1

* Tue Jan  3 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.2
- update from trunk
  - PRs bootstrap/51686, bootstrap/51725, c++/15867, c++/16603, c++/20140,
	c++/23211, c++/51316, c++/51379, c++/51397, c++/51462, c++/51507,
	c++/51547, c++/51666, c++/51669, c++/51675, c++/51723, debug/51650,
	driver/48306, fortran/46262, fortran/46328, fortran/51052,
	fortran/51502, fortran/51529, fortran/51682, libfortran/51646,
	libgcj/49193, libstdc++/48362, libstdc++/49204, libstdc++/51608,
	libstdc++/51701, libstdc++/51711, lto/51650, middle-end/48641,
	middle-end/51200, middle-end/51212, middle-end/51252,
	middle-end/51730, other/51679, pch/51722, rtl-optimization/50396,
	rtl-optimization/51069, rtl-optimization/51667, target/27468,
	target/47643, target/51345, target/51552, target/51623, target/51643,
	target/51729, testsuite/50722, testsuite/51645, testsuite/51702,
	tree-optimization/43491, tree-optimization/51070,
	tree-optimization/51269, tree-optimization/51683,
	tree-optimization/51684, tree-optimization/51692,
	tree-optimization/51704, tree-optimization/51719

* Wed Dec 21 2011 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.1
- new package

* Thu Oct 27 2011 Jakub Jelinek <jakub@redhat.com> 4.6.2-1
- update from the 4.6 branch
  - GCC 4.6.2 release
  - PRs c++/44473, c++/49216, c++/49855, c++/49896, c++/50531, c++/50611,
	c++/50618, c++/50787, c++/50793, c/50565, debug/50816, fortran/47023,
	fortran/48706, fortran/50016, fortran/50273, fortran/50570,
	fortran/50585, fortran/50625, fortran/50659, fortran/50718,
	libobjc/49883, libobjc/50002, libstdc++/48698, middle-end/49801,
	middle-end/50326, middle-end/50386, obj-c++/48275, objc-++/48275,
	target/49049, target/49824, target/49965, target/49967, target/50106,
	target/50350, target/50652, target/50737, target/50788, target/50820,
	tree-optimization/49279, tree-optimization/50189,
	tree-optimization/50700, tree-optimization/50712,
	tree-optimization/50723
- add armv7hl configury options (#746843)
- add `gcc -print-file-name=rpmver` file with gcc NVRA for plugins
  (#744922)
- fix build against current glibc, ctype.h changes broke libjava compilation

* Mon Oct  2 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-10
- update from the 4.6 branch
  - PRs c++/20039, c++/40831, c++/42844, c++/46105, c++/48320, c++/50424,
	c++/50442, c++/50491, c++/50508, inline-asm/50571, libstdc++/49559,
	libstdc++/50509, libstdc++/50510, libstdc++/50529, middle-end/49886,
	target/50091, target/50341, target/50464, testsuite/50487,
	tree-optimization/49518, tree-optimization/49628,
	tree-optimization/49911, tree-optimization/50162,
	tree-optimization/50412, tree-optimization/50413,
	tree-optimization/50472
- recognize IVs with REFERENCE_TYPE in simple_iv similarly to
  IVs with POINTER_TYPE (#528578)
- return larger types for odd-sized precision in Fortran type_for_size
  langhook if possible

* Thu Sep  8 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-9
- update from the 4.6 branch
  - PRs c++/49267, c++/50089, c++/50157, c++/50207, c++/50220, c++/50224,
	c++/50234, c++/50255, c++/50309, c/50179, fortran/50163,
	libffi/49594, libfortran/50192, libstdc++/50268, middle-end/50116,
	middle-end/50266, target/50090, target/50202, target/50289,
	target/50310, tree-optimization/50178
- debug info related backports from the trunk
  - PRs debug/50191, debug/50215
- fix call site debug info on big endian targets (PR debug/50299)
- put libgcc.a into libgcc_s.so linker script also on arm (#733549)
- use %%{?fedora} instead of %%{fedora}, handle 0%%{?rhel} >= 7 like
  0%%{?fedora} >= 16

* Wed Aug 24 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-8
- update from the 4.6 branch
  - PRs c++/46862, c++/48993, c++/49669, c++/49921, c++/49988, c++/50024,
	c++/50054, c++/50086, fortran/49792, fortran/50050, fortran/50109,
	fortran/50129, fortran/50130, middle-end/49923, target/50001,
	target/50092, tree-optimization/48739
- build EH_SPEC_BLOCK with the same location as current function
  to help gcov (#732802, PR c++/50055)
- support used attribute on template class methods and static data
  members for forced instantiation (#722587)
- fix up location copying in the vectorizer (PR tree-optimization/50133)
- unshare CALL_INSN_FUNCTION_USAGE (PR middle-end/48722)
- fix up gthr*.h for -E -C (#713800)

* Thu Aug  4 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-7
- update from the 4.6 branch
  - PRs c++/43886, c++/49593, c++/49803, fortran/49885,
	tree-optimization/49948
- add self_spec support to specs
- add COPYING.RUNTIME to gcc and libgcc docs (#727809)
- SPARC entry_value fixes (PRs target/48220, debug/49815)
- fix up c-family headers in gcc-plugin-devel (#728011, PRs plugins/45348,
  plugins/46577, plugins/48425)

* Tue Aug  2 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-6
- update from the 4.6 branch
  - PRs c++/49260, c++/49924, libstdc++/49925, target/47908, target/49920
  - fix libquadmath on i686 (#726909)
- OpenMP 3.1 support (PR fortran/42041, PR fortran/46752)
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
- make -grecord-gcc-switches the default
%endif

* Sun Jul 31 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-5
- update from the 4.6 branch
  - PRs debug/49871, fortran/48876, fortran/49791, middle-end/49897,
	middle-end/49898, rtl-optimization/49799, target/47364
- don't attempt to size optimize -gdwarf-2 DW_AT_data_member_location
  from DW_OP_plus_uconst form

* Wed Jul 27 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-4
- update from the 4.6 branch
  - PRs ada/49819, c++/49785, debug/47393, fortran/49648, fortran/49708,
	middle-end/49675, middle-end/49732, target/39386, target/49600,
	target/49723, target/49746, testsuite/49753, tree-opt/49671,
	tree-optimization/45819, tree-optimization/49309,
	tree-optimization/49725, tree-optimization/49768
- require gmp-devel, mpfr-devel and libmpc-devel in gcc-plugin-devel
  (#725569)
- backport -grecord-gcc-switches (#507759, PR other/32998)
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
- more compact debug macro info for -g3 - .debug_macro section
- improve call site debug info for some floating point parameters
  passed on the stack (PR debug/49846)
%endif
- fix -mcmodel=large call constraints (PR target/49866, #725516)

* Fri Jul 15 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-3
- update from the 4.6 branch
  - PRs ada/46350, ada/48711, c++/49672, fortran/48926, fortran/49562,
	fortran/49690, fortran/49698, target/39633, target/46779,
	target/49487, target/49541, target/49621, tree-opt/49309,
	tree-optimization/49094, tree-optimization/49651
- backport -march=bdver2 and -mtune=bdver2 support
%if 0%{?fedora} < 16 || 0%{?rhel} >= 7
- use ENTRY_VALUE RTLs internally to improve generated debug info,
  just make sure to remove it from possible options before emitting
  var-tracking notes
%endif

* Fri Jul  8 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-2
- update from the 4.6 branch
  - PRs ada/49511, bootstrap/23656, bootstrap/49247, c++/48157, c/48825,
	c++/49418, c++/49440, c++/49528, c++/49598, c/49644, debug/49262,
	debug/49522, fortran/49466, fortran/49479, fortran/49623,
	libffi/46660, libfortran/49296, middle-end/49640, other/47733,
	regression/47836, rtl-optimization/49014, rtl-optimization/49472,
	rtl-optimization/49619, target/34734, target/47997, target/48273,
	target/49089, target/49335, target/49660, testsuite/49643,
	tree-optimization/38752, tree-optimization/49516,
	tree-optimization/49539, tree-optimization/49572,
	tree-optimization/49615, tree-optimization/49618
  - decrease compiler memory and time requirements on Fortran DATA
    with many times repeated initializers (#716721, PR fortran/49540)
- backport some debuginfo improvements and fixes
  - PRs debug/49364, debug/49602
  - fix typed DWARF stack ICE (#717240, PR49567)
- backport __builtin_assume_aligned support (#713586)
- backport further C++ FE improvements for heavy overloading use
  (#651098, PR c++/48481)

* Mon Jun 27 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-1
- update from the 4.6 branch
  - GCC 4.6.1 release
  - PRs c++/33840, c++/49117, c++/49134, c++/49229, c++/49251, c++/49264,
	c++/49276, c++/49290, c++/49298, c++/49369, c++/49482, c++/49507,
	debug/47590, debug/48459, fortran/47601, fortran/48699,
	fortran/49074, fortran/49103, fortran/49112, fortran/49268,
	fortran/49324, fortran/49417, gcov-profile/49299, middle-end/49191,
	rtl-optimization/48542, rtl-optimization/49235, target/44618,
	target/48454, target/49186, target/49238, target/49307, target/49411,
	target/49461, testsuite/49432, tree-optimization/48613,
	tree-optimization/48702, tree-optimization/49038,
	tree-optimization/49115, tree-optimization/49243,
	tree-optimization/49419
  - fix GCSE (#712480, PR rtl-optimization/49390)
- use rm -f and mv -f in split-debuginfo.sh (#716664)
- backport some debuginfo improvements and bugfixes
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
  - improve debug info for IPA-SRA through DW_OP_GNU_parameter_ref
    (PR debug/47858)
  - emit DW_OP_GNU_convert <0> as convert to untyped
%endif
  - emit .debug_loc empty ranges for parameters that are
    modified even before first insn in a function (PR debug/49382)
  - fix debug ICE on s390x (PR debug/49544)
  - VTA ICE fix (PR middle-end/49308)
- balance work in #pragma omp for schedule(static) better (PR libgomp/49490)

* Fri Jun  3 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-10
- update from the 4.6 branch
  - PRs fortran/45786, fortran/49265, middle-end/48953, middle-end/48985,
	tree-optimization/49093
- backport some debuginfo improvements
  - PRs debug/47919, debug/47994, debug/49250
- decrease C++ FE memory usage on code with heavy overloading
  (#651098, PR c++/48481)

* Mon May 30 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-9
- update from the 4.6 branch
  - PRs c++/44311, c++/44994, c++/45080, c++/45401, c++/45418, c++/45698,
	c++/46005, c++/46245, c++/46696, c++/47049, c++/47184, c++/47277,
	c++/48284, c++/48292, c++/48424, c++/48935, c++/49156, c++/49165,
	c++/49176, c++/49223, fortran/48955, libobjc/48177, libstdc++/49141,
	target/43700, target/43995, target/44643, target/45263,
	tree-optimization/44897, tree-optimization/49161,
	tree-optimization/49217, tree-optimization/49218
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
- default to -gdwarf-4 -fno-debug-types-section instead of -gdwarf-3
- backport DW_OP_GNU_entry_value support
  (PRs rtl-optimization/48826, debug/48902, bootstrap/48148,
   debug/48203, bootstrap/48168, debug/48023, debug/48178,
   debug/48163, debug/48160, bootstrap/48153, middle-end/48152,
   bootstrap/48148, debug/45882)
- backport DW_OP_GNU_{{const,regval,deref}_type,convert,reinterpret}
  support (PRs debug/48928, debug/48853)
%endif
- split off debuginfo for libgcc_s, libstdc++ and libgomp into
  gcc-base-debuginfo subpackage (#706973)
- run ldconfig in libgcc %%postun, drop libcc_post_upgrade,
  instead write the script in <lua> (#705832)

* Wed May 25 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-8
- update from the 4.6 branch
  - PRs bootstrap/49086, c++/47263, c++/47336, c++/47544, c++/48522,
	c++/48617, c++/48647, c++/48736, c++/48745, c++/48780, c++/48859,
	c++/48869, c++/48873, c++/48884, c++/48945, c++/48948, c++/49042,
	c++/49043, c++/49066, c++/49082, c++/49105, c++/49136, c/49120,
	debug/48159, debug/49032, fortran/48889, libstdc++/49058, lto/48207,
	lto/48703, lto/49123, middle-end/48973, middle-end/49029,
	preprocessor/48677, target/48986, target/49002, target/49104,
	target/49128, target/49133, tree-optimization/48172,
	tree-optimization/48794, tree-optimization/48822,
	tree-optimization/48975, tree-optimization/49000,
	tree-optimization/49018, tree-optimization/49039,
	tree-optimization/49073, tree-optimization/49079
  - ppc V2DImode ABI fix (#705764, PR target/48857)
  - fix ppc var-tracking ICE (#703888, PR debug/48967)

* Mon May  9 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-7
- update from the 4.6 branch
  - PRs ada/48844, c++/40975, c++/48089, c++/48446, c++/48656, c++/48749,
	c++/48838, c++/48909, c++/48911, fortran/48112, fortran/48279,
	fortran/48462, fortran/48720, fortran/48746, fortran/48788,
	fortran/48800, fortran/48810, fortran/48894, libgfortran/48030,
	libstdc++/48750, libstdc++/48760, lto/48846, middle-end/48597,
	preprocessor/48192, target/48226, target/48252, target/48262,
	target/48774, target/48900, tree-optimization/48809
- fix ICE with references in templates (PR c++/48574)
- disable tail call optimization if tail recursion needs accumulators
  (PR PR tree-optimization/48837)

* Thu Apr 28 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-6
- update from the 4.6 branch
  - PRs c++/42687, c++/46304, c++/48046, c++/48657, c++/48707, c++/48726,
	c/48685, c/48716, c/48742, debug/48768, fortran/47976,
	fortran/48588, libstdc++/48521, lto/48148, lto/48492,
	middle-end/48695, other/48748, preprocessor/48740, target/48288,
	target/48708, target/48723, tree-optimization/48611,
	tree-optimization/48717, tree-optimization/48731,
	tree-optimization/48734

* Tue Apr 19 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-5
- update from the 4.6 branch
  - PRs c++/48537, c++/48632, fortran/48360, fortran/48456,
	libfortran/47571, libstdc++/48476, libstdc++/48631,
	libstdc++/48635, lto/48538, middle-end/46364, middle-end/48661,
	preprocessor/48248, target/48366, target/48605, target/48614,
	target/48678, testsuite/48675, tree-optimization/48616
  - fix calling functor or non-pointer-to-member through
    overloaded pointer-to-member operator (#695567, PR c++/48594)

* Wed Apr 13 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-4
- update from the 4.6 branch
  - PRs c++/48450, c++/48452, c++/48468, c++/48500, c++/48523, c++/48528,
	c++/48534, c++/48570, c++/48574, c/48517, libstdc++/48465,
	libstdc++/48541, libstdc++/48566, target/47829, target/48090,
	testsuite/48506, tree-optimization/48195, tree-optimization/48377
  - fix combiner with -g (#695019, PR rtl-optimization/48549)
  - fix OpenMP atomic __float128 handling on i?86 (#696129,
    PR middle-end/48591)

* Fri Apr  8 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-3
- update from the 4.6 branch
  - PRs bootstrap/48431, c++/48280, debug/48343, debug/48466, fortran/48117,
	fortran/48291, libstdc++/48398, middle-end/48335,
	rtl-optimization/48143, rtl-optimization/48144, target/16292,
	target/48142
  - don't ICE because of empty partitions during LTO (#688767, PR lto/48246)
- don't emit DW_AT_*_pc for CUs without any code

* Thu Mar 31 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-2
- update from the 4.6 branch
  - PRs c++/47504, c++/47570, c++/47999, c++/48166, c++/48212, c++/48265,
	c++/48281, c++/48289, c++/48296, c++/48313, c++/48319, c++/48369,
	debug/48041, debug/48253, preprocessor/48248, target/48349
- add -fno-debug-types-section switch
- don't emit .debug_abbrev section if it is empty and unused

* Tue Mar 29 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-1
- update from the 4.6 branch
  - GCC 4.6.0 release
  - PRs c/42544, c/48197, debug/48204, middle-end/48031,
	middle-end/48134, middle-end/48269, other/48179, other/48221,
	other/48234, rtl-optimization/48156, target/47553,
	target/48237, testsuite/48251, tree-optimization/48228
  - improve RTL DSE speed with large number of stores (#684900,
    PR rtl-optimization/48141)
- add gnative2ascii binary and man page to libgcj

* Mon Mar 21 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-0.15
- update from the 4.6 branch
  - PRs bootstrap/45381, bootstrap/48135
- fix s390 ICE during address delegitimization (PR target/48213, #689266)

* Fri Mar 18 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-0.14
- update from the 4.6 branch
  - PRs bootstrap/48161, c++/48113, c++/48115, c++/48132, debug/47510,
	debug/48176, libstdc++/48123, middle-end/47405, middle-end/48165,
	target/46778, target/46788, target/48171
- update libstdc++ pretty printers from trunk

* Tue Mar 15 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-0.13
- update from trunk and the 4.6 branch
  - PRs bootstrap/48000, bootstrap/48102, c++/44629, c++/45651, c++/46220,
	c++/46803, c++/47125, c++/47144, c++/47198, c++/47488, c++/47705,
	c++/47808, c++/47957, c++/47971, c++/48003, c++/48008, c++/48015,
	c++/48029, c++/48035, c++/48069, c/47786, debug/47881, debug/48043,
	fortran/47552, fortran/47850, fortran/48054, fortran/48059,
	libfortran/48066, libgfortran/48047, libstdc++/48038, libstdc++/48114,
	lto/47497, lto/48073, lto/48086, middle-end/47968, middle-end/47975,
	middle-end/48044, middle-end/48098, rtl-optimization/47866,
	rtl-optimization/47899, target/45413, target/47719, target/47862,
	target/47986, target/48032, target/48053, testsuite/47954,
	tree-optimization/47127, tree-optimization/47278,
	tree-optimization/47714, tree-optimization/47967,
	tree-optimization/48022, tree-optimization/48063,
	tree-optimization/48067
  - fix var-tracking ICE on s390x (#682410, PR debug/47991)

* Thu Dec 2 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/gcc-4.4.4-13.el6

* Fri Jul 9 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/gcc-4.4.4-5.el6
- import source package RHEL6/gcc-4.4.3-1.el6

* Fri May 7 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/gcc-4.1.1-52.el5
- added submodule prep for package gcc
