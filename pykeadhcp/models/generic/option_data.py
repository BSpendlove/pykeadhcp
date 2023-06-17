from typing import Optional
from pykeadhcp.models.generic.base import KeaModel


class OptionData(KeaModel):
    data: str
    name: Optional[str]
    code: Optional[int]
    space: Optional[str]
    csv_format: Optional[bool]
    always_send: Optional[bool]
