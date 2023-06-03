from pykeadhcp.parsers.generic import GenericParser
from pykeadhcp.models.dhcp6.config import Dhcp6DaemonConfig
from pykeadhcp.models.dhcp6.subnet import Subnet6


class Dhcp6Parser(GenericParser):
    """Parser for the ISC Kea Dhcp6 configuration file. This should ideally
    be used with the cached config stored in the Daemon class like this:

    parser = Dhcp6Parser(config=server.dhcp6.cached_config)
    """

    def __init__(self, config: dict):
        self.config = Dhcp6DaemonConfig.parse_obj(config["Dhcp6"])
