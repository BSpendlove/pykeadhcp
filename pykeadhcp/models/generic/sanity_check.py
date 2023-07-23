from typing import Optional
from pykeadhcp.models.generic.base import KeaBaseModel


class SanityCheck(KeaBaseModel):
    lease_checks: str
    extended_info_checks: Optional[str]
