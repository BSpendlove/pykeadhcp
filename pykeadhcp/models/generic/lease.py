from typing import Optional
from pykeadhcp.models.generic.base import KeaBaseModel


class Lease(KeaBaseModel):
    cltt: Optional[int]
    fqdn_fwd: Optional[bool]
    fqdn_rev: Optional[bool]
    hostname: Optional[str]
    hw_address: Optional[str]
    ip_address: str
    state: Optional[int]
    subnet_id: Optional[int]
    valid_lft: Optional[int]


class LeasePage(KeaBaseModel):
    count: int
