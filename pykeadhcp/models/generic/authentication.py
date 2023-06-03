from typing import Optional, List
from pykeadhcp.models.generic.config import CommonConfig
from pykeadhcp.models.enums import AuthenticationTypeEnum


class AuthenticationClient(CommonConfig):
    user: Optional[str]
    user_file: Optional[str]
    password: Optional[str]
    password_file: Optional[str]


class Authentication(CommonConfig):
    type: AuthenticationTypeEnum
    realm: str
    directory: Optional[str]
    clients: List[Optional[AuthenticationClient]] = []
