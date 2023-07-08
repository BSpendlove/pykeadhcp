from pykeadhcp import Kea
from pykeadhcp.models.dhcp6.subnet import Subnet6
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.exceptions import KeaSubnetNotFoundException
import pytest

"""remote-subnet6 process:
get (non-existent subnet)
add
list
get by id
get by prefix
del by id
del non existent by prefix??
"""


def test_kea_dhcp6_remote_subnet6_get_non_existent(kea_server: Kea):
    with pytest.raises(KeaSubnetNotFoundException):
        kea_server.dhcp6.remote_subnet6_get_by_id(subnet_id=40123)


def test_kea_dhcp6_remote_subnet6_add_subnet(kea_server: Kea):
    subnet = Subnet6(subnet="2001:db8::32/127", id=40123)

    # Create subnet
    response = kea_server.dhcp6.remote_subnet6_set(subnet=subnet, server_tags=["all"])
    assert response.result == 0
    assert len(response.arguments.get("subnets", [])) > 0


def test_kea_dhcp6_remote_subnet6_list(kea_server: Kea):
    subnets = kea_server.dhcp6.remote_subnet6_list(server_tags=["pykeadhcp-1"])
    assert subnets
    assert len(subnets) > 0


def test_kea_dhcp6_remote_subnet6_get_by_id(kea_server: Kea):
    subnet = kea_server.dhcp6.remote_subnet6_get_by_id(subnet_id=40123)
    assert subnet
    assert subnet.id == 40123
    assert subnet.subnet == "2001:db8::32/127"


def test_kea_dhcp6_remote_subnet6_get_by_prefix(kea_server: Kea):
    subnet = kea_server.dhcp6.remote_subnet6_get_by_prefix(prefix="2001:db8::32/127")
    assert subnet
    assert subnet.id == 40123
    assert subnet.subnet == "2001:db8::32/127"


def test_kea_dhcp6_remote_subnet6_del_by_id(kea_server: Kea):
    response = kea_server.dhcp6.remote_subnet6_del_by_id(subnet_id=40123)
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp6_remote_subnet6_del_by_prefix_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.remote_subnet6_del_by_prefix(prefix="2001:db8::32/127")
    assert response.result == 3
    assert response.arguments.get("count") == 0
