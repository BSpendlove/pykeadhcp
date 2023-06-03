from pykeadhcp.models.ctrlagent.config import CtrlAgentDaemonConfig
from pykeadhcp.models.generic.control_socket import ControlSockets


def test_ci_kea_ctrlagent_config_model_load(ctrlagent_model: CtrlAgentDaemonConfig):
    assert ctrlagent_model


def test_ci_kea_ctrlagent_config_model_by_export(
    ctrlagent_model: CtrlAgentDaemonConfig,
):
    assert ctrlagent_model.dict(exclude_none=True, by_alias=True)


def test_ci_kea_ctrlagent_config_model_check_required(
    ctrlagent_model: CtrlAgentDaemonConfig,
):
    assert ctrlagent_model.http_host
    assert ctrlagent_model.http_port


def test_ci_kea_ctrlagent_config_model_control_sockets(
    ctrlagent_model: CtrlAgentDaemonConfig,
):
    assert type(ctrlagent_model.control_sockets) == ControlSockets

    assert ctrlagent_model.control_sockets.d2.socket_name
    assert ctrlagent_model.control_sockets.d2.socket_type == "unix"

    assert ctrlagent_model.control_sockets.dhcp4.socket_name
    assert ctrlagent_model.control_sockets.dhcp4.socket_type == "unix"

    assert ctrlagent_model.control_sockets.dhcp6.socket_name
    assert ctrlagent_model.control_sockets.dhcp6.socket_type == "unix"


def test_ci_kea_ctrlagent_config_model_loggers(
    ctrlagent_model: CtrlAgentDaemonConfig,
):
    assert len(ctrlagent_model.loggers) > 0
