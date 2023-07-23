from typing import Optional, List
from pykeadhcp.models.generic.daemon import CommonDhcpDaemonConfig
from pykeadhcp.models.dhcp6.client_class import ClientClass6
from pykeadhcp.models.dhcp6.shared_network import SharedNetwork6
from pykeadhcp.models.dhcp6.subnet import Subnet6
from pykeadhcp.models.dhcp6.reservation import Reservation6
from pykeadhcp.models.dhcp6.server_id import ServerId


class Dhcp6DaemonConfig(CommonDhcpDaemonConfig):
    client_classes: Optional[List[ClientClass6]] = []
    shared_networks: Optional[List[SharedNetwork6]] = []
    reservations: Optional[List[Reservation6]] = []
    data_directory: Optional[str]
    preferred_lifetime: Optional[int]
    min_preferred_lifetime: Optional[int]
    max_preferred_lifetime: Optional[int]
    subnet6: Optional[List[Subnet6]] = []
    mac_sources: Optional[List[str]] = []
    relay_supplied_options: Optional[List[str]] = []
    server_id: ServerId
    pd_allocator: Optional[str]
