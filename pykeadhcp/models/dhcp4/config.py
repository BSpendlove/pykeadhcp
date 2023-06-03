from typing import Optional, List
from pykeadhcp.models.generic.daemon import CommonDhcpDaemonConfig
from pykeadhcp.models.dhcp4.client_class import ClientClass4
from pykeadhcp.models.dhcp4.shared_network import SharedNetwork4
from pykeadhcp.models.dhcp4.subnet import Subnet4
from pykeadhcp.models.dhcp4.reservation import Reservation4


class Dhcp4DaemonConfig(CommonDhcpDaemonConfig):
    client_classes: Optional[List[ClientClass4]] = []
    shared_networks: Optional[List[SharedNetwork4]] = []
    reservations: Optional[List[Reservation4]] = []
    subnet4: Optional[List[Subnet4]] = []
    echo_client_id: Optional[bool]
    match_client_id: Optional[bool]
    authoritative: Optional[bool]
    next_server: Optional[str]
    server_hostname: Optional[str]
    boot_file_name: Optional[str]
