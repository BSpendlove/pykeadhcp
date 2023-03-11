from pykeadhcp import Kea
import pytest


def test_kea_ctrlagent_build_report(kea_server: Kea):
    response = kea_server.ctrlagent.build_report()
    assert response["result"] == 0
