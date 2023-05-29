from typing import Optional, List
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.generic.option_data import OptionData


class Reservation(KeaBaseModel):
    duid: Optional[str]
    reservation_client_classes: Optional[List[str]]
    flex_id: Optional[str]
    hw_address: Optional[str]
    hostname: Optional[str]
    optional_data: Optional[List[OptionData]]
    user_context: Optional[dict]
    comment: Optional[str]
    unknown_map_entry: Optional[str]
