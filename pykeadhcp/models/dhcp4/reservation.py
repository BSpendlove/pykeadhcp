from typing import Optional
from pykeadhcp.models.generic.reservation import Reservation


class Reservation4(Reservation):
    client_id: Optional[str]
    circuit_id: Optional[str]
    ip_address: str
    next_server: Optional[str]
    server_hostname: Optional[str]
    boot_file_name: Optional[str]
