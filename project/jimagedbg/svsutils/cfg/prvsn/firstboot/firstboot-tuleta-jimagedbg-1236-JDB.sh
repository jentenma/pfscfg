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
