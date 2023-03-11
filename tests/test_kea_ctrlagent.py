from pykeadhcp import Kea
import pytest


def test_kea_ctrlagent_build_report(kea_server: Kea):
    response = kea_server.ctrlagent.build_report()
    assert response["result"] == 0


def test_kea_ctrlagent_config_get(kea_server: Kea):
    response = kea_server.ctrlagent.config_get()
    assert response["result"] == 0


def test_kea_ctrlagent_config_reload(kea_server: Kea):
    response = kea_server.ctrlagent.config_reload()
    assert response["result"] == 0


def test_kea_ctrlagent_list_commands(kea_server: Kea):
    response = kea_server.ctrlagent.list_commands()
    assert response["result"] == 0


def test_kea_ctrlagent_status_get(kea_server: Kea):
    response = kea_server.ctrlagent.status_get()
    assert response["result"] == 0


def test_kea_ctrlagent_version_get(kea_server: Kea):
    response = kea_server.ctrlagent.version_get()
    assert response["result"] == 0


def test_kea_ctrlagent_shutdown(kea_server: Kea):
    response = kea_server.ctrlagent.shutdown()
    assert response["result"] == 0
