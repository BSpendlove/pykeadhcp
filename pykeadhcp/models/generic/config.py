from typing import Optional, List, Union
from pykeadhcp.models.generic.base import KeaModel
from pykeadhcp.models.generic.hook import Hook
from pykeadhcp.models.generic.logger import Logger
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.models.enums import ReservationMode, DDNSReplaceClientNameEnum


class CommonConfig(KeaModel):
    store_extended_info: Optional[bool]


class CommonDhcpConfig(CommonConfig):
    valid_lifetime: Optional[int]
    min_valid_lifetime: Optional[int]
    max_valid_lifetime: Optional[int]
    renew_timer: Optional[int]
    rebind_timer: Optional[int]
    option_data: Optional[List[OptionData]] = []
    reservation_mode: Optional[ReservationMode]
    reservations_global: Optional[bool]
    reservations_in_subnet: Optional[bool]
    reservations_out_of_pool: Optional[bool]
    calculate_tee_times: Optional[bool]
    t1_percent: Optional[float]
    t2_percent: Optional[float]
    cache_threshold: Optional[float]
    cache_max_age: Optional[int]
    ddns_send_updates: Optional[bool]
    ddns_override_no_update: Optional[bool]
    ddns_override_client_update: Optional[bool]
    ddns_replace_client_name: Optional[Union[DDNSReplaceClientNameEnum, bool]]
    ddns_generated_prefix: Optional[str]
    ddns_qualifying_suffix: Optional[str]
    ddns_update_on_renew: Optional[bool]
    ddns_use_conflict_resolution: Optional[bool]
