from typing import List


class GenericParser:
    """A Parser does not interact with the ISC Kea Daemon APIs but essentially builds
    similar functionality for a local cached config file. If you do not pay for the
    premium hooks to expose the different commands like subnet4-add or network4-del then
    the parsers job is to provide similar functionality for the provided daemon configuration
    and then you should use the relevant service `config-set` functionality which is implemented
    for each service in pykeadhcp.

    The recommended option is to use the functions within the Daemon class (eg. server.dhcp4) and to
    use these parsers as a last resort as tests are not currently performed as extensively vs the API
    functionality"""

    def __init__(self, config: dict):
        self.config = config
