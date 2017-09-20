#
# PFS diags image RPM
#

# RPM version
%define version %(cat version.txt)

# this will ignore the spec file
%define _unpackaged_files_terminate_build 0
%define _binaries_in_noarch_packages_terminate_build 0

# setup the built directories to be at the current level
%define _rpmdir ./
%define _srcrpmdir ./

# Standard PFS install path from file
%define install_path %(cat install_path.txt)
%define webdir /var/www/images
%define base_install_path %(cat install_path.txt | sed 's$/svsutils$$')
#%define builddir %(cat install_path.txt | sed -s 's/^\\///')/images/pfsimg
%define builddir %(cat install_path.txt | sed -s 's/^\\///')

requires: pfs-software

Summary:Provisioning tools RPM
Name: svsutils
Version: %{version}
Release: %{build_num}
BuildArch: noarch
License: GPL
Group: Firmware
Source: %{install_path}
Distribution: PFS

%description
PFS Provisioning tools and other utilities and such

%prep

%pre

%post
echo "buildir=%{builddir} install_path=%{install_path}"

echo "%{base_install_path}/etc/svsutils.d/prvsn.d"

# defaults for now
fname=setup-saba-clap3-1234-SC3.json
cse=settings-saba-clap3-1234-SC3
fb=firstboot-saba-clap3-1234-SC3.sh
netrules=70-saba-clap3-persistent-net.rules
webdir=/var/www/images

if [ -f /etc/httpd/conf/httpd.conf ]
then 
	webdir=`cat /etc/httpd/conf/httpd.conf | grep ^DocumentRoot | sed 's/\"//g' | awk '{print $2}'`
fi

enable_htx=y
if [ -e %{base_install_path}/etc/MTM ];
then
	mtm=`cat %{base_install_path}/etc/MTM`
	case "$mtm" in
	3452-DB1)
		fname=setup-tuleta-sfv2-${mtm}.json
		cse=settings-tuleta-sfv2-${mtm}
		fb=firstboot-tuleta-sfv2-${mtm}.sh
		netrules=70-tuleta-sfv2-persistent-net.rules
		etchosts=etchosts-tuleta-sfv2
                ;;
        3452-FB1)
		fname=setup-tuleta-sfv2-${mtm}.json
		cse=settings-tuleta-sfv2-${mtm}
		fb=firstboot-tuleta-sfv2-${mtm}.sh
		netrules=70-tuleta-sfv2-persistent-net.rules
		etchosts=etchosts-tuleta-sfv2
                ;;
        3452-GB1)
		fname=setup-tuleta-sfv2-${mtm}.json
		cse=settings-tuleta-sfv2-${mtm}
		fb=firstboot-tuleta-sfv2-${mtm}.sh
		netrules=70-tuleta-sfv2-persistent-net.rules
		etchosts=etchosts-tuleta-sfv2
                ;;
	1234-SC3)
		fname=setup-saba-clap3-${mtm}.json
		cse=settings-saba-clap3-${mtm}
		fb=firstboot-saba-clap3-${mtm}.sh
		netrules=70-saba-clap3-persistent-net.rules
		etchosts=etchosts-saba-clap3
                ;;
	1234-RC3)
		fname=setup-r610-clap3-${mtm}.json
		cse=settings-r610-clap3-${mtm}
		fb=firstboot-r610-clap3-${mtm}.sh
		netrules=70-r610-clap3-persistent-net.rules
		etchosts=etchosts-r610-clap3
		enable_htx=n
                ;;
	1235-SNF)
		fname=setup-saba-svrnfs-${mtm}.json
		cse=settings-saba-svrnfs-${mtm}
		fb=firstboot-saba-svrnfs-${mtm}.sh
		netrules=70-saba-svrnfs-persistent-net.rules
		etchosts=etchosts-saba-svrnfs
		enable_htx=n
                ;;
	1236-JDB)
		fname=setup-tuleta-jimagedbg-${mtm}.json
		cse=settings-tuleta-jimagedbg-${mtm}
		fb=firstboot-tuleta-jimagedbg-${mtm}.sh
		netrules=70-tuleta-jimagedbg-persistent-net.rules
		etchosts=etchosts-tuleta-jimagedbg
		enable_htx=n
                ;;
        esac
fi

echo "fname=${fname}"
echo "cse=${cse}"
echo "fb=${fb}"
echo "netrules=${netrules}"
echo "webdir=${webdir}"

echo "mkdir -p ${webdir}/prvsn-files"
mkdir -p ${webdir}/prvsn-files

echo "mkdir -p %{base_install_path}/etc/svsutils.d/prvsn.d"
mkdir -p %{base_install_path}/etc/svsutils.d/prvsn.d

install -m 644 %{builddir}/scripts/cfg/prvsn/${fname} %{base_install_path}/etc/svsutils.d/prvsn.d/setup.json
install -m 644 %{builddir}/scripts/cfg/prvsn/cobbler/${cse} %{base_install_path}/etc/svsutils.d/prvsn.d/cobbler-settings
install -m 644 %{builddir}/scripts/cfg/logging/logging.json %{base_install_path}/etc/svsutils.d/prvsn.d/logging.json
install -m 644 %{builddir}/scripts/cfg/prvsn/firstboot/${fb}  ${webdir}/prvsn-files/firstboot.sh
install -m 644 %{builddir}/scripts/cfg/prvsn/udev/${netrules} ${webdir}/prvsn-files/70-persistent-net.rules
install -m 644 %{builddir}/scripts/cfg/prvsn/hosts/${etchosts} ${webdir}/prvsn-files/hosts

echo "mkdir -p %{base_install_path}/etc/svsutils.d/sdc.d"
mkdir -p %{base_install_path}/etc/svsutils.d/sdc.d

install -m 644 %{builddir}/scripts/cfg/sdc/${fname} %{base_install_path}/etc/svsutils.d/sdc.d/setup.json
install -m 644 %{builddir}/scripts/cfg/logging/logging.json %{base_install_path}/etc/svsutils.d/sdc.d/logging.json

echo "mkdir -p %{base_install_path}/etc/svsutils.d/sysdiag.d"
mkdir -p %{base_install_path}/etc/svsutils.d/sysdiag.d

install -m 644 %{builddir}/scripts/cfg/sysdiag/${fname} %{base_install_path}/etc/svsutils.d/sysdiag.d/setup.json
install -m 644 %{builddir}/scripts/cfg/logging/logging.json %{base_install_path}/etc/svsutils.d/sysdiag.d/logging.json

if [ "$enable_htx" == "y" ]
then
	echo "mkdir -p %{base_install_path}/etc/svsutils.d/htx.d"
	mkdir -p %{base_install_path}/etc/svsutils.d/htx.d
	install -m 644 %{builddir}/scripts/cfg/htx/${fname} %{base_install_path}/etc/svsutils.d/htx.d/setup.json
	install -m 644 %{builddir}/scripts/cfg/logging/logging.json %{base_install_path}/etc/svsutils.d/htx.d/logging.json
fi

%postun
rm -rf %{base_install_path}/etc/svsutils.d

%clean

%files
