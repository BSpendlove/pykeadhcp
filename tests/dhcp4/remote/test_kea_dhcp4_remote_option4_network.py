from pykeadhcp import Kea
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.models.dhcp4.shared_network import SharedNetwork4

"""remote-option4-network process:

del (non existent)
set
del
"""


def test_kea_dhcp4_remote_option4_network_prepare(kea_server: Kea):
    shared_network = SharedNetwork4(name="pykeadhcp-network")
    response = kea_server.dhcp4.remote_network4_set(
        shared_networks=[shared_network], server_tags=["all"]
    )
    assert response.result == 0


def test_kea_dhcp4_remote_option4_network_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp4.remote_option4_network_del(
        shared_network="pykeadhcp-network", option_code=6, option_space="dhcp4"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0


def test_kea_dhcp4_remote_option4_network_set(kea_server: Kea):
    option_data = OptionData(name="domain-name-servers", data="192.0.2.111")
    response = kea_server.dhcp4.remote_option4_network_set(
        shared_network="pykeadhcp-network", option_data=option_data
    )
    assert response.result == 0
    assert len(response.arguments.get("options", [])) > 0


def test_kea_dhcp4_remote_option4_network_del(kea_server: Kea):
    response = kea_server.dhcp4.remote_option4_network_del(
        shared_network="pykeadhcp-network", option_code=6, option_space="dhcp4"
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp4_remote_option4_network_cleanup(kea_server: Kea):
    response = kea_server.dhcp4.remote_network4_del(
        name="pykeadhcp-network", keep_subnets=False
    )
    assert response.result == 0
