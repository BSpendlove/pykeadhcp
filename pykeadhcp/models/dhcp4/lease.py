from typing import List, Optional
from pykeadhcp.models.generic.lease import Lease, LeasePage


class Lease4(Lease):
    pass


class Lease4Page(LeasePage):
    count: int
    leases: Optional[List[Lease4]] = []
