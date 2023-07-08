from pykeadhcp import Kea
from pykeadhcp.exceptions import KeaSharedNetworkNotFoundException
import pytest

"""remote-global-parameter6 process:

get (non existent)
set
get
get-all
del
"""


def test_kea_dhcp6_remote_global_parameter6_get_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.remote_global_parameter6_get(
        parameter="t1-percent", server_tag="pykeadhcp-1"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0


def test_kea_dhcp6_remote_global_parameter6_set(kea_server: Kea):
    response = kea_server.dhcp6.remote_global_parameter6_set(
        parameters={"t1-percent": 0.85}, server_tag="all"
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp6_remote_global_parameter6_get(kea_server: Kea):
    response = kea_server.dhcp6.remote_global_parameter6_get(
        parameter="t1-percent", server_tag="all"
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp6_remote_global_parameter6_get_all(kea_server: Kea):
    response = kea_server.dhcp6.remote_global_parameter6_get_all(server_tag="all")
    assert response.result == 0
    assert len(response.arguments.get("parameters")) > 0


def test_kea_dhcp6_remote_global_parameter6_del(kea_server: Kea):
    response = kea_server.dhcp6.remote_global_parameter6_del(
        parameter="t1-percent", server_tag="all"
    )
    assert response.result == 0


def test_kea_dhcp6_remote_global_parameter6_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.remote_global_parameter6_del(
        parameter="t1-percent", server_tag="all"
    )
    assert response.result == 3
