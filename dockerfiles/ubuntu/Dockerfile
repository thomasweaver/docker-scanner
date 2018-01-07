FROM ubuntu:16.04

WORKDIR /opt
RUN apt-get -y update
RUN apt-get -y install wget libtool automake pkg-config unzip autoconf pkg-config libdbus-1-dev libgconf2-dev libacl1-dev libblkid-dev libcap-dev libcurl4-openssl-dev libgcrypt11-dev libxml2-dev libxslt1-dev make libpcre2-dev libxml-parser-perl libxml-xpath-perl libperl-dev python2.7-dev swig bzip2 libapt-pkg-dev libopenscap8
RUN wget https://github.com/OpenSCAP/openscap/archive/1.2.16.zip
RUN unzip 1.2.16.zip
WORKDIR /opt/openscap-1.2.16
RUN ls -l
RUN /bin/sh autogen.sh
RUN /bin/sh configure --enable-util-scap-as-rpm=no --enable-util-oscap-docker=no
RUN make
RUN make install
RUN /sbin/ldconfig
RUN echo /sbin/ldconfig >> /etc/bash.bashrc
ADD entry.sh /opt/entry.sh

CMD ["bash", "/opt/entry.sh"]
