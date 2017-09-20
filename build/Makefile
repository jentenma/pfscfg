#############################################################
# Makefile for building the Platform Services Diag image RPM
# 
# Date: 09/29/2016
# Author: Justin Morin
#
#  -------- Building RPMS --------------
#
# pull the needed image pieces
# build the RPM.spec 
#

SHELL := /bin/bash

.SUFFIXES:
base-dir = $(shell cd ..;pwd)
current-dir = $(shell pwd)
rpm-dir   = $(shell cd $(base-dir)/build; pwd)

pfscfg-new-dir            = $(shell cat install_path.txt | sed s/^\\///)
pfscfg-new-base           = $(shell cat install_path.txt | sed s/^\\\(\\/[[:alnum:]]\\+\\\)\\/.*/\\1/)
pfscfg-spec-file = pfscfg.spec

# check if build number is passed in
build-state = development
ifdef BUILD_NUM
    build-state = ${BUILD_NUM}
endif

all: rpm-build
rpm-build: pfscfg-rpm

stage-source:
# Create a directory to place all the files and the sub directories
	@echo "Creating the temp dir ${PWD}/${pfscfg-new-dir}"
	@mkdir -p ${pfscfg-new-dir}
	@cp version.txt ${pfscfg-new-dir}
	@cp template.spec pfscfg.spec
	if [ ! -d ~/rpmbuild/SOURCES/pfscfg ]; \
	then \
		mkdir -p ~/rpmbuild/SOURCES/pfscfg; \
	fi

pfscfg-rpm: stage-source
	@echo "Creating pfscfg RPM"
	@echo "Copying pkg files to ${pfscfg-new-dir}/${pkgdir}"
	@cp -r ${base-dir}/scripts ${pfscfg-new-dir}

	@echo "Adding PFSCFG files to the spec file"
	@find ${pfscfg-new-dir} -type d -print > dirs.txt
	@sed -i 's/^/%dir %attr(755,root,root) \//g' dirs.txt
	@find ${pfscfg-new-dir} -type f -not -name "*.pyc" -print > files.txt
	#find ${pfscfg-new-dir} -type f -print > files.txt
	@sed -i 's/^/%attr(755,root,root) \//g' files.txt
	@cat dirs.txt files.txt >> ${pfscfg-spec-file}
	@rpmbuild --buildroot=${rpm-dir} -ba --define 'build_num ${build-state}' ${rpm-dir}/${pfscfg-spec-file};
	@mv ${current-dir}/noarch/* ${current-dir}/
	@rm -rf ${current-dir}/noarch
	@rm -f ${current-dir}/*src.rpm

clean:
	@rm -rf $(current-dir)/rpms
	@rm -rf ${current-dir}/noarch
	@rm -f ${current-dir}/*.rpm
	@rm -rf $(current-dir)/opt
	@rm -f ${current-dir}/pfscfg.spec
	@rm -f ${current-dir}/files.txt
	@rm -f ${current-dir}/dirs.txt
	@find .. -name "*~" -print | xargs rm -f
	@find .. -name "\#*" -print | xargs rm -f
	@find .. -name "\.\#*" -print | xargs rm -f
