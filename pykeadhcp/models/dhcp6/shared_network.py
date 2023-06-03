from typing import Optional, List
from pykeadhcp.models.generic.shared_network import SharedNetwork
from pykeadhcp.models.dhcp6.subnet import Subnet6


class SharedNetwork6(SharedNetwork):
    subnet6: Optional[List[Subnet6]] = []
    interface_id: Optional[str]
    min_preferred_lifetime: Optional[int]
    max_preferred_lifetime: Optional[int]
    rapid_commit: Optional[bool]
