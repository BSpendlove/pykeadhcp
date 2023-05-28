from pykeadhcp import Kea
import pytest


def test_kea_dhcp4_build_report(kea_server: Kea):
    response = kea_server.dhcp4.build_report()
    assert response.result == 0
    assert response.text


def test_kea_dhcp4_config_get(kea_server: Kea):
    response = kea_server.dhcp4.config_get()
    assert response.result == 0
    assert "Dhcp4" in response.arguments


def test_kea_dhcp4_config_reload(kea_server: Kea):
    response = kea_server.dhcp4.config_reload()
    assert response.result == 0
    assert response.text == "Configuration successful."


def test_kea_dhcp4_dhcp_disable(kea_server: Kea):
    response = kea_server.dhcp4.dhcp_disable()
    assert response.result == 0
    assert "DHCPv4 service disabled" in response.text

    status = kea_server.dhcp4.status_get()
    assert status.reload < 20


def test_kea_dhcp4_list_commands(kea_server: Kea):
    response = kea_server.dhcp4.list_commands()
    assert response.result == 0
    assert "config-get" in response.arguments


def test_kea_dhcp4_status_get(kea_server: Kea):
    response = kea_server.dhcp4.status_get()
    assert response.pid
    assert response.uptime


def test_kea_dhcp4_version_get(kea_server: Kea):
    response = kea_server.dhcp4.version_get()
    assert response.result == 0


def test_kea_dhcp4_shutdown(kea_server: Kea):
    response = kea_server.dhcp4.shutdown()
    assert response == 0
