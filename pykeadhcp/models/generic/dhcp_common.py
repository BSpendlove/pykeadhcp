from typing import Optional, List, Union
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.enums import ReservationMode, DDNSReplaceClientNameEnum


class CommonDHCPParams(KeaBaseModel):
    """Any param shared between Shared Network and Subnets"""

    interface: Optional[str]
    renew_timer: Optional[int]
    rebind_timer: Optional[int]
    option_data_list: Optional[List[dict]]
    client_class: Optional[str]
    require_client_classes: Optional[List[str]]
    reservation_mode: Optional[ReservationMode]
    reservations_global: Optional[bool]
    reservations_in_subnet: Optional[bool]
    reservations_out_of_pool: Optional[bool]
    user_context: Optional[dict]
    comment: Optional[str]
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
    store_extended_info: Optional[bool]
    unknown_map_entry: Optional[str]

    class Config:
        use_enum_values = True
