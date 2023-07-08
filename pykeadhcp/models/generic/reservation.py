from typing import Optional, List
from pykeadhcp.models.generic.base import KeaModel
from pykeadhcp.models.generic.option_data import OptionData


class Reservation(KeaModel):
    duid: Optional[str]
    client_classes: Optional[List[str]] = []
    flex_id: Optional[str]
    hw_address: Optional[str]
    hostname: Optional[str]
    option_data: Optional[List[OptionData]] = []
    subnet_id: Optional[int]  # Used for reservation-add
