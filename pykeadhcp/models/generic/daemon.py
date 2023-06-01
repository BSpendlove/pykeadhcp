from typing import Optional, List, Union
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.generic.config import CommonDhcpConfig
from pykeadhcp.models.generic.hook import Hook
from pykeadhcp.models.generic.logger import Logger
from pykeadhcp.models.enums import DHCPSocketTypeEnum, OutboundInterfaceEnum


class CommonDaemonConfig(CommonDhcpConfig):
    hooks_libraries: Optional[List[Hook]]
    loggers: Optional[List[Logger]]


class InterfaceListConfig(KeaBaseModel):
    interfaces: List[str]
    dhcp_socket_type: Optional[DHCPSocketTypeEnum]
    outbound_interface: Optional[OutboundInterfaceEnum]
    re_detect: Optional[bool]
    service_sockets_require_all: Optional[bool]
    service_sockets_retry_wait_time: Optional[int]
    service_sockets_max_retries: Optional[int]


class CommonDhcpDaemonConfig(CommonDaemonConfig):
    interfaces_config: InterfaceListConfig
    lease_database: None
    hosts_database: None
    hosts_databases: None
    host_reservation_identifiers: None
    client_classes: None
    option_def: None
    expired_leases_processing: None
    dhcp4o6_port: Optional[int]
    control_socket: None
    dhcp_queue_control: None
    dhcp_ddns: None
    sanity_checks: None
    config_control: None
    server_tag: Optional[str]
    hostname_char_set: Optional[str]
    hostname_char_replacement: Optional[str]
    statistic_default_sample_count: Optional[int]
    statistic_default_sample_age: Optional[int]
    dhcp_multi_threading: None
    early_global_reservations_lookup: Optional[bool]
    ip_reservations_unique: Optional[bool]
    reservations_lookup_first: Optional[bool]
    compatibility: None
    parked_packet_limit: Optional[int]
