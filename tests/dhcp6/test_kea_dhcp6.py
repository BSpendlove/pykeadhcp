from pykeadhcp import Kea


def test_kea_dhcp6_build_report(kea_server: Kea):
    response = kea_server.dhcp6.build_report()
    assert response.result == 0
    assert response.text


def test_kea_dhcp6_config_get(kea_server: Kea):
    response = kea_server.dhcp6.config_get()
    assert response.result == 0
    assert "Dhcp6" in response.arguments


def test_kea_dhcp6_config_test(kea_server: Kea):
    config = kea_server.dhcp6.cached_config
    response = kea_server.dhcp6.config_test(config=config)
    assert response.result == 0


def test_kea_dhcp6_config_set(kea_server: Kea):
    config = kea_server.dhcp6.cached_config
    response = kea_server.dhcp6.config_set(config=config)
    assert response.result == 0


def test_kea_dhcp6_config_write(kea_server: Kea):
    filename = "/usr/local/etc/kea/kea-dhcp6.conf"
    response = kea_server.dhcp6.config_write(filename=filename)
    assert response.result == 0
    assert response.arguments["filename"] == filename
    assert response.arguments["size"] > 0


def test_kea_dhcp6_config_reload(kea_server: Kea):
    response = kea_server.dhcp6.config_reload()
    assert response.result == 0
    assert response.text == "Configuration successful."


def test_kea_dhcp6_dhcp_disable(kea_server: Kea):
    response = kea_server.dhcp6.dhcp_disable(max_period=60)
    assert response.result == 0
    assert response.text == "DHCPv6 service disabled for 60 seconds"


def test_kea_dhcp6_dhcp_enable(kea_server: Kea):
    response = kea_server.dhcp6.dhcp_enable()
    assert response.result == 0
    assert response.text == "DHCP service successfully enabled"


def test_kea_dhcp6_list_commands(kea_server: Kea):
    response = kea_server.dhcp6.list_commands()
    assert response.result == 0
    assert "config-get" in response.arguments


def test_kea_dhcp6_status_get(kea_server: Kea):
    response = kea_server.dhcp6.status_get()
    assert response.pid
    assert response.uptime


def test_kea_dhcp6_version_get(kea_server: Kea):
    response = kea_server.dhcp6.version_get()
    assert response.result == 0


def test_kea_dhcp6_shutdown(kea_server: Kea):
    response = kea_server.dhcp6.shutdown()
    assert response == 0
