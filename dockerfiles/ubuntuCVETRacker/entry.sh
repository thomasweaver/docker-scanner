#!/bin/bash

if [ ! -d /mnt/data ]; then
	echo "No /mnt/data found quitting"
	exit 1
fi

cd /opt/bzr-pulls/ubuntu-cve-tracker
/usr/bin/bzr pull

cd /opt
/usr/bin/python ubuntu-vuln-sql.py
