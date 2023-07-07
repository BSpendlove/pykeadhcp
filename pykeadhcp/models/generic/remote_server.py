from typing import Optional
from pydantic import constr
from pykeadhcp.models.generic.base import KeaBaseModel


class RemoteServer(KeaBaseModel):
    server_tag: constr(max_length=256)
    description: Optional[str]
