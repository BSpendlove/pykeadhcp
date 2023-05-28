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
subnet-add
subnet-del
update (full update without option 3... should disappear)
del
list
"""


def test_kea_dhcp4_network4_get_non_existent(kea_server: Kea):
    name = "pykeadhcp-pytest"
    with pytest.raises(KeaSharedNetworkNotFoundException):
        response = kea_server.dhcp4.network4_get(name=name)


def test_kea_dhcp4_network4_add(kea_server: Kea):
    name = "pykeadhcp-pytest"
    data = SharedNetwork4(name=name)
    shared_networks = [data]
    response = kea_server.dhcp4.network4_add(shared_networks)
    assert response.result == 0


def test_kea_dhcp4_network4_add_duplicate(kea_server: Kea):
    name = "pykeadhcp-pytest"
    data = SharedNetwork4(name=name)
    shared_networks = [data]
    response = kea_server.dhcp4.network4_add(shared_networks)
    assert response.result == 1


def test_kea_dhcp4_network4_get(kea_server: Kea):
    name = "pykeadhcp-pytest"
    response = kea_server.dhcp4.network4_get(name=name)
    assert response
    assert response.name == name


def test_kea_dhcp4_network4_subnet_add(kea_server: Kea):
    name = "pykeadhcp-pytest"

    # Create Temporary Subnet
    data = Subnet4(subnet="192.0.2.32/31", id=40123)
    subnets = [data]
    subnet = kea_server.dhcp4.subnet4_add(subnets=subnets)
    assert subnet.result == 0

    # Assign Subnet to existing shared network
    response = kea_server.dhcp4.network4_subnet_add(name=name, subnet_id=data.id)
    assert response.result == 0

    # Confirm shared-network has at least 1 subnet
    shared_network = kea_server.dhcp4.network4_get(name=name)
    assert shared_network
    assert len(shared_network.subnet4) == 1


def test_kea_dhcp4_network4_subnet_del(kea_server: Kea):
    name = "pykeadhcp-pytest"

    # Delete temporary subnet assosication
    response = kea_server.dhcp4.network4_subnet_del(name=name, subnet_id=40123)
    assert response.result == 0

    # Delete Temporary Subnet
    deleted_subnet = kea_server.dhcp4.subnet4_del(subnet_id=40123)
    assert deleted_subnet.result == 0

    # Confirm Shared Network now has 0 subnets
    shared_network = kea_server.dhcp4.network4_get(name=name)
    assert shared_network
    assert len(shared_network.subnet4) == 0


def test_kea_dhcp4_network4_del(kea_server: Kea):
    name = "pykeadhcp-pytest"
    response = kea_server.dhcp4.network4_del(name=name)
    assert response.result == 0
