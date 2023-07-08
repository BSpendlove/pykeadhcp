from pykeadhcp import Kea
from pykeadhcp.models.generic.option_def import OptionDef
from pykeadhcp.models.generic.option_data import OptionData

"""remote-option-def6 process:

get (non existent)
set
get
get-all
del
"""


def test_kea_dhcp6_remote_option6_global_get_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.remote_option6_global_get(
        option_code=23, option_space="dhcp6", server_tag="all"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0


def test_kea_dhcp6_remote_option6_global_set(kea_server: Kea):
    option_data = OptionData(name="dns-servers", data="2001:db8::111")
    response = kea_server.dhcp6.remote_option6_global_set(
        option_data=option_data, server_tag="all"
    )
    assert response.result == 0
    assert len(response.arguments.get("options", [])) > 0


def test_kea_dhcp6_remote_option6_global_del(kea_server: Kea):
    response = kea_server.dhcp6.remote_option6_global_del(
        option_code=23, option_space="dhcp6", server_tag="all"
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp6_remote_option6_global_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp6.remote_option6_global_del(
        option_code=23, option_space="dhcp6", server_tag="all"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0
