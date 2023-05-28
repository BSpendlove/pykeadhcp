from typing import Optional
from pykeadhcp.models.generic.base import KeaBaseModel


class Lease(KeaBaseModel):
    cltt: int
    fqdn_fwd: Optional[bool]
    fqdn_rev: Optional[bool]
    hostname: Optional[str]
    hw_address: str
    ip_address: str
    state: int
    subnet_id: int
    valid_lft: int
