from typing import Optional, List
from pykeadhcp.models.generic.config import CommonConfig
from pykeadhcp.models.generic.option_data import OptionData


class ClientClass(CommonConfig):
    name: str
    test: Optional[str]
    only_if_required: Optional[bool]
    option_data: Optional[List[OptionData]]
    valid_lifetime: Optional[int]
    min_valid_lifetime: Optional[int]
    max_valid_lifetime: Optional[int]
