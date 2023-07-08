from typing import Optional
from pydantic import conint
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.enums import RemoteMapTypeEnum


class RemoteMap(KeaBaseModel):
    type: Optional[RemoteMapTypeEnum]
    host: Optional[str]
    port: Optional[conint(gt=1, le=65535)]
