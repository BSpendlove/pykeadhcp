from pykeadhcp.models.dhcp4.config import Dhcp4DaemonConfig


def test_ci_kea_dhcp4_config_model_load(dhcp4_model: Dhcp4DaemonConfig):
    assert dhcp4_model


def test_ci_kea_dhcp4_config_model_export(dhcp4_model: Dhcp4DaemonConfig):
    assert dhcp4_model.dict(exclude_none=True, by_alias=True)


def test_ci_kea_dhcp4_config_model_hooks(dhcp4_model: Dhcp4DaemonConfig):
    assert len(dhcp4_model.hooks_libraries) > 0
    for hook_library in dhcp4_model.hooks_libraries:
        assert hook_library.library


def test_ci_kea_dhcp4_config_model_host_reservation_identifiers(
    dhcp4_model: Dhcp4DaemonConfig,
):
    identifiers = ["hw-address", "duid", "circuit-id", "client-id"]
    assert len(dhcp4_model.host_reservation_identifiers) > 0
    for identifier in dhcp4_model.host_reservation_identifiers:
        assert identifier in identifiers


def test_ci_kea_dhcp4_config_model_interfaces_config(dhcp4_model: Dhcp4DaemonConfig):
    assert len(dhcp4_model.interfaces_config.interfaces) == 1
    assert dhcp4_model.interfaces_config.interfaces[0] == "eth0"


def test_ci_kea_dhcp4_config_model_subnet4(dhcp4_model: Dhcp4DaemonConfig):
    assert len(dhcp4_model.subnet4) > 0
    for subnet in dhcp4_model.subnet4:
        assert subnet.id
        assert subnet.subnet


def test_ci_kea_dhcp4_config_model_subnet4_option_data(dhcp4_model: Dhcp4DaemonConfig):
    for subnet in dhcp4_model.subnet4:
        assert len(subnet.option_data) > 0

        for option in subnet.option_data:
            assert option.code
            assert option.data


def test_ci_kea_dhcp4_config_model_subnet4_pool(dhcp4_model: Dhcp4DaemonConfig):
    for subnet in dhcp4_model.subnet4:
        assert len(subnet.pools) > 0
        for pool in subnet.pools:
            assert pool.pool


def test_ci_kea_dhcp4_config_model_subnet4_reservations(dhcp4_model: Dhcp4DaemonConfig):
    for subnet in dhcp4_model.subnet4:
        assert len(subnet.reservations) > 0
        for reservation in subnet.reservations:
            assert reservation.ip_address
