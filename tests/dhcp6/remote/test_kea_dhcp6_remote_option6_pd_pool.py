from pykeadhcp import Kea
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.models.dhcp6.subnet import Subnet6
from pykeadhcp.models.dhcp6.pd_pool import PDPool

"""remote-option6-pd-pool process:

del (non existent)
set
del
"""


def test_kea_dhcp6_remote_option6_pd_pool_prepare(kea_server: Kea):
    subnet = Subnet6(
        id=40123,
        subnet="2001:db8::/64",
        pd_pools=[PDPool(prefix="2001:1db8::", prefix_len=38, delegated_len=56)],
    )
    response = kea_server.dhcp6.remote_subnet6_set(subnet=subnet, server_tags=["all"])
    assert response.result == 0


def test_kea_dhcp6_remote_option6_pd_pool_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.remote_option6_pd_pool_del(
        prefix="2001:1db8::", prefix_len=38, option_code=23, option_space="dhcp6"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0


def test_kea_dhcp6_remote_option6_pd_pool_set(kea_server: Kea):
    option_data = OptionData(name="dns-servers", data="2001:db8::111")
    response = kea_server.dhcp6.remote_option6_pd_pool_set(
        prefix="2001:1db8::", prefix_len=38, option_data=option_data
    )
    assert response.result == 0
    assert len(response.arguments.get("options", [])) > 0


def test_kea_dhcp6_remote_option6_pd_pool_del(kea_server: Kea):
    response = kea_server.dhcp6.remote_option6_pd_pool_del(
        prefix="2001:1db8::", prefix_len=38, option_code=23, option_space="dhcp6"
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp6_remote_option6_pd_pool_cleanup(kea_server: Kea):
    response = kea_server.dhcp6.remote_subnet6_del_by_id(subnet_id=40123)
    assert response.result == 0


"""
def test_kea_dhcp6_remote_option6_pool_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.remote_option6_pool_del(
        pool="2001:db8::2-2001:db8::ffff", option_code=23, option_space="dhcp6"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0


def test_kea_dhcp6_remote_option6_pool_set(kea_server: Kea):
    option_data = OptionData(name="dns-servers", data="2001:db8::111")
    response = kea_server.dhcp6.remote_option6_pool_set(
        pool="2001:db8::2-2001:db8::ffff", option_data=option_data
    )
    assert response.result == 0
    assert len(response.arguments.get("options", [])) > 0


def test_kea_dhcp6_remote_option6_pool_del(kea_server: Kea):
    response = kea_server.dhcp6.remote_option6_pool_del(
        pool="2001:db8::2-2001:db8::ffff", option_code=23, option_space="dhcp6"
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1

"""
