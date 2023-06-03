from typing import Optional, List
from pykeadhcp.models.generic.client_class import ClientClass
from pykeadhcp.models.generic.option_def import OptionDef


class ClientClass4(ClientClass):
    option_def: Optional[List[OptionDef]]
    next_server: Optional[str]
    server_hostname: Optional[str]
    boot_file_name: Optional[str]
