from typing import Optional, List
from pydantic import BaseModel
from pykeadhcp.models.generic import Sockets


class StatusGet(BaseModel):
    pid: int
    uptime: int
    reload: int
    multi_threading_enabled: Optional[bool]
    sockets: Optional[Sockets]
    high_availability: Optional[List[dict]]

    class Config:
        fields = {
            "multi_threading_enabled": "multi-threading-enabled",
            "high_availability": "high-availability",
        }
