[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# pykeadhcp
A python module used to interact the the Kea DHCP API daemons (dhcp4, dhcp6, ctrl-agent and ddns)

## How to use

1. Install the module

```
pip install pykeadhcp
```

2. Import the Kea class

```python
from pykeadhcp import Kea

server = Kea(host="http://192.168.0.102", port=8000)
```

3. Call API commands based on the Daemon

```python

subnets_v4 = server.dhcp4.subnet4_list()
subnets_v6 = server.dhcp6.subnet6_list()
```

## API Reference

All supported commands by the daemons are in the format of the API referenced commands with the exception of replacing any hypthen or space with an underscore. Eg. the `build-report` API command for all daemons is implemented as `build_report` so it heavily ties into the Kea predefined commands when looking at their documentation. Currently everything is built towards Kea 2.2.0.

## Commands supported

### control-agent (ca)

| Command | Implemented | Tested |
| --- | --- | --- |
| build-report | :white_check_mark: | - |
| config-get | :white_check_mark: | - |
| config-reload | :white_check_mark: | - |
| config-set | :white_check_mark: | - |
| config-test | :white_check_mark: | - |
| config-write | :white_check_mark: | - |
| list-commands | :white_check_mark: | - |
| shutdown | :white_check_mark: | - |
| status-get | :white_check_mark: | - |
| version-get | :white_check_mark: | - |

### ddns

| Command | Implemented | Tested |
| --- | --- | --- |
| build-report | - | - |
| config-get | - | - |
| config-reload | - | - |
| config-set | - | - |
| config-test | - | - |
| config-write | - | - |
| gss-tsig-get | - | - |
| gss-tsig-get-all | - | - |
| gss-tsig-key-del | - | - |
| gss-tsig-key-expire | - | - |
| gss-tsig-key-get | - | - |
| gss-tsig-list | - | - |
| gss-tsig-purge | - | - |
| gss-tsig-purge-all | - | - |
| gss-tsig-rekey | - | - |
| gss-tsig-rekey-all | - | - |
| list-commands | - | - |
| shutdown | - | - |
| statistic-get | - | - |
| statistic-get-all | - | - |
| statistic-reset | - | - |
| statistic-reset-all | - | - |
| status-get | - | - |
| version-get | - | - |

### dhcp4

| Command | Implemented | Tested |
| --- | --- | --- |
| build-report | - | - |
| cache-clear | - | - |
| cache-flush | - | - |
| cache-get | - | - |
| cache-get-by-id | - | - |
| cache-insert | - | - |
| cache-load | - | - |
| cache-remove | - | - |
| cache-size | - | - |
| cache-write | - | - |
| class-add | - | - |
| class-del | - | - |
| class-get | - | - |
| class-list | - | - |
| class-update | - | - |
| config-backend-pull | - | - |
| config-get | - | - |
| config-reload | - | - |
| config-set | - | - |
| config-test | - | - |
| config-write | - | - |
| dhcp-disable | - | - |
| dhcp-enable | - | - |
| ha-continue | - | - |
| ha-heartbeat | - | - |
| ha-maintenance-cancel | - | - |
| ha-maintenance-notify | - | - |
| ha-maintenance-start | - | - |
| ha-reset | - | - |
| ha-scopes | - | - |
| ha-sync | - | - |
| ha-sync-complete-notify | - | - |
| lease4-add | - | - |
| lease4-del | - | - |
| lease4-get | - | - |
| lease4-get-all | - | - |
| lease4-get-by-client-id | - | - |
| lease4-get-by-hostname | - | - |
| lease4-get-by-hw-address | - | - |
| lease4-get-page | - | - |
| lease4-resend-ddns | - | - |
| lease4-update | - | - |
| lease4-wipe | - | - |
| leases-reclaim | - | - |
| libreload | - | - |
| list-commands | - | - |
| network4-add | - | - |
| network4-del | - | - |
| network4-get | - | - |
| network4-list | - | - |
| network4-subnet-add | - | - |
| network4-subnet-del | - | - |
| remote-class4-del | - | - |
| remote-class4-get | - | - |
| remote-class4-get-all | - | - |
| remote-class4-set | - | - |
| remote-global-parameter4-del | - | - |
| remote-global-parameter4-get | - | - |
| remote-global-parameter4-get-all | - | - |
| remote-global-parameter4-set | - | - |
| remote-network4-del | - | - |
| remote-network4-get | - | - |
| remote-network4-list | - | - |
| remote-network4-set | - | - |
| remote-option-def4-del | - | - |
| remote-option-def4-get | - | - |
| remote-option-def4-get-all | - | - |
| remote-option-def4-set | - | - |
| remote-option4-global-del | - | - |
| remote-option4-global-get | - | - |
| remote-option4-global-get-all | - | - |
| remote-option4-global-set | - | - |
| remote-option4-network-del | - | - |
| remote-option4-network-set | - | - |
| remote-option4-pool-del | - | - |
| remote-option4-pool-set | - | - |
| remote-option4-subnet-del | - | - |
| remote-option4-subnet-set | - | - |
| remote-server4-del | - | - |
| remote-server4-get | - | - |
| remote-server4-get-all | - | - |
| remote-server4-set | - | - |
| remote-subnet4-del-by-id | - | - |
| remote-subnet4-del-by-prefix | - | - |
| remote-subnet4-get-by-id | - | - |
| remote-subnet4-get-by-prefix | - | - |
| remote-subnet4-list | - | - |
| remote-subnet4-set | - | - |
| reservation-add | - | - |
| reservation-del | - | - |
| reservation-get | - | - |
| reservation-get-all | - | - |
| reservation-get-by-hostname | - | - |
| reservation-get-by-id | - | - |
| reservation-get-page | - | - |
| server-tag-get | - | - |
| shutdown | - | - |
| stat-lease4-get | - | - |
| statistic-get | - | - |
| statistic-get-all | - | - |
| statistic-remove | - | - |
| statistic-remove-all | - | - |
| statistic-reset | - | - |
| statistic-reset-all | - | - |
| statistic-sample-age-set | - | - |
| statistic-sample-age-set-all | - | - |
| statistic-sample-count-set | - | - |
| statistic-sample-count-set-all | - | - |
| status-get | - | - |
| subnet4-add | - | - |
| subnet4-del | - | - |
| subnet4-delta-add | - | - |
| subnet4-delta-del | - | - |
| subnet4-get | - | - |
| subnet4-list | - | - |
| subnet4-update | - | - |
| version-get | - | - |

### dhcp6

| Command | Implemented | Tested |
| --- | --- | --- |
| build-report | - | - |
| cache-clear | - | - |
| cache-flush | - | - |
| cache-get | - | - |
| cache-get-by-id | - | - |
| cache-insert | - | - |
| cache-load | - | - |
| cache-remove | - | - |
| cache-size | - | - |
| cache-write | - | - |
| class-add | - | - |
| class-del | - | - |
| class-get | - | - |
| class-list | - | - |
| class-update | - | - |
| config-backend-pull | - | - |
| config-get | - | - |
| config-reload | - | - |
| config-set | - | - |
| config-test | - | - |
| config-write | - | - |
| dhcp-disable | - | - |
| dhcp-enable | - | - |
| ha-continue | - | - |
| ha-heartbeat | - | - |
| ha-maintenance-cancel | - | - |
| ha-maintenance-notify | - | - |
| ha-maintenance-start | - | - |
| ha-reset | - | - |
| ha-scopes | - | - |
| ha-sync | - | - |
| ha-sync-complete-notify | - | - |
| lease6-add | - | - |
| lease6-bulk-apply | - | - |
| lease6-del | - | - |
| lease6-get | - | - |
| lease6-get-all | - | - |
| lease6-get-by-duid | - | - |
| lease6-get-by-hostname | - | - |
| lease6-get-page | - | - |
| lease6-resend-ddns | - | - |
| lease6-update | - | - |
| lease6-wipe | - | - |
| leases-reclaim | - | - |
| libreload | - | - |
| list-commands | - | - |
| network6-add | - | - |
| network6-del | - | - |
| network6-get | - | - |
| network6-list | - | - |
| network6-subnet-add | - | - |
| network6-subnet-del | - | - |
| remote-class6-del | - | - |
| remote-class6-get | - | - |
| remote-class6-get-all | - | - |
| remote-class6-set | - | - |
| remote-global-parameter6-del | - | - |
| remote-global-parameter6-get | - | - |
| remote-global-parameter6-get-all | - | - |
| remote-global-parameter6-set | - | - |
| remote-network6-del | - | - |
| remote-network6-get | - | - |
| remote-network6-list | - | - |
| remote-network6-set | - | - |
| remote-option-def6-del | - | - |
| remote-option-def6-get | - | - |
| remote-option-def6-get-all | - | - |
| remote-option-def6-set | - | - |
| remote-option6-global-del | - | - |
| remote-option6-global-get | - | - |
| remote-option6-global-get-all | - | - |
| remote-option6-global-set | - | - |
| remote-option6-network-del | - | - |
| remote-option6-network-set | - | - |
| remote-option6-pd-pool-del | - | - |
| remote-option6-pd-pool-set | - | - |
| remote-option6-pool-del | - | - |
| remote-option6-pool-set | - | - |
| remote-option6-subnet-del | - | - |
| remote-option6-subnet-set | - | - |
| remote-server6-del | - | - |
| remote-server6-get | - | - |
| remote-server6-get-all | - | - |
| remote-server6-set | - | - |
| remote-subnet6-del-by-id | - | - |
| remote-subnet6-del-by-prefix | - | - |
| remote-subnet6-get-by-id | - | - |
| remote-subnet6-get-by-prefix | - | - |
| remote-subnet6-list | - | - |
| remote-subnet6-set | - | - |
| reservation-add | - | - |
| reservation-del | - | - |
| reservation-get | - | - |
| reservation-get-all | - | - |
| reservation-get-by-hostname | - | - |
| reservation-get-by-id | - | - |
| reservation-get-page | - | - |
| server-tag-get | - | - |
| shutdown | - | - |
| stat-lease6-get | - | - |
| statistic-get | - | - |
| statistic-get-all | - | - |
| statistic-remove | - | - |
| statistic-remove-all | - | - |
| statistic-reset | - | - |
| statistic-reset-all | - | - |
| statistic-sample-age-set | - | - |
| statistic-sample-age-set-all | - | - |
| statistic-sample-count-set | - | - |
| statistic-sample-count-set-all | - | - |
| status-get | - | - |
| subnet6-add | - | - |
| subnet6-del | - | - |
| subnet6-delta-add | - | - |
| subnet6-delta-del | - | - |
| subnet6-get | - | - |
| subnet6-list | - | - |
| subnet6-update | - | - |
| version-get | - | - |

## Development / Contribution

See [this document which explains the development/setup to contribute to this project](https://github.com/BSpendlove/pykeadhcp/blob/main/CONTRIBUTING.md)