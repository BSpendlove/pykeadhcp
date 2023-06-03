from pykeadhcp.models.generic.base import KeaBaseModel


class SanityCheck(KeaBaseModel):
    lease_checks: str
