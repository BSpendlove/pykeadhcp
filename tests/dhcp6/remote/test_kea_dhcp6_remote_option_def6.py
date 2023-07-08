from pykeadhcp import Kea
from pykeadhcp.models.generic.option_def import OptionDef
import pytest

"""remote-option-def6 process:

get (non existent)
set
get
get-all
del
"""


def test_kea_dhcp6_remote_option_def6_get_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.remote_option_def6_get(
        option_code=1, option_space="pykeadhcp", server_tag="all"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0


def test_kea_dhcp6_remote_option_def6_set(kea_server: Kea):
    option_def = OptionDef(name="subopt1", code=1, space="pykeadhcp", type="string")
    response = kea_server.dhcp6.remote_option_def6_set(
        option_def=option_def, server_tag="all"
    )
    assert response.result == 0
    assert len(response.arguments.get("option-defs", [])) > 0


def test_kea_dhcp6_remote_option_def6_del(kea_server: Kea):
    response = kea_server.dhcp6.remote_option_def6_del(
        option_code=1, option_space="pykeadhcp", server_tag="all"
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp6_remote_option_def6_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.remote_option_def6_del(
        option_code=1, option_space="pykeadhcp", server_tag="all"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0
