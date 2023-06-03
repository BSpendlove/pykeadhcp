from typing import Optional, List
from pykeadhcp.models.generic.lease import Lease, LeasePage
from pykeadhcp.models.enums import Lease6TypeEnum


class Lease6(Lease):
    duid: str
    iaid: int
    prefix_len: Optional[int]
    type: Optional[Lease6TypeEnum]


class Lease6Page(LeasePage):
    count: int
    leases: Optional[List[Lease6]] = []
