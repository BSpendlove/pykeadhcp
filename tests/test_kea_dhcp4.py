from pykeadhcp import Kea
import pytest


def test_kea_dhcp4_build_report(kea_server: Kea):
    response = kea_server.dhcp4.build_report()
    assert response["result"] == 0


def test_kea_dhcp4_config_get(kea_server: Kea):
    response = kea_server.dhcp4.config_get()
    assert response["result"] == 0


def test_kea_dhcp4_config_reload(kea_server: Kea):
    response = kea_server.dhcp4.config_reload()
    assert response["result"] == 0
