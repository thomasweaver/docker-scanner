FROM ubuntu:16.04

WORKDIR /opt
RUN apt-get -y update
RUN apt-get -y install python tar

ADD https://github.com/toolswatch/vFeed/archive/v0.7.2.1.tar.gz /opt/vfeed.tar.gz
WORKDIR /opt
RUN tar -xzf vfeed.tar.gz
RUN mv vFeed-0.7.2.1 vfeed
ADD vfeed.db.tgz /opt/vfeed/vfeed.db.tgz
WORKDIR /opt/vfeed
RUN mv vfeed.db.tgz/vfeed.db .

CMD ["/bin/bash"]

