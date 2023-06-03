from typing import Optional
from pykeadhcp.models.generic.config import CommonConfig


class OptionDef(CommonConfig):
    name: str
    code: Optional[int]
    type: Optional[str]
    record_types: Optional[str]
    space: Optional[str]
    encapsulate: Optional[str]
    array: Optional[bool]
