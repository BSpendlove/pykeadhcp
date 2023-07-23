from pykeadhcp import Kea
from pykeadhcp.models.dhcp6.reservation import Reservation6

"""cache process:Reservation6
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


def test_kea_dhcp6_cache_get_none(kea_server: Kea):
    response = kea_server.dhcp6.cache_get()
    assert len(response) == 0


def test_kea_dhcp6_cache_insert(kea_server: Kea):
    reservation = Reservation6(
        ip_addresses=["2001:db8::33"],
        duid="00:01:00:01:17:96:f9:3a:aa:bb:cc:dd:ee:ff",
    )
    response = kea_server.dhcp6.cache_insert(subnet_id=40123, reservation=reservation)
    assert response.result == 0


def test_kea_dhcp6_cache_get(kea_server: Kea):
    response = kea_server.dhcp6.cache_get()
    assert len(response) > 0


def test_kea_dhcp6_cache_get_by_id(kea_server: Kea):
    response = kea_server.dhcp6.cache_get_by_id(
        identifier_type="duid", identifier="00:01:00:01:17:96:f9:3a:aa:bb:cc:dd:ee:ff"
    )
    assert len(response) > 0


def test_kea_dhcp6_cache_size(kea_server: Kea):
    response = kea_server.dhcp6.cache_size()
    assert response.result == 0
    assert response.arguments.get("size") > 0


def test_kea_dhcp6_cache_remove(kea_server: Kea):
    response = kea_server.dhcp6.cache_remove(subnet_id=40123, ip_address="2001:db8::33")
    assert response.result == 0


def test_kea_dhcp6_cache_get_by_id_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.cache_get_by_id(
        identifier_type="duid", identifier="00:01:00:01:17:96:f9:3a:aa:bb:cc:dd:ee:ff"
    )
    assert len(response) == 0


def test_kea_dhcp6_cache_clear(kea_server: Kea):
    response = kea_server.dhcp6.cache_clear()
    assert response.result == 0


def test_kea_dhcp6_cache_flush(kea_server: Kea):
    response = kea_server.dhcp6.cache_flush(number=123)
    assert response.result == 0


def test_kea_dhcp6_cache_write(kea_server: Kea):
    response = kea_server.dhcp6.cache_write(filepath="/tmp/kea-host-cache.json")
    assert response.result == 0


def test_kea_dhcp6_cache_load(kea_server: Kea):
    response = kea_server.dhcp6.cache_load(filepath="/tmp/kea-host-cache.json")
    assert response.result == 0
