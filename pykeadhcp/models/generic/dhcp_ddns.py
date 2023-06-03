from typing import Optional
from pykeadhcp.models.generic.config import CommonConfig
from pykeadhcp.models.enums import NCRProtocolEnum, NCRFormatEnum


class DhcpDdns(CommonConfig):
    enable_updates: bool
    server_ip: str
    server_port: int
    sender_ip: str
    sender_port: int
    max_queue_size: int
    ncr_protocol: NCRProtocolEnum
    ncr_format: NCRFormatEnum
    dep_override_no_update: Optional[bool]
    dep_override_client_update: Optional[bool]
    dep_replace_client_name: Optional[str]
    dep_generated_prefix: Optional[str]
    dep_qualifying_suffix: Optional[str]
    dep_hostname_char_set: Optional[str]
    dep_hostname_char_replacement: Optional[str]


"""
"enable-updates": false,
"max-queue-size": 1024,
"ncr-format": "JSON",
"ncr-protocol": "UDP",
"sender-ip": "0.0.0.0",
"sender-port": 0,
"server-ip": "127.0.0.1",
"server-port": 53001
"""
