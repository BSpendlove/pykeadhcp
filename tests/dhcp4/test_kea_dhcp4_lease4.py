from pykeadhcp import Kea
from pykeadhcp.exceptions import KeaLeaseNotFoundException
from pykeadhcp.models.dhcp4.subnet import Subnet4
import pytest

"""lease4 process:
get (non-existent lease)
add
add (again to check duplicate lease)
get
get-all
get-page
get-by-client-id
get-by-hw-address
update
del
wipe
reclaim
"""


def test_kea_dhcp4_lease4_get_non_exsistent(kea_server: Kea):
    with pytest.raises(KeaLeaseNotFoundException):
        kea_server.dhcp4.lease4_get(ip_address="192.0.2.32")


def test_kea_dhcp4_lease4_add(kea_server: Kea):
    # Add Temporary Subnet
    data = Subnet4(id=40123, subnet="192.0.2.32/31")
    subnets = [data]
    response = kea_server.dhcp4.subnet4_add(subnets=subnets)
    assert response.result == 0

    # Add Lease
    lease_response = kea_server.dhcp4.lease4_add(
        ip_address="192.0.2.32",
        identifier_key="hw-address",
        identifier_value="aa:bb:cc:11:22:33",
    )

    assert lease_response.result == 0

    delete_response = kea_server.dhcp4.subnet4_del(subnet_id=40123)
    assert delete_response.result == 0


def test_kea_dhcp4_lease4_get(kea_server: Kea):
    response = kea_server.dhcp4.lease4_get(ip_address="192.0.2.32")
    assert response
    assert response.ip_address == "192.0.2.32"
    assert response.hw_address == "aa:bb:cc:11:22:33"


def test_kea_dhcp4_lease4_get_all(kea_server: Kea):
    response = kea_server.dhcp4.lease4_get_all(subnets=[40123])
    assert len(response) > 0


def test_kea_dhcp4_lease4_get_page(kea_server: Kea):
    response = kea_server.dhcp4.lease4_get_page(limit=100, search_from="start")
    assert response.count > 0


def test_kea_dhcp4_lease4_get_by_client_id_non_existent(kea_server: Kea):
    with pytest.raises(KeaLeaseNotFoundException):
        kea_server.dhcp4.lease4_get_by_client_id(client_id="00:00:11:00:00:22")


def test_kea_dhcp4_lease4_get_by_hostname_non_existent(kea_server: Kea):
    with pytest.raises(KeaLeaseNotFoundException):
        kea_server.dhcp4.lease4_get_by_hostname(hostname="bad-hostname")


def test_kea_dhcp4_lease4_get_by_hw_address(kea_server: Kea):
    response = kea_server.dhcp4.lease4_get_by_hw_address(hw_address="aa:bb:cc:11:22:33")
    assert response.ip_address == "192.0.2.32"
    assert response.hw_address == "aa:bb:cc:11:22:33"
    assert response.subnet_id == 40123


def test_kea_dhcp4_lease4_get_by_hw_address_non_existent(kea_server: Kea):
    with pytest.raises(KeaLeaseNotFoundException):
        kea_server.dhcp4.lease4_get_by_hw_address(hw_address="00:00:11:00:00:22")


def test_kea_dhcp4_lease4_del(kea_server: Kea):
    response = kea_server.dhcp4.lease4_del(ip_address="192.0.2.32")
    assert response.result == 0


def test_kea_dhcp4_lease4_del_non_exsistent(kea_server: Kea):
    response = kea_server.dhcp4.lease4_del(ip_address="192.0.2.32")
    assert response.result == 3
