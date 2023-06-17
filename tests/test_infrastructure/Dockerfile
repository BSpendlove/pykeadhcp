ARG KEA_REPO=public/isc/kea-2-2
ARG KEA_VERSION=2.2.0-isc20220726061131
# Indicate if the premium packages should be installed.
# Valid values: "premium" or empty.
ARG KEA_PREMIUM=""


FROM debian:10.13-slim AS debian-base

# Container with a modern Supervisord installled.
FROM debian-base AS supervisor-base
RUN apt-get update \
        && apt-get install \
        -y \
        --no-install-recommends \
        python3.7=3.7.* \
        python3-pip=18.* \
        python3-setuptools=40.8.* \
        wget \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && python3.7 -m pip install --no-cache-dir supervisor==4.2 \
        && mkdir -p /var/log/supervisor

# Server containers
FROM supervisor-base AS server
ENTRYPOINT [ "/bin/sh", "-c", \
        "supervisord -c /etc/supervisor/supervisord.conf" ]
EXPOSE 8080
HEALTHCHECK CMD [ "supervisorctl", "status " ]

FROM supervisor-base AS kea-base
# Install Kea dependencies
RUN apt-get update \
        && apt-get install \
        -y \
        --no-install-recommends \
        curl=7.64.* \
        apt-transport-https=1.8.* \
        gnupg=2.2.* \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Install Kea from Cloudsmith
SHELL [ "/bin/bash", "-o", "pipefail", "-c" ]
ARG KEA_REPO
ARG KEA_VERSION
RUN wget --no-verbose -O- https://dl.cloudsmith.io/${KEA_REPO}/setup.deb.sh | bash \
        && apt-get update \
        && apt-get install \
        --no-install-recommends \
        -y \
        python3-isc-kea-connector=${KEA_VERSION} \
        isc-kea-ctrl-agent=${KEA_VERSION} \
        isc-kea-dhcp4-server=${KEA_VERSION} \
        isc-kea-dhcp6-server=${KEA_VERSION} \
        isc-kea-admin=${KEA_VERSION} \
        isc-kea-common=${KEA_VERSION} \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && mkdir -p /var/run/kea/

# Install premium packages. The KEA_REPO variable must
# be set to the private repository and include an access token.
# Docker ignores this section if the KEA_PREMIUM is empty - thanks
# to this, the image builds correctly when the token is unknown.
FROM kea-base AS keapremium-base
ARG KEA_PREMIUM
ARG KEA_VERSION
# Execute only if the premium is enabled
RUN [ "${KEA_PREMIUM}" != "premium" ] || ( \
        apt-get update \
        && apt-get install \
        --no-install-recommends \
        -y \
        isc-kea-premium-host-cmds=${KEA_VERSION} \
        isc-kea-premium-forensic-log=${KEA_VERSION} \
        isc-kea-premium-host-cache=${KEA_VERSION} \
        isc-kea-premium-radius=${KEA_VERSION} \
        isc-kea-premium-flex-id=${KEA_VERSION} \
        isc-kea-premium-subnet-cmds=${KEA_VERSION} \
        isc-kea-premium-lease-cmds=${KEA_VERSION} \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && mkdir -p /var/run/kea/ \
        )

ENTRYPOINT [ "/bin/sh", "-c", \
        "supervisord -c /etc/supervisor/supervisord.conf" ]
EXPOSE 8080
HEALTHCHECK CMD [ "supervisorctl", "status " ]