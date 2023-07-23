from typing import Optional, List, Union
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.generic.config import CommonDhcpConfig
from pykeadhcp.models.generic.hook import Hook
from pykeadhcp.models.generic.logger import Logger
from pykeadhcp.models.generic.database import Database
from pykeadhcp.models.generic.option_def import OptionDef
from pykeadhcp.models.generic.control_socket import ControlSocket
from pykeadhcp.models.generic.dhcp_queue_control import DHCPQueueControl
from pykeadhcp.models.generic.dhcp_ddns import DhcpDdns
from pykeadhcp.models.generic.sanity_check import SanityCheck
from pykeadhcp.models.generic.multi_threading import MultiThreading
from pykeadhcp.models.enums import (
    DHCPSocketTypeEnum,
    OutboundInterfaceEnum,
    HostReservationIdentifierEnum,
)


class CommonDaemonConfig(CommonDhcpConfig):
    hooks_libraries: Optional[List[Hook]] = []
    loggers: Optional[List[Logger]] = []


class InterfaceListConfig(KeaBaseModel):
    interfaces: List[str] = []
    dhcp_socket_type: Optional[DHCPSocketTypeEnum]
    outbound_interface: Optional[OutboundInterfaceEnum]
    re_detect: Optional[bool]
    service_sockets_require_all: Optional[bool]
    service_sockets_retry_wait_time: Optional[int]
    service_sockets_max_retries: Optional[int]


class CommonDhcpDaemonConfig(CommonDaemonConfig):
    interfaces_config: InterfaceListConfig
    lease_database: Optional[Database]
    hosts_database: Optional[Database]
    hosts_databases: Optional[List[Database]]
    host_reservation_identifiers: Optional[List[HostReservationIdentifierEnum]] = []
    option_def: Optional[List[OptionDef]] = []
    expired_leases_processing: Optional[dict]
    dhcp4o6_port: Optional[int]
    control_socket: Optional[ControlSocket]
    dhcp_queue_control: Optional[DHCPQueueControl]
    dhcp_ddns: Optional[DhcpDdns]
    sanity_checks: Optional[SanityCheck]
    config_control: Optional[dict]
    server_tag: Optional[str]
    hostname_char_set: Optional[str]
    hostname_char_replacement: Optional[str]
    statistic_default_sample_count: Optional[int]
    statistic_default_sample_age: Optional[int]
    multi_threading: Optional[MultiThreading]
    early_global_reservations_lookup: Optional[bool]
    ip_reservations_unique: Optional[bool]
    reservations_lookup_first: Optional[bool]
    compatibility: Optional[dict]
    parked_packet_limit: Optional[int]
    decline_probation_period: Optional[int]
    allocator: Optional[str]
