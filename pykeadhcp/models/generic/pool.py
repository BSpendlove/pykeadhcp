from typing import Optional, List
from pykeadhcp.models.generic.base import KeaModel
from pykeadhcp.models.generic.option_data import OptionData


class Pool(KeaModel):
    pool: str
    option_data: Optional[List[OptionData]] = []
    client_class: Optional[str]
    require_client_classes: Optional[str]
