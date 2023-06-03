from typing import Optional, List
from pykeadhcp.models.generic.daemon import CommonDaemonConfig
from pykeadhcp.models.generic.control_socket import ControlSockets


class CtrlAgentDaemonConfig(CommonDaemonConfig):
    http_host: str
    http_port: int
    trust_anchor: Optional[str]
    cert_file: Optional[str]
    key_file: Optional[str]
    cert_required: Optional[bool]
    control_sockets: Optional[ControlSockets]
    authentication: Optional[dict]
