from typing import Optional, List, Union
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.enums import HAModeTypeEnum, HARoleTypeEnum, HAStateTypeEnum


class HAServerLocal(KeaBaseModel):
    role: HARoleTypeEnum
    scopes: List[str]
    state: HAStateTypeEnum


class HAServerRemote(KeaBaseModel):
    age: int
    in_touch: bool
    last_scopes: List[str]
    last_state: Union[None, HAStateTypeEnum]
    role: HARoleTypeEnum


class HAServers(KeaBaseModel):
    local: HAServerLocal
    remote: HAServerRemote


class HighAvailability(KeaBaseModel):
    ha_mode: HAModeTypeEnum
    ha_servers: HAServers
