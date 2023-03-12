from pykeadhcp import Kea
import pytest


def test_kea_dhcp6_build_report(kea_server: Kea):
    response = kea_server.dhcp6.build_report()
    assert response["result"] == 0
