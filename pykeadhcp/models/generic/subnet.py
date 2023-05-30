from typing import Optional, List
from pydantic import conint
from pykeadhcp.models.generic.dhcp_common import CommonDHCPParams
from pykeadhcp.models.generic.pool import Pool


class Subnet(CommonDHCPParams):
    id: conint(gt=0, lt=4294967295)
    pools_list: Optional[List[Pool]]
    subnet: str
    hostname_char_set: Optional[str]
    hostname_char_replacement: Optional[str]
