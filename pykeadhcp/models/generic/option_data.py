from typing import Optional
from pykeadhcp.models.generic.base import KeaBaseModel


class OptionData(KeaBaseModel):
    data: str
    name: Optional[str]
    code: Optional[int]
    space: Optional[str]
    csv_format: Optional[bool]
    always_send: Optional[bool]
    user_context: Optional[dict]
    comment: Optional[str]
    unknown_map_entry: Optional[str]
