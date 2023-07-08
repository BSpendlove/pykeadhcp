from pykeadhcp import Kea
from pykeadhcp.models.generic.option_def import OptionDef
from pykeadhcp.models.generic.option_data import OptionData
import pytest

"""remote-option-def4 process:

get (non existent)
set
get
get-all
del
"""


def test_kea_dhcp4_remote_option4_global_get_non_existent(kea_server: Kea):
    response = kea_server.dhcp4.remote_option4_global_get(
        option_code=6, option_space="dhcp4", server_tag="all"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0


def test_kea_dhcp4_remote_option4_global_set(kea_server: Kea):
    option_data = OptionData(name="domain-name-servers", data="192.0.2.111")
    response = kea_server.dhcp4.remote_option4_global_set(
        option_data=option_data, server_tag="all"
    )
    assert response.result == 0
    assert len(response.arguments.get("options", [])) > 0


def test_kea_dhcp4_remote_option4_global_del(kea_server: Kea):
    response = kea_server.dhcp4.remote_option4_global_del(
        option_code=6, option_space="dhcp4", server_tag="all"
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp4_remote_option4_global_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp4.remote_option4_global_del(
        option_code=6, option_space="dhcp4", server_tag="all"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0
