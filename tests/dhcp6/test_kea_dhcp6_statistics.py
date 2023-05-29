from pykeadhcp import Kea


def test_kea_dhcp6_statistic_get_all(kea_server: Kea):
    response = kea_server.dhcp6.statistic_get_all()
    assert response.result == 0
