from pykeadhcp import Kea
from pykeadhcp.models.dhcp4.shared_network import SharedNetwork4
from pykeadhcp.models.dhcp4.subnet import Subnet4
from pykeadhcp.exceptions import KeaSharedNetworkNotFoundException
import pytest

"""network4 process:
get (non-existent network)
add
add (again to check duplicate subnets)
get
update (full update without option 3... should disappear)
del
del (non-existent)
list
"""


def test_kea_dhcp4_remote_network4_get_non_existent(kea_server: Kea):
    name = "pykeadhcp-pytest"
    with pytest.raises(KeaSharedNetworkNotFoundException):
        kea_server.dhcp4.remote_network4_get(name=name)


def test_kea_dhcp4_remote_network4_add(kea_server: Kea):
    name = "pykeadhcp-pytest"
    data = SharedNetwork4(name=name)
    shared_networks = [data]
    response = kea_server.dhcp4.remote_network4_set(
        shared_networks=shared_networks, server_tags=["all"]
    )

    assert response.result == 0
    assert len(response.arguments.get("shared-networks", [])) > 0


def test_kea_dhcp4_remote_network4_get(kea_server: Kea):
    name = "pykeadhcp-pytest"
    shared_network = kea_server.dhcp4.remote_network4_get(name=name)
    assert shared_network
    assert shared_network.name == name


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


def test_kea_dhcp4_remote_network4_del(kea_server: Kea):
    response = kea_server.dhcp4.remote_network4_del(
        name="pykeadhcp-pytest", keep_subnets=False
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp4_remote_network4_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp4.remote_network4_del(name="pykeadhcp-pytest")
    assert response.result == 3
    assert response.arguments["count"] == 0
