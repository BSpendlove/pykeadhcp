from typing import List, Optional
from pykeadhcp.models.generic.subnet import Subnet
from pykeadhcp.models.dhcp6.pd_pool import PDPool
from pykeadhcp.models.dhcp6.reservation import Reservation6


class Subnet6(Subnet):
    preferred_lifetime: Optional[int]
    min_preferred_lifetime: Optional[int]
    max_preferred_lifetime: Optional[int]
    pd_pools: Optional[List[PDPool]] = []
    interface_id: Optional[str]
    rapid_commit: Optional[bool]
    reservations: Optional[List[Reservation6]] = []
