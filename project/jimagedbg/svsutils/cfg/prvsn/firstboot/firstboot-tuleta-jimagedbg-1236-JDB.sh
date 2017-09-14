#!/bin/bash

#
# Install latest Mellanox
#
echo "Updating Mellanox Driver" >> /var/log/firstboot
#/bin/cd /root/mlnx
/bin/tar xvf  /root/mlnx/mlnx-en-4.1-1.0.2.0-rhel7.3-ppc64le.tar -C /root/mlnx >> /var/log/firstboot 2>&1
/root/mlnx/mlnx-en-4.1-1.0.2.0-rhel7.3-ppc64le/install --force >> /var/log/firstboot 2>&1
/etc/init.d/mlnx-en.d restart >> /var/log/firstboot 2>&1
mlogs=`ls /tmp/mlnx*`
echo "Mellanox logs are in $mlogs" >> /var/log/firstboot

fabname=`hostname`-fab
fabip=`cat /etc/hosts | grep $fabname | awk '{print $1}'`
#cat /etc/sysconfig/network-scripts/ifcfg-fbond | sed "s/INSERT_FAB_ADDRESS_HERE/$fabip/g" > /tmp/fbond.tmp
#cp /tmp/fbond.tmp /etc/sysconfig/network-scripts/ifcfg-fbond

mgtname=`hostname`-mgt
mgtip=`cat /etc/hosts | grep $mgtname | awk '{print $1}'`
#cat /etc/sysconfig/network-scripts/ifcfg-mgt0 | sed "s/INSERT_MGT0_ADDRESS_HERE/$mgtip/g" > /tmp/mgt0.tmp
#cp /tmp/mgt0.tmp /etc/sysconfig/network-scripts/ifcfg-mgt0

echo "Configuring mgt0 interface" >> /var/log/firstboot
cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-mgt0
TYPE="Ethernet"
BOOTPROTO="static"
DEFROUTE="no"
PEERDNS="yes"
PEERROUTE="yes"
IPV4_FAILURE_FATAL="no"
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
IPV6_DEFROUTE="yes"
IPV6_PEERDNS="yes"
IPV6_PEERROUTES="yes"
IPV6_FAILURE_FATAL="no"
NAME="mgt0"
DEVICE="mgt0"
IPADDR=$mgtip
NETMASK="255.255.254.0"
EOF
echo "Done Configuring mgt0 interface" >> /var/log/firstboot

echo "Configuring Fabric interface" >> /var/log/firstboot
cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-fab0
NAME=fab0
DEVICE=fab0
BOOTPROTO=none
ONBOOT=yes
NETBOOT=no
IPV6INIT=yes
TYPE=Ethernet
TXQUEUELEN=100000
MASTER=fbond
SLAVE=yes
NM_CONTROLLED=no
EOF

cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-fab1
NAME=fab1
DEVICE=fab1
BOOTPROTO=none
ONBOOT=yes
NETBOOT=no
IPV6INIT=yes
TYPE=Ethernet
TXQUEUELEN=100000
MASTER=fbond
SLAVE=yes
NM_CONTROLLED=no
EOF

cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-fab2
NAME=fab2
DEVICE=fab2
BOOTPROTO=none
ONBOOT=yes
NETBOOT=no
IPV6INIT=yes
TYPE=Ethernet
TXQUEUELEN=100000
MASTER=fbond
SLAVE=yes
NM_CONTROLLED=no
EOF

cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-fab3
NAME=fab3
DEVICE=fab3
BOOTPROTO=none
ONBOOT=yes
NETBOOT=no
IPV6INIT=yes
TYPE=Ethernet
TXQUEUELEN=100000
MASTER=fbond
SLAVE=yes
NM_CONTROLLED=no
EOF

cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-fbond
DEVICE=fbond
NAME=fbond
TYPE=Bond
BONDING_MASTER=YES
ONBOOT=yes
BOOTPROTO=none
NM_CONTROLLED=no
USERCTL=no
IPV6INIT=no
BONDING_OPTS="mode=4 miimon=200 xmit_hash_policy=1 updelay=2000"
MTU=9000
TXQUEUELEN=100000
IPADDR=$fabip
NETMASK=255.255.254.0
EOF

cat <<EOF > /tmp/fbvars.log
$mgtname
$mgtip
$fabname
$fabip
EOF

/sbin/ifdown mgt0
/sbin/ifup mgt0

/sbin/ifdown fab0
/sbin/ifdown fab1
/sbin/ifdown fab2
/sbin/ifdown fab3
/sbin/ifdown fbond
/sbin/ifup fab0
/sbin/ifup fab1
/sbin/ifup fab2
/sbin/ifup fab3
/sbin/ifup fbond
echo "Done Configuring Fabric interface" >> /var/log/firstboot

#
# Always at the end
#
echo "Cleaning up" >> /var/log/firstboot
/bin/cat /etc/crontab | /bin/grep -v firstboot > /etc/crontab.tmp
/bin/cp /etc/crontab /tmp/crontab.fb
/bin/rm -f /etc/crontab
/bin/mv /etc/crontab.tmp /etc/crontab
/bin/cp $0 /tmp/$0.fb
rm -f $0