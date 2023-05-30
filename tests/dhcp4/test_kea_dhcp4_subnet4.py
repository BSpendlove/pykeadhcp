from pykeadhcp import Kea
from pykeadhcp.models.dhcp4.subnet import Subnet4
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


def test_kea_dhcp4_subnet4_get_non_existent(kea_server: Kea):
    with pytest.raises(KeaSubnetNotFoundException):
        kea_server.dhcp4.subnet4_get(subnet_id=40123)


def test_kea_dhcp4_subnet4_add(kea_server: Kea):
    data = Subnet4(id=40123, subnet="192.0.2.32/31")
    subnets = [data]
    response = kea_server.dhcp4.subnet4_add(subnets=subnets)
    assert response.result == 0


def test_kea_dhcp4_subnet4_add_existing(kea_server: Kea):
    data = Subnet4(id=40123, subnet="192.0.2.32/31")
    subnets = [data]
    response = kea_server.dhcp4.subnet4_add(subnets=subnets)
    assert response.result == 1


def test_kea_dhcp4_subnet4_list(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_list()
    assert response


def test_kea_dhcp4_subnet4_get(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_get(subnet_id=40123)
    assert response
    assert response.id == 40123


def test_kea_dhcp4_subnet4_delta_add(kea_server: Kea):
    data = Subnet4(
        id=40123,
        subnet="192.0.2.32/31",
        min_valid_lifetime=5000,
        max_valid_lifetime=7000,
        option_data=[{"code": 3, "data": "192.0.2.32"}],
    )
    subnets = [data]

    response = kea_server.dhcp4.subnet4_delta_add(subnets=subnets)
    assert response.result == 0


def test_kea_dhcp4_subnet4_delta_delete(kea_server: Kea):
    data = Subnet4(
        id=40123,
        subnet="192.0.2.32/31",
        min_valid_lifetime=5000,
        max_valid_lifetime=7000,
        option_data=[{"code": 3, "data": "192.0.2.32"}],
    )
    subnets = [data]
    response = kea_server.dhcp4.subnet4_delta_del(subnets=subnets)
    assert response.result == 0

    updated_subnet = kea_server.dhcp4.subnet4_get(subnet_id=40123)
    assert updated_subnet
    assert updated_subnet.max_valid_lifetime != 7000


def test_kea_dhcp4_subnet4_update(kea_server: Kea):
    data = Subnet4(
        id=40123,
        subnet="192.0.2.32/31",
    )
    subnets = [data]
    response = kea_server.dhcp4.subnet4_update(subnets=subnets)
    assert response.result == 0

    updated_subnet = kea_server.dhcp4.subnet4_get(subnet_id=40123)
    assert updated_subnet
    assert len(updated_subnet.option_data) == 0


def test_kea_dhcp4_subnet4_del(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_del(subnet_id=40123)
    assert response.result == 0


def test_kea_dhcp4_subnet4_del_non_existent(kea_server: Kea):
    with pytest.raises(KeaSubnetNotFoundException):
        kea_server.dhcp4.subnet4_del(subnet_id=40123)
