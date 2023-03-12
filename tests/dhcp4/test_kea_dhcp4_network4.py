from pykeadhcp import Kea
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
    response = kea_server.dhcp4.network4_get(name="pykeadhcp-pytest")
    assert response["result"] == 3


def test_kea_dhcp4_network4_add(kea_server: Kea):
    response = kea_server.dhcp4.network4_add(
        shared_networks=[
            {"name": "pykeadhcp-pytest", "user-context": {"comment": "pytest"}}
        ]
    )
    assert response["result"] == 0


def test_kea_dhcp4_network4_add_duplicate(kea_server: Kea):
    response = kea_server.dhcp4.network4_add(
        shared_networks=[
            {"name": "pykeadhcp-pytest", "user-context": {"comment": "pytest"}}
        ]
    )
    assert response["result"] == 1


def test_kea_dhcp4_network4_get(kea_server: Kea):
    response = kea_server.dhcp4.network4_get(name="pykeadhcp-pytest")
    assert response["result"] == 0


def test_kea_dhcp4_network4_subnet_add(kea_server: Kea):
    # Create temporary subnet
    subnet = kea_server.dhcp4.subnet4_add(
        subnets=[{"id": 40123, "subnet": "192.0.2.32/31"}]
    )
    assert subnet["result"] == 0

    # assign subnet to our existing shared-network
    response = kea_server.dhcp4.network4_subnet_add(
        name="pykeadhcp-pytest", subnet_id=40123
    )
    assert response["result"] == 0

    # Confirm shared-network has 1 subnet
    shared_network = kea_server.dhcp4.network4_get(name="pykeadhcp-pytest")
    assert shared_network["result"] == 0
    assert len(shared_network["arguments"]["shared-networks"][0]["subnet4"]) == 1


def test_kea_dhcp4_network4_subnet_del(kea_server: Kea):
    # Delete temporary subnet assosication
    subnet = kea_server.dhcp4.network4_subnet_del(
        name="pykeadhcp-pytest", subnet_id=40123
    )
    assert subnet["result"] == 0

    # Delete temporary subnet
    deleted_subnet = kea_server.dhcp4.subnet4_del(subnet_id=40123)
    assert deleted_subnet["result"] == 0

    # Confirm shared-network has no subnets
    shared_network = kea_server.dhcp4.network4_get(name="pykeadhcp-pytest")
    assert shared_network["result"] == 0

    assert len(shared_network["arguments"]["shared-networks"][0]["subnet4"]) == 0


def test_kea_dhcp4_network4_del(kea_server: Kea):
    response = kea_server.dhcp4.network4_del(name="pykeadhcp-pytest")
    assert response["result"] == 0
