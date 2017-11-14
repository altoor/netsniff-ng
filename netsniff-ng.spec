Name:		netsniff-ng
Version:	0.6.3
Release:	5%{?dist}
Summary:	Packet sniffing beast
Group:		Applications/Internet
License:	GPLv2
URL:		http://netsniff-ng.org/
Source0:	http://www.netsniff-ng.org/pub/netsniff-ng/netsniff-ng-%{version}.tar.xz
BuildRequires:	ncurses-devel GeoIP-devel libnetfilter_conntrack-devel
BuildRequires:	userspace-rcu-devel libnl3-devel libcli-devel flex bison
BuildRequires:	perl-podlators zlib-devel libpcap-devel libnet-devel
BuildRequires:	libsodium-devel
# rhbz#1111779, this should be probably dropped in f23 or later
Provides:	mausezahn = 0.40-9
Obsoletes:	mausezahn < 0.40-9

%description
netsniff-ng is a high performance Linux network sniffer for packet inspection.
It can be used for protocol analysis, reverse engineering or network
debugging. The gain of performance is reached by 'zero-copy' mechanisms, so
that the kernel does not need to copy packets from kernelspace to userspace.

netsniff-ng toolkit currently consists of the following utilities:

* netsniff-ng: the zero-copy sniffer, pcap capturer and replayer itself.
* trafgen: a high performance zero-copy network packet generator.
* ifpps: a top-like kernel networking and system statistics tool.
* curvetun: a lightweight curve25519-based multiuser IP tunnel.
* ashunt: an autonomous system trace route and ISP testing utility.
* flowtop: a top-like netfilter connection tracking tool.
* bpfc: a tiny Berkeley Packet Filter compiler supporting Linux extensions.

%prep
%setup -q

%build
export NACL_INC_DIR=$(pkg-config --variable=includedir libsodium )/sodium
export NACL_LIB=sodium
# the current configure script doesn't support unknown options, thus we cannot
# use the generic %%configure macro
./configure --prefix='%{_prefix}' --sysconfdir='%{_sysconfdir}'
make %{?_smp_mflags} ETCDIR=%{_sysconfdir} Q= STRIP=: \
  CFLAGS="%{optflags} -fPIC" LDFLAGS="%{?__global_ldflags}"

%install
make install PREFIX=%{_prefix} ETCDIR=%{_sysconfdir} DESTDIR="%{buildroot}"

%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING README
%{_sbindir}/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_mandir}/man8/*
