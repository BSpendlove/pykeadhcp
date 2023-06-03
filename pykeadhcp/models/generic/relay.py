from typing import List
from pykeadhcp.models.generic.base import KeaBaseModel


class Relay(KeaBaseModel):
    ip_addresses: List[str] = []
