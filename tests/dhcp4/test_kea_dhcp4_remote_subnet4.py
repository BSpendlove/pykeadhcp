from pykeadhcp import Kea
from pykeadhcp.models.dhcp4.subnet import Subnet4
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.exceptions import KeaSubnetNotFoundException
import pytest

"""subnet4 process:
get (non-existent subnet)
add
add (again to check duplicate subnets)
list
get
delta-add (partial update code 3 option and valid-lifetime)
delta-del (remove valid-lifetime)
update (full update without option 3... should disappear)
del
"""


def test_kea_dhcp4_remote_subnet4_add_subnet(kea_server: Kea):
    name = "pykeadhcp-pytest"

    # Create Temporary Subnet
    data = Subnet4(subnet="192.0.2.32/31", id=40123, shared_network_name=name)
    subnets = [data]

    # Create subnet with shared network assosication
    response = kea_server.dhcp4.remote_subnet4_set(subnets=subnets, server_tags=["all"])
    assert response.result == 0
    assert len(response.arguments.get("subnets", [])) > 0


def test_kea_dhcp4_remote_subnet4_del_by_id(kea_server: Kea):
    response = kea_server.dhcp4.remote_subnet4_del_by_id(id=40123)
    assert response.result == 0
    assert response.arguments.get("count") == 1
