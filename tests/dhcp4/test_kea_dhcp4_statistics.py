from pykeadhcp import Kea


def test_kea_dhcp4_statistic_get_all(kea_server: Kea):
    response = kea_server.dhcp4.statistic_get_all()
    assert response.result == 0


def test_kea_dhcp4_statistic_get(kea_server: Kea):
    response = kea_server.dhcp4.statistic_get(name="pkt4-received")
    assert response.result == 0
    assert response.arguments["pkt4-received"]


def test_kea_dhcp4_statistic_get_bad_name(kea_server: Kea):
    response = kea_server.dhcp4.statistic_get(name="bad-name-argument")
    assert response.result == 0
    assert response.arguments == {}
