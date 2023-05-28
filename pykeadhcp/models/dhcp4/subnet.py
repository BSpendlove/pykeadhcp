from typing import Any, List, Optional
from pydantic import BaseModel, conint
from pykeadhcp.models.generic.dhcp_common import CommonDHCPParams


class Subnet4(CommonDHCPParams):
    subnet: str
    id: conint(
        gt=0, lt=4294967295
    )  # https://kea.readthedocs.io/en/kea-2.2.0/arm/dhcp4-srv.html#ipv4-subnet-identifier
    option_data: Optional[List[Any]]
    min_valid_lifetime: Optional[int]
    max_valid_lifetime: Optional[int]
    pools_list: Optional[List[dict]]
    relay: Optional[dict]
    match_client_id: Optional[bool]
    authoritative: Optional[bool]
    next_server: Optional[str]
    boot_file_name: Optional[str]
    subnet_4o6_interface: Optional[str]
    subnet_4o6_interface_id: Optional[str]
    subnet_4o6_subnet: Optional[str]
    hostname_char_set: Optional[str]
    hostname_char_replacement: Optional[str]
