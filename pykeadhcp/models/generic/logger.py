from typing import Optional, List
from pydantic import conint
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.enums import LoggerLevelEnum


class Output(KeaBaseModel):
    output: str
    flush: bool
    maxsize: int
    maxver: int
    pattern: Optional[str]


class Logger(KeaBaseModel):
    name: str
    output_options: Optional[List[Output]]
    debuglevel: conint(ge=0, le=100)
    severity: Optional[LoggerLevelEnum]
    user_context: Optional[dict]
    comment: Optional[str]
    unknown_map_entry: Optional[str]

    class Config:
        fields = {"output_options": "output_options"}
