from typing import Optional, List
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.generic.option_data import OptionData


class PDPool(KeaBaseModel):
    prefix: str
    prefix_len: int
    delegated_len: int
    option_data: Optional[List[OptionData]]
    client_class: Optional[str]
    require_client_classes: Optional[List[str]]
    excluded_prefix: Optional[str]
    excluded_prefix_len: Optional[int]
    user_context: Optional[dict]
    comment: Optional[str]
    unknown_map_entry: Optional[str]
