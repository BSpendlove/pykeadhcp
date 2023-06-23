from pykeadhcp import Kea
from pykeadhcp.exceptions import KeaLeaseNotFoundException
from pykeadhcp.models.dhcp6.subnet import Subnet6
import pytest

"""lease6 process:
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


def test_kea_dhcp6_lease6_get_non_exsistent(kea_server: Kea):
    with pytest.raises(KeaLeaseNotFoundException):
        kea_server.dhcp6.lease6_get(ip_address="2001:db8::32")


def test_kea_dhcp4_lease6_get_all_none(kea_server: Kea):
    with pytest.raises(KeaLeaseNotFoundException):
        kea_server.dhcp6.lease6_get_all()


def test_kea_dhcp6_lease6_add(kea_server: Kea):
    # Add Temporary Subnet
    data = Subnet6(id=40123, subnet="2001:db8::/64")
    subnets = [data]
    response = kea_server.dhcp6.subnet6_add(subnets=subnets)
    assert response.result == 0

    # Add Lease
    lease_response = kea_server.dhcp6.lease6_add(
        ip_address="2001:db8::32", duid="1a:1b:1c:1d:1e:1f:20:21:22:23:24", iaid=1234
    )
    assert lease_response.result == 0


def test_kea_dhcp6_lease6_get(kea_server: Kea):
    response = kea_server.dhcp6.lease6_get(ip_address="2001:db8::32")
    assert response
    assert response.ip_address == "2001:db8::32"
    assert response.duid == "1a:1b:1c:1d:1e:1f:20:21:22:23:24"
    assert response.iaid == 1234


def test_kea_dhcp4_lease6_get_all(kea_server: Kea):
    response = kea_server.dhcp6.lease6_get_all()
    assert len(response) > 0


def test_kea_dhcp6_lease6_get_all_subnets(kea_server: Kea):
    response = kea_server.dhcp6.lease6_get_all(subnets=[40123])
    assert len(response) > 0


def test_kea_dhcp6_lease6_get_page(kea_server: Kea):
    response = kea_server.dhcp6.lease6_get_page(limit=100, search_from="start")
    assert response.count > 0


def test_kea_dhcp6_lease6_get_by_duid(kea_server: Kea):
    response = kea_server.dhcp6.lease6_get_by_duid(
        duid="1a:1b:1c:1d:1e:1f:20:21:22:23:24"
    )
    assert response
    assert response.type == "IA_NA"
    assert response.ip_address == "2001:db8::32"
    assert response.duid == "1a:1b:1c:1d:1e:1f:20:21:22:23:24"
    assert response.iaid == 1234


def test_kea_dhcp6_lease6_get_by_hostname_non_existent(kea_server: Kea):
    with pytest.raises(KeaLeaseNotFoundException):
        kea_server.dhcp6.lease6_get_by_hostname(hostname="bad-hostname")


def test_kea_dhcp6_lease6_update(kea_server: Kea):
    response = kea_server.dhcp6.lease6_update(
        ip_address="2001:db8::32",
        duid="1a:1b:1c:1d:1e:1f:20:21:22:23:25",
        iaid=1234,
        hostname="new-hostname",
    )
    assert response.result == 0

    updated_lease = kea_server.dhcp6.lease6_get(ip_address="2001:db8::32")
    assert updated_lease.hostname == "new-hostname"


def test_kea_dhcp6_lease6_del(kea_server: Kea):
    response = kea_server.dhcp6.lease6_del(ip_address="2001:db8::32")
    assert response.result == 0


def test_kea_dhcp6_lease6_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.lease6_del(ip_address="2001:db8::32")
    assert response.result == 3


def test_kea_dhcp6_lease6_del_temp_subnet(kea_server: Kea):
    delete_response = kea_server.dhcp6.subnet6_del(subnet_id=40123)
    assert delete_response.result == 0
