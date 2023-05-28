from typing import Any, List, Optional, TYPE_CHECKING
from pydantic import BaseModel

from pykeadhcp.models.generic.dhcp_common import CommonDHCPParams
from pykeadhcp.models.dhcp4.subnet import Subnet4


class SharedNetwork4(CommonDHCPParams):
    calculate_tee_times: Optional[bool]
    max_valid_lifetime: Optional[int]
    min_valid_lifetime: Optional[int]
    name: str
    option_data: Optional[List[Any]]
    rebind_timer: Optional[int]
    relay: Optional[dict]
    renew_timer: Optional[int]
    store_extended_info: Optional[bool]
    subnet4: Optional[List[Subnet4]]
    t1_percent: Optional[float]
    t2_percent: Optional[float]
    user_context: Optional[dict]
    valid_lifetime: Optional[int]
