from pykeadhcp import Kea


def test_kea_ctrlagent_build_report(kea_server: Kea):
    response = kea_server.ctrlagent.build_report()
    assert response.result == 0
    assert response.text


def test_kea_ctrlagent_config_get(kea_server: Kea):
    response = kea_server.ctrlagent.config_get()
    assert response.result == 0
    assert response.arguments


def test_kea_ctrlagent_config_reload(kea_server: Kea):
    response = kea_server.ctrlagent.config_reload()
    assert response.result == 0
    assert response.text


def test_kea_ctrlagent_list_commands(kea_server: Kea):
    response = kea_server.ctrlagent.list_commands()
    assert response.result == 0
    assert response.arguments
    assert "config-get" in response.arguments


def test_kea_ctrlagent_status_get(kea_server: Kea):
    response = kea_server.ctrlagent.status_get()
    assert response.pid
    assert response.reload >= 0
    assert response.uptime


def test_kea_ctrlagent_shutdown(kea_server: Kea):
    response = kea_server.ctrlagent.shutdown()
    assert response.result == 0
    assert response.text == "Control Agent is shutting down"
