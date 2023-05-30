from pykeadhcp import Kea
from pykeadhcp.models.dhcp6.shared_network import SharedNetwork6
from pykeadhcp.models.dhcp6.subnet import Subnet6
from pykeadhcp.exceptions import KeaSharedNetworkNotFoundException
import pytest

"""network4 process:
get (non-existent network)
add
add (again to check duplicate subnets)
list
get
subnet-add
subnet-del
update (full update without option 3... should disappear)
del
"""


def test_kea_dhcp6_network6_get_non_existent(kea_server: Kea):
    name = "pykeadhcp-pytest"
    with pytest.raises(KeaSharedNetworkNotFoundException):
        response = kea_server.dhcp6.network6_get(name=name)


def test_kea_dhcp6_network6_add(kea_server: Kea):
    name = "pykeadhcp-pytest"
    data = SharedNetwork6(name=name)
    shared_networks = [data]
    response = kea_server.dhcp6.network6_add(shared_networks=shared_networks)
    assert response.result == 0


def test_kea_dhcp6_network6_add_duplicate(kea_server: Kea):
    name = "pykeadhcp-pytest"
    data = SharedNetwork6(name=name)
    shared_networks = [data]
    response = kea_server.dhcp6.network6_add(shared_networks)
    assert response.result == 1


def test_kea_dhcp6_network6_get(kea_server: Kea):
    name = "pykeadhcp-pytest"
    response = kea_server.dhcp6.network6_get(name=name)
    assert response
    assert response.name == name


def test_kea_dhcp6_network6_list(kea_server: Kea):
    networks = kea_server.dhcp6.network6_list()
    assert networks
    assert len(networks) > 0


def test_kea_dhcp6_network6_subnet_add(kea_server: Kea):
    name = "pykeadhcp-pytest"

    # Create Temporary Subnet
    data = Subnet6(subnet="2001:db8::/64", id=40123)
    subnets = [data]
    subnet = kea_server.dhcp6.subnet6_add(subnets=subnets)
    assert subnet.result == 0

    # Assign Subnet to existing shared network
    response = kea_server.dhcp6.network6_subnet_add(name=name, subnet_id=data.id)
    assert response.result == 0

    # Confirm shared-network has at least 1 subnet
    shared_network = kea_server.dhcp6.network6_get(name=name)
    assert shared_network
    assert len(shared_network.subnet6) == 1


def test_kea_dhcp6_network6_subnet_del(kea_server: Kea):
    name = "pykeadhcp-pytest"

    # Delete temporary subnet assosication
    response = kea_server.dhcp6.network6_subnet_del(name=name, subnet_id=40123)
    assert response.result == 0

    # Delete Temporary Subnet
    deleted_subnet = kea_server.dhcp6.subnet6_del(subnet_id=40123)
    assert deleted_subnet.result == 0

    # Confirm Shared Network now has 0 subnets
    shared_network = kea_server.dhcp6.network6_get(name=name)
    assert shared_network
    assert len(shared_network.subnet6) == 0


def test_kea_dhcp6_network6_del(kea_server: Kea):
    name = "pykeadhcp-pytest"
    response = kea_server.dhcp6.network6_del(name=name)
    assert response.result == 0
