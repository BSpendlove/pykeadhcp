from pykeadhcp import Kea
import pytest

"""subnet4 process:
get (non-existent subnet)
add
add (again to check duplicate subnets)
get
delta-add (partial update code 3 option and valid-lifetime)
delta-del (remove valid-lifetime)
update (full update without option 3... should disappear)
del
list
"""


def test_kea_dhcp4_subnet4_get_non_existent(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_get(subnet_id=40123)
    assert response["result"] == 3


def test_kea_dhcp4_subnet4_add(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_add(
        subnets=[{"id": 40123, "subnet": "192.0.2.32/31"}]
    )
    assert response["result"] == 0


def test_kea_dhcp4_subnet4_add_existing(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_add(
        subnets=[{"id": 40123, "subnet": "192.0.2.32/31"}]
    )
    assert response["result"] == 1


def test_kea_dhcp4_subnet4_get(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_get(subnet_id=40123)
    assert response["result"] == 0


def test_kea_dhcp4_subnet4_delta_add(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_delta_add(
        subnets=[
            {
                "id": 40123,
                "subnet": "192.0.2.32/31",
                "min-valid-lifetime": 5000,
                "max-valid-lifetime": 7000,
                "option-data": [{"code": 3, "data": "192.0.2.32"}],
                "valid-lifetime": 5678,
            }
        ]
    )
    assert response["result"] == 0


def test_kea_dhcp4_subnet4_delta_delete(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_delta_del(
        subnets=[
            {
                "id": 40123,
                "subnet": "192.0.2.32/31",
                "valid-lifetime": 0,
                "min-valid-lifetime": 0,
                "max-valid-lifetime": 0,
            }
        ]
    )
    assert response["result"] == 0
    updated_subnet = kea_server.dhcp4.subnet4_get(subnet_id=40123)
    assert updated_subnet["arguments"]["subnet4"][0]["max-valid-lifetime"] != 7000


def test_kea_dhcp4_subnet4_update(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_update(
        subnets=[{"id": 40123, "subnet": "192.0.2.32/31"}]
    )
    assert response["result"] == 0
    updated_subnet = kea_server.dhcp4.subnet4_get(subnet_id=40123)
    assert not updated_subnet["arguments"]["subnet4"][0]["option-data"]


def test_kea_dhcp4_subnet4_del(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_del(subnet_id=40123)
    assert response["result"] == 0


def test_kea_dhcp4_subnet4_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_del(subnet_id=40123)
    assert response["result"] == 3


def test_kea_dhcp4_subnet4_list(kea_server: Kea):
    response = kea_server.dhcp4.subnet4_list()
    assert response["result"] == 0
