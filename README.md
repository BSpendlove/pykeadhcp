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

## Development / Contribution

See [this document which explains the development/setup to contribute to this project](https://github.com/BSpendlove/pykeadhcp/blob/main/CONTRIBUTING.md)