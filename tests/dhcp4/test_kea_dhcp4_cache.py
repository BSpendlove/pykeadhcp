from pykeadhcp import Kea
from pykeadhcp.models.dhcp4.subnet import Subnet4
from pykeadhcp.models.dhcp4.reservation import Reservation4
import pytest

"""cache process:
cache get (none)
cache insert
cache get
cache get_by_id
cache_size
cache remove
cache get_by_id (non existent)
cache_clear
cache_flush
cache_write
cache_load
"""


def test_kea_dhcp4_cache_get_none(kea_server: Kea):
    response = kea_server.dhcp4.cache_get()
    assert len(response) == 0


def test_kea_dhcp4_cache_insert(kea_server: Kea):
    reservation = Reservation4(ip_address="192.0.2.33", hw_address="aa:bb:cc:dd:ee:ff")
    response = kea_server.dhcp4.cache_insert(subnet_id=40123, reservation=reservation)
    assert response.result == 0


def test_kea_dhcp4_cache_get(kea_server: Kea):
    response = kea_server.dhcp4.cache_get()
    assert len(response) > 0


def test_kea_dhcp4_cache_get_by_id(kea_server: Kea):
    response = kea_server.dhcp4.cache_get_by_id(
        identifier_type="hw-address", identifier="aa:bb:cc:dd:ee:ff"
    )
    assert len(response) > 0


def test_kea_dhcp4_cache_size(kea_server: Kea):
    response = kea_server.dhcp4.cache_size()
    assert response.result == 0
    assert response.arguments.get("size") > 0


def test_kea_dhcp4_cache_remove(kea_server: Kea):
    response = kea_server.dhcp4.cache_remove(subnet_id=40123, ip_address="192.0.2.33")
    assert response.result == 0


def test_kea_dhcp4_cache_get_by_id_non_existent(kea_server: Kea):
    response = kea_server.dhcp4.cache_get_by_id(
        identifier_type="hw-address", identifier="aa:bb:cc:dd:ee:ff"
    )
    assert len(response) == 0


def test_kea_dhcp4_cache_clear(kea_server: Kea):
    response = kea_server.dhcp4.cache_clear()
    assert response.result == 0


def test_kea_dhcp4_cache_flush(kea_server: Kea):
    response = kea_server.dhcp4.cache_flush(number=123)
    assert response.result == 0


def test_kea_dhcp4_cache_write(kea_server: Kea):
    response = kea_server.dhcp4.cache_write(filepath="/tmp/kea-host-cache.json")
    assert response.result == 0


def test_kea_dhcp4_cache_load(kea_server: Kea):
    response = kea_server.dhcp4.cache_load(filepath="/tmp/kea-host-cache.json")
    assert response.result == 0
