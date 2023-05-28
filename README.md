[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI Status](https://github.com/BSpendlove/pykeadhcp/actions/workflows/python-publish.yml/badge.svg)](https://github.com/BSpendlove/pykeadhcp/actions/workflows/python-publish.yml/badge.svg)

# pykeadhcp
A python module used to interact with the Kea DHCP API daemons (dhcp4, dhcp6, ctrl-agent and ddns) with Pydantic support so your editor support should be pretty, and also provides basic data validation for any models implemented (eg. Subnet4).

## How to use

1. Install the module

```
pip install pykeadhcp
```

2. Import the Kea class

```python
from pykeadhcp import Kea

server = Kea(host="http://localhost", port=8000)
```

3. Call API commands based on the Daemon

```python

subnets_v4 = server.dhcp4.subnet4_list()

for subnet in subnets_v4:
    print(subnet.subnet, subnet.option_data, subnet.relay, subnet.pools_list)
```

4. Utilize the Pydantic models which provide basic data validation

```python
from pykeadhcp.models.dhcp4.subnet import Subnet4

my_subnet = Subnet4(
    id=1234, subnet="192.0.2.32/31", option_data=[{"code": 3, "data": "192.0.2.32"}]
)

create_subnet = server.dhcp4.subnet4_add(subnets=[my_subnet])
print(create_subnet.result, create_subnet.text)

# Note because subnet_cmds hook library is not loaded, we run into an exception here:
# pykeadhcp.exceptions.KeaHookLibraryNotConfiguredException: Hook library 'subnet_cmds' is not configured for 'dhcp4' service. Please ensure this is enabled in the configuration for the 'dhcp4' daemon
```

### Basic Authentication

If you have basic authentication enabled on your Kea Servers, initialize the `Kea` class like this:

```python
from pykeadhcp import Kea

server = Kea(host="http://localhost", port=8000, use_basic_auth=True, username="your-username", password="your-password")
```

## API Reference

All supported commands by the daemons are in the format of the API referenced commands with the exception of replacing any hypthen or space with an underscore. Eg. the `build-report` API command for all daemons is implemented as `build_report` so it heavily ties into the Kea predefined commands when looking at their documentation. Currently everything is built towards Kea 2.2.0. Pydantic variables will replace any hyphens with an underscore however when loading/exporting the data models, it will replace all keys with the hyphen to adhere to the Kea expected variables, ensure that the `KeaBaseModel` (located in `from pykeadhcp.models.generic.base import KeaBaseModel` instead of `from pydantic import BaseModel`) is used when creating any Pydantic models to inherit this functionality.

## Development / Contribution

See [this document which explains the development/setup to contribute to this project](CONTRIBUTING.md)

## Commands Implemented/Tested

See [this document which shows what commands are implemented and tested in the latest release](COMMANDS.md)