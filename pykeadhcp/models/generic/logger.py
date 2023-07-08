from typing import Optional, List
from pydantic import conint
from pykeadhcp.models.generic.base import KeaBaseModel, KeaModel
from pykeadhcp.models.enums import LoggerLevelEnum


class Output(KeaBaseModel):
    output: str
    flush: bool
    maxsize: Optional[int]
    maxver: Optional[int]
    pattern: Optional[str]


class Logger(KeaModel):
    name: str
    output_options: Optional[List[Output]] = []
    debuglevel: conint(ge=0, le=100)
    severity: Optional[LoggerLevelEnum]

    class Config:
        fields = {"output_options": "output_options"}
