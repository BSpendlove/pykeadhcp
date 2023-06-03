from typing import Optional, List
from pykeadhcp.models.generic.client_class import ClientClass


class ClientClass6(ClientClass):
    preferred_lifetime: Optional[int]
    min_preferred_lifetime: Optional[int]
    max_preferred_lifetime: Optional[int]
