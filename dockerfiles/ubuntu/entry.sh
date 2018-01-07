#!/bin/bash

/sbin/ldconfig

/usr/sbin/chroot /mnt/rootfs /usr/bin/apt-get -s upgrade > /mnt/results/apt-get.results

/usr/local/bin/oscap-chroot /mnt/rootfs oval eval --results /mnt/results/ubuntu-results.xml --report /mnt/results/ubuntu-report.html /mnt/results/com.ubuntu.xenial.cve.oval.xml

/usr/bin/dpkg --root /mnt/rootfs --list > /mnt/results/dpkg-list.results
