from pykeadhcp import Kea
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.models.dhcp6.shared_network import SharedNetwork6

"""remote-option6-network process:

del (non existent)
set
del
"""


def test_kea_dhcp6_remote_option6_network_prepare(kea_server: Kea):
    shared_network = SharedNetwork6(name="pykeadhcp-network")
    response = kea_server.dhcp6.remote_network6_set(
        shared_networks=[shared_network], server_tags=["all"]
    )
    assert response.result == 0


def test_kea_dhcp6_remote_option6_network_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.remote_option6_network_del(
        shared_network="pykeadhcp-network", option_code=6, option_space="dhcp6"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0


def test_kea_dhcp6_remote_option6_network_set(kea_server: Kea):
    option_data = OptionData(name="dns-servers", data="2001:db8::111")
    response = kea_server.dhcp6.remote_option6_network_set(
        shared_network="pykeadhcp-network", option_data=option_data
    )
    assert response.result == 0
    assert len(response.arguments.get("options", [])) > 0


def test_kea_dhcp6_remote_option6_network_del(kea_server: Kea):
    response = kea_server.dhcp6.remote_option6_network_del(
        shared_network="pykeadhcp-network", option_code=23, option_space="dhcp6"
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp6_remote_option6_network_cleanup(kea_server: Kea):
    response = kea_server.dhcp6.remote_network6_del(
        name="pykeadhcp-network", keep_subnets=False
    )
    assert response.result == 0
