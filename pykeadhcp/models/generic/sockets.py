from typing import Optional, List
from pydantic import BaseModel
from pykeadhcp.models.enums import StatusEnum


class Sockets(BaseModel):
    errors: Optional[List[str]] = []
    status: StatusEnum

    class Config:
        use_enum_values = True
