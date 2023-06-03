from pykeadhcp.parsers.generic import GenericParser
from pykeadhcp.models.dhcp4.config import Dhcp4DaemonConfig
from pykeadhcp.models.dhcp4.shared_network import SharedNetwork4
from pykeadhcp.models.dhcp4.subnet import Subnet4


class Dhcp4Parser(GenericParser):
    """Parser for the ISC Kea Dhcp4 configuration file. This should ideally
    be used with the cached config stored in the Daemon class like this:

    parser = Dhcp4Parser(config=server.dhcp4.cached_config)
    """

    def __init__(self, config: dict):
        self.config = Dhcp4DaemonConfig.parse_obj(config["Dhcp4"])

    def get_shared_network(self, name: str) -> SharedNetwork4:
        """Returns a specific Dhcp4 shared-network

        Args:
            name:       Name of the shared-network
        """
        for shared_network in self.config.shared_networks:
            if shared_network.name == name:
                return shared_network

    def get_subnet(self, id: int) -> Subnet4:
        """Attempts to return the first found subnet based on the subnets id using
        global subnets first then shared-networks last.

        Args:
            id:     ID of the subnet
        """
        for subnet in self.config.subnet4:
            if subnet.id == id:
                return subnet

        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet4:
                if subnet.id == id:
                    return subnet

    def get_subnet_by_cidr(self, cidr: str) -> Subnet4:
        """Attempts to return the first found subnet based on the provided cidr
        using global subnets first and then shared-networks last.

        Args:
            cidr:       IPv4 CIDR (eg. 192.0.2.0/24)
        """
        for subnet in self.config.subnet4:
            if subnet.subnet == cidr:
                return subnet

        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet4:
                if subnet.subnet == cidr:
                    return subnet
