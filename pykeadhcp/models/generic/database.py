from typing import Optional
from pykeadhcp.models.generic.base import KeaBaseModel
from pykeadhcp.models.enums import DatabaseTypeEnum, DatabaseOnFailEnum


class Database(KeaBaseModel):
    type: DatabaseTypeEnum
    user: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int]
    name: Optional[str]
    persist: Optional[bool]
    lfc_interval: Optional[int]
    readonly: Optional[bool]
    connect_timeout: Optional[int]
    max_reconnect_tries: Optional[int]
    on_fail: Optional[DatabaseOnFailEnum]
    max_row_errors: Optional[int]
    trust_anchor: Optional[str]
    cert_file: Optional[str]
    key_file: Optional[str]
    cipher_list: Optional[str]
    unknown_map_entry: Optional[str]
