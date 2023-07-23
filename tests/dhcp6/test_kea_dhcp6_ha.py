from pykeadhcp import Kea
import pytest

"""ha process:
status-get (get HA mode)
"""


@pytest.mark.order("first")
def test_kea_dhcp6_ha_check_primary(kea_server: Kea):
    status = kea_server.dhcp6.status_get()

    assert status.high_availability
    assert len(status.high_availability) > 0

    ha_settings = status.high_availability[0]

    assert ha_settings.ha_mode == "hot-standby"
    assert ha_settings.ha_servers.local.role == "primary"
    assert ha_settings.ha_servers.local.state == "hot-standby"
    assert ha_settings.ha_servers.remote.last_state == "hot-standby"


def test_kea_dhcp6_ha_continue_not_paused(kea_server: Kea):
    response = kea_server.dhcp6.ha_continue()
    assert response.result == 0
    assert "not paused" in response.text


def test_kea_dhcp6_ha_heartbeat(kea_server: Kea):
    response = kea_server.dhcp6.ha_heartbeat()
    assert response.result == 0


def test_kea_dhcp6_ha_maintenance_cancel_wrong_state(kea_server: Kea):
    response = kea_server.dhcp6.ha_maintenance_cancel()
    assert response.result == 1
    assert "not in the partner-in-maintenance state" in response.text


def test_kea_dhcp6_ha_maintenance_notify_not_in_maintenance_mode(kea_server: Kea):
    response = kea_server.dhcp6.ha_maintenance_notify(cancel=True)
    assert response.result == 1
    assert "not in the in-maintenance state" in response.text


def test_kea_dhcp6_ha_maintenance_start(kea_server: Kea):
    response = kea_server.dhcp6.ha_maintenance_start()
    assert response.result == 0

    status = kea_server.dhcp6.status_get()
    ha_settings = status.high_availability[0]
    assert ha_settings.ha_servers.local.state == "partner-in-maintenance"


def test_kea_dhcp6_ha_maintenance_cancel(kea_server: Kea):
    response = kea_server.dhcp6.ha_maintenance_cancel()
    assert response.result == 0


def test_kea_dhcp6_ha_maintenance_reset(kea_server: Kea):
    response = kea_server.dhcp6.ha_reset()
    assert response.result == 0


def test_kea_dhcp6_ha_reset_peer(kea_server: Kea):
    kea_server.port = (
        8081  # Need to find a better way to integrate this into pytest as a fixture...
    )
    response = kea_server.dhcp6.ha_reset()
    assert response.result == 0

    kea_server.dhcp6.ha_maintenance_cancel()


def test_kea_dhcp6_ha_sync(kea_server: Kea):
    response = kea_server.dhcp6.ha_sync(partner_server="server2", max_period=30)
    assert response.result == 0


def test_kea_dhcp6_ha_synbc_complete_notify(kea_server: Kea):
    response = kea_server.dhcp6.ha_sync_complete_notify()
    assert response.result == 0
