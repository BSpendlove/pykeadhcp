from pykeadhcp import Kea
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.models.dhcp6.subnet import Subnet6

"""remote-option6-subnet process:

del (non existent)
set
del
"""


def test_kea_dhcp6_remote_option6_subnet_prepare(kea_server: Kea):
    subnet = Subnet6(id=40123, subnet="2001:db8::/64")
    response = kea_server.dhcp6.remote_subnet6_set(subnet=subnet, server_tags=["all"])
    assert response.result == 0


def test_kea_dhcp6_remote_option6_subnet_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.remote_option6_subnet_del(
        subnet_id=40123, option_code=23, option_space="dhcp6"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0


def test_kea_dhcp6_remote_option6_subnet_set(kea_server: Kea):
    option_data = OptionData(name="dns-servers", data="2001:db8::111")
    response = kea_server.dhcp6.remote_option6_subnet_set(
        subnet_id=40123, option_data=option_data
    )
    assert response.result == 0
    assert len(response.arguments.get("options", [])) > 0


def test_kea_dhcp6_remote_option6_subnet_del(kea_server: Kea):
    response = kea_server.dhcp6.remote_option6_subnet_del(
        subnet_id=40123, option_code=23, option_space="dhcp6"
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp6_remote_option6_subnet_cleanup(kea_server: Kea):
    response = kea_server.dhcp6.remote_subnet6_del_by_id(subnet_id=40123)
    assert response.result == 0
