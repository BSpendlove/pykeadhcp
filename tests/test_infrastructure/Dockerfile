FROM ubuntu:20.04

ARG KEA_VERSION=2.2.0
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    automake libtool pkg-config build-essential ccache \
    libboost-all-dev libssl-dev liblog4cplus-dev \
    curl apt-transport-https ca-certificates && \
    curl -RL -O "https://ftp.isc.org/isc/kea/${KEA_VERSION}/kea-${KEA_VERSION}.tar.gz" && \
    tar xvzf kea-${KEA_VERSION}.tar.gz

RUN cd kea-${KEA_VERSION} && \
    autoreconf --install && \
    ./configure && \
    make && \
    make install && \
    ldconfig

ADD start.sh script.sh

CMD ["bash", "./script.sh"]