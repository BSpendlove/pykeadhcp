from typing import Optional
from pykeadhcp.models.generic.lease import Lease
from pykeadhcp.models.enums import Lease6TypeEnum


class Lease6(Lease):
    duid: str
    iaid: int
    prefix_len: Optional[int]
    type: Optional[Lease6TypeEnum]
