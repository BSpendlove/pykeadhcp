from typing import Optional, List
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.generic.option_data import OptionData


class Pool(KeaBaseModel):
    pool: str
    option_data: Optional[List[OptionData]]
    client_class: Optional[str]
    require_client_classes: Optional[str]
    user_context: Optional[dict]
    comment: Optional[str]
    unknown_map_entry: Optional[str]
