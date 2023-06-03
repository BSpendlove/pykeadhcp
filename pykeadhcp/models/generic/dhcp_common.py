from typing import Optional, List
from pykeadhcp.models.generic.config import CommonDhcpConfig
from pykeadhcp.models.generic.relay import Relay


class CommonDHCPParams(CommonDhcpConfig):
    """Any param shared between v4/v6 Shared Networks and Subnets"""

    interface: Optional[str]
    client_class: Optional[str]
    require_client_classes: Optional[List[str]] = []
    relay: Optional[Relay]
