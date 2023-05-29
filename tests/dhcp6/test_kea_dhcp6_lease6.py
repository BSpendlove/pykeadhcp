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

    delete_response = kea_server.dhcp6.subnet6_del(subnet_id=40123)
    assert delete_response.result == 0


def test_kea_dhcp6_lease6_get(kea_server: Kea):
    response = kea_server.dhcp6.lease6_get(ip_address="2001:db8::32")
    assert response
    assert response.ip_address == "2001:db8::32"
    assert response.duid == "1a:1b:1c:1d:1e:1f:20:21:22:23:24"
    assert response.iaid == 1234


def test_kea_dhcp6_lease6_del(kea_server: Kea):
    response = kea_server.dhcp6.lease6_del(ip_address="2001:db8::32")
    assert response.result == 0
