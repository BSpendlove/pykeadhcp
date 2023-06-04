from typing import Optional, List
from pykeadhcp.models.generic.base import KeaModel
from pykeadhcp.models.generic.option_data import OptionData


class PDPool(KeaModel):
    prefix: str
    prefix_len: int
    delegated_len: int
    option_data: Optional[List[OptionData]] = []
    client_class: Optional[str]
    require_client_classes: Optional[List[str]] = []
    excluded_prefix: Optional[str]
    excluded_prefix_len: Optional[int]
