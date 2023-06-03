from typing import Optional, List
from pykeadhcp.models.generic.reservation import Reservation


class Reservation6(Reservation):
    ip_addresses: Optional[List[str]] = []
    prefixes: Optional[List[str]] = []
