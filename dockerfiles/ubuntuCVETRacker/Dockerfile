FROM ubuntu:16.04

WORKDIR /opt
RUN apt-get -y --fix-missing update && apt-get install -y python bzr && apt-get -y autoremove && mkdir bzr-pulls
WORKDIR /opt/bzr-pulls
RUN bzr branch lp:ubuntu-cve-tracker

WORKDIR /opt/
COPY ubuntu-vuln-sql.py  ubuntu-vuln-sql.py
COPY entry.sh entry.sh

CMD ["/bin/bash", "entry.sh"]

