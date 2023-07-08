from pykeadhcp import Kea
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.models.dhcp4.subnet import Subnet4
from pykeadhcp.models.generic.pool import Pool

"""remote-option4-pool process:

del (non existent)
set
del
"""


def test_kea_dhcp4_remote_option4_pool_prepare(kea_server: Kea):
    subnet = Subnet4(
        id=40123, subnet="192.0.2.0/24", pools=[Pool(pool="192.0.2.100-192.0.2.200")]
    )
    response = kea_server.dhcp4.remote_subnet4_set(subnet=subnet, server_tags=["all"])
    assert response.result == 0


def test_kea_dhcp4_remote_option4_pool_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp4.remote_option4_pool_del(
        pool="192.0.2.100-192.168.0.200", option_code=6, option_space="dhcp4"
    )
    assert response.result == 3
    assert response.arguments.get("count") == 0


def test_kea_dhcp4_remote_option4_pool_set(kea_server: Kea):
    option_data = OptionData(name="domain-name-servers", data="192.0.2.111")
    response = kea_server.dhcp4.remote_option4_pool_set(
        pool="192.0.2.100-192.0.2.200", option_data=option_data
    )
    assert response.result == 0
    assert len(response.arguments.get("options", [])) > 0


def test_kea_dhcp4_remote_option4_pool_del(kea_server: Kea):
    response = kea_server.dhcp4.remote_option4_pool_del(
        pool="192.0.2.100-192.0.2.200", option_code=6, option_space="dhcp4"
    )
    assert response.result == 0
    assert response.arguments.get("count") == 1


def test_kea_dhcp4_remote_option4_pool_cleanup(kea_server: Kea):
    response = kea_server.dhcp4.remote_subnet4_del_by_id(subnet_id=40123)
    assert response.result == 0
