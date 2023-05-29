from pykeadhcp import Kea
from pykeadhcp.models.dhcp6.subnet import Subnet6
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


def test_kea_dhcp6_subnet6_get_non_existent(kea_server: Kea):
    with pytest.raises(KeaSubnetNotFoundException):
        response = kea_server.dhcp6.subnet6_get(subnet_id=40123)


def test_kea_dhcp6_subnet6_add(kea_server: Kea):
    data = Subnet6(id=40123, subnet="2001:db8::/64")
    subnets = [data]
    response = kea_server.dhcp6.subnet6_add(subnets=subnets)
    assert response.result == 0


def test_kea_dhcp6_subnet6_add_existing(kea_server: Kea):
    data = Subnet6(id=40123, subnet="2001:db8::/64")
    subnets = [data]
    response = kea_server.dhcp6.subnet6_add(subnets=subnets)
    assert response.result == 1


def test_kea_dhcp6_subnet6_list(kea_server: Kea):
    response = kea_server.dhcp6.subnet6_list()
    assert response


def test_kea_dhcp6_subnet6_get(kea_server: Kea):
    response = kea_server.dhcp6.subnet6_get(subnet_id=40123)
    assert response
    assert response.id == 40123
