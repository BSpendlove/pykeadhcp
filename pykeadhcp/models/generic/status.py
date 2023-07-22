from typing import Optional, List
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.generic import Sockets
from pykeadhcp.models.generic.high_availability import HighAvailability


class StatusGet(KeaBaseModel):
    pid: int
    uptime: int
    reload: int
    multi_threading_enabled: Optional[bool]
    sockets: Optional[Sockets]
    high_availability: Optional[List[HighAvailability]] = []
