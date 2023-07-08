from pykeadhcp import Kea
from pykeadhcp.models.dhcp6.shared_network import SharedNetwork6
from pykeadhcp.models.dhcp6.subnet import Subnet6
from pykeadhcp.exceptions import KeaSharedNetworkNotFoundException
import pytest

"""remote-network6 process:
get (non-existent network)
add
list
get
add and delete subnet (for existing shared-network)
del
del (non-existent)
"""


def test_kea_dhcp6_remote_network6_get_non_existent(kea_server: Kea):
    name = "pykeadhcp-pytest"
    with pytest.raises(KeaSharedNetworkNotFoundException):
        kea_server.dhcp6.remote_network6_get(name=name)


def test_kea_dhcp6_remote_network6_add(kea_server: Kea, db_remote_map: dict):
    name = "pykeadhcp-pytest"
    data = SharedNetwork6(name=name)
    shared_networks = [data]
    response = kea_server.dhcp6.remote_network6_set(
        shared_networks=shared_networks, server_tags=["all"], remote_map=db_remote_map
    )

    assert response.result == 0
    assert len(response.arguments.get("shared-networks", [])) > 0


def test_kea_dhcp6_remote_network6_list(kea_server: Kea, db_remote_map: dict):
    shared_networks = kea_server.dhcp6.remote_network6_list(
        server_tags=["pykeadhcp-1"], remote_map=db_remote_map
    )
    assert shared_networks
    assert len(shared_networks) > 0


def test_kea_dhcp6_remote_network6_get(kea_server: Kea, db_remote_map: dict):
    name = "pykeadhcp-pytest"
    shared_network = kea_server.dhcp6.remote_network6_get(
        name=name, remote_map=db_remote_map
    )
    assert shared_network
    assert shared_network.name == name


def test_kea_dhcp6_remote_subnet6_add_subnet(kea_server: Kea, db_remote_map: dict):
    name = "pykeadhcp-pytest"

    # Create Temporary Subnet
    subnet = Subnet6(subnet="2001:db8::32/127", id=40123, shared_network_name=name)

    # Create subnet with shared network assosication
    response = kea_server.dhcp6.remote_subnet6_set(
        subnet=subnet, server_tags=["all"], remote_map=db_remote_map
    )
    assert response.result == 0
    assert len(response.arguments.get("subnets", [])) > 0


def test_kea_dhcp6_remote_subnet6_del_by_id(kea_server: Kea, db_remote_map: dict):
    response = kea_server.dhcp6.remote_subnet6_del_by_id(
        subnet_id=40123, remote_map=db_remote_map
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp6_remote_network6_del(kea_server: Kea, db_remote_map: dict):
    response = kea_server.dhcp6.remote_network6_del(
        name="pykeadhcp-pytest", keep_subnets=False, remote_map=db_remote_map
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp6_remote_network6_del_non_existent(
    kea_server: Kea, db_remote_map: dict
):
    response = kea_server.dhcp6.remote_network6_del(
        name="pykeadhcp-pytest", remote_map=db_remote_map
    )
    assert response.result == 3
    assert response.arguments["count"] == 0
