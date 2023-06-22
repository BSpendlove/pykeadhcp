from pykeadhcp.models.dhcp6.config import Dhcp6DaemonConfig


def test_ci_kea_dhcp6_config_model_load(dhcp6_model: Dhcp6DaemonConfig):
    assert dhcp6_model


def test_ci_kea_dhcp6_config_model_export(dhcp6_model: Dhcp6DaemonConfig):
    assert dhcp6_model.dict(exclude_none=True, by_alias=True)


def test_ci_kea_dhcp6_config_model_hooks(dhcp6_model: Dhcp6DaemonConfig):
    assert len(dhcp6_model.hooks_libraries) > 0
    for hook_library in dhcp6_model.hooks_libraries:
        assert hook_library.library


def test_ci_kea_dhcp6_config_client_classes(dhcp6_model: Dhcp6DaemonConfig):
    assert len(dhcp6_model.client_classes) > 0
    for client_class in dhcp6_model.client_classes:
        assert client_class.name
        assert len(client_class.option_data) > 0
