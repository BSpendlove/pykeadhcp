from typing import List, Optional
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.generic.lease import Lease


class Lease4(Lease):
    pass


class Lease4Page(KeaBaseModel):
    count: int
    leases: Optional[List[Lease4]]
