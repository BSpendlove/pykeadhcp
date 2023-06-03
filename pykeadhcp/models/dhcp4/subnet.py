from typing import List, Optional
from pykeadhcp.models.generic.subnet import Subnet
from pykeadhcp.models.dhcp4.reservation import Reservation4


class Subnet4(Subnet):
    match_client_id: Optional[bool]
    authoritative: Optional[bool]
    next_server: Optional[str]
    boot_file_name: Optional[str]
    subnet_4o6_interface: Optional[str]
    subnet_4o6_interface_id: Optional[str]
    subnet_4o6_subnet: Optional[str]
    reservations: Optional[List[Reservation4]] = []

    class Config:
        fields = {
            "subnet_4o6_interface": "4o6-interface",
            "subnet_4o6_interface_id": "4o6-interface-id",
            "subnet_4o6_subnet": "4o6-subnet",
        }
