from pykeadhcp.parsers.generic import GenericParser
from pykeadhcp.models.dhcp4.config import Dhcp4DaemonConfig
from pykeadhcp.models.dhcp4.shared_network import SharedNetwork4
from pykeadhcp.models.dhcp4.subnet import Subnet4
from pykeadhcp.models.dhcp4.reservation import Reservation4
from pykeadhcp.models.generic.pool import Pool
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.models.enums import HostReservationIdentifierEnum
from pykeadhcp.parsers import exceptions

from ipaddress import IPv4Address, IPv4Network


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

    def add_shared_network(self, name: str, **kwargs) -> SharedNetwork4:
        """Attempts to add a shared network if it doesn't already
        exist

        Args:
            name:       Name of the shared network
        """
        if self.get_shared_network(name):
            raise exceptions.ParserSharedNetworkAlreadyExistError(name)
        network = SharedNetwork4(name=name, **kwargs)
        self.config.shared_networks.append(network)
        return network

    def add_subnet(self, id: int, subnet: str, **kwargs) -> Subnet4:
        """Attempts to add a Subnet if it doesn't already exist

        Args:
            id:         Subnet Id
            subnet:     Subnet (CIDR eg. 192.0.2.0/24)
        """
        if self.get_subnet(id):
            raise exceptions.ParserSubnetIDAlreadyExistError(id)

        if self.get_subnet_by_cidr(subnet):
            raise exceptions.ParserSubnetCIDRAlreadyExistError(subnet)

        subnet = Subnet4(id=id, subnet=subnet, **kwargs)
        self.config.subnet4.append(subnet)
        return subnet

    def add_subnet_to_shared_network(self, id: int, name: str) -> Subnet4:
        """Attempts to assosicate an existing subnet to a shared-network and returns
        the shared-network

        Args:
            id:     Subnet ID
            name:   Name of the shared network
        """
        existing_network = self.get_shared_network(name)
        if not existing_network:
            raise exceptions.ParserSharedNetworkNotFoundError(name)

        existing_subnet = self.get_subnet(id)
        if not existing_subnet:
            raise exceptions.ParserSubnetNotFoundError(id)

        for index, subnet in enumerate(self.config.subnet4):
            if existing_subnet.id != subnet.id:
                continue

            subnet_to_assosicate = self.config.subnet4.pop(index)
            existing_network.subnet4.append(subnet_to_assosicate)
            return subnet_to_assosicate

    def add_reservation_to_subnet(
        self, id: int, ip_address: str, **kwargs
    ) -> Reservation4:
        """Attempts to add a reservation to an existing subnet

        Args:
            id:             Subnet ID
            ip_address:     IP Address of Reservation
        """
        if self.get_reservation_by_ip(ip_address):
            raise exceptions.ParserReservationAlreadyExistError(ip_address)

        existing_subnet = self.get_subnet(id)
        if not existing_subnet:
            raise exceptions.ParserSubnetNotFoundError(id)

        reservation = Reservation4(ip_address=ip_address, **kwargs)
        existing_subnet.reservations.append(reservation)
        return reservation

    def add_dhcp_option_to_subnet(
        self, id: int, code: int, data: str, **kwargs
    ) -> Subnet4:
        """Attempts to add a DHCP Option to an existing subnet

        Args:
            id:         Subnet ID
            code:       DHCP Option Code
            data:       DHCP Option Data
        """
        existing_subnet = self.get_subnet(id)
        if not existing_subnet:
            raise exceptions.ParserSubnetNotFoundError

        for existing_option in existing_subnet.option_data:
            if existing_option.code == code:
                raise exceptions.ParserOptionDataAlreadyExistError(
                    f"Subnet (ID: {id})", code
                )

        option_data = OptionData(code=code, data=data, **kwargs)
        existing_subnet.option_data.append(option_data)
        return existing_subnet

    def add_dhcp_option_to_shared_network(
        self, name: str, code: int, data: str, **kwargs
    ) -> SharedNetwork4:
        """Attempts to add a DHCP Option to an existing shared network

        Args:
            name:       Name of shared network
            code:       DHCP Option Code
            data:       DHCP Option Data
        """
        existing_shared_network = self.get_shared_network(name)
        if not existing_shared_network:
            raise exceptions.ParserSharedNetworkNotFoundError

        for existing_option in existing_shared_network.option_data:
            if existing_option.code == code:
                raise exceptions.ParserOptionDataAlreadyExistError(
                    f"Shared Network ({name})", code
                )

        option_data = OptionData(code=code, data=data, **kwargs)
        existing_shared_network.option_data.append(option_data)
        return existing_shared_network

    def add_pool_to_subnet(self, id: int, start: str, end: str, **kwargs) -> Subnet4:
        """Attempts to add a pool to an existing subnet

        Args:
            id:     Subnet ID
            start:  Pool Start
            end:    Pool End
        """
        try:
            ipv4_start = IPv4Address(start)
            ipv4_end = IPv4Address(end)
        except:
            raise exceptions.ParserPoolInvalidAddressError(start, end)

        existing_subnet = self.get_subnet(id)
        if not existing_subnet:
            raise exceptions.ParserSubnetNotFoundError(id)

        subnet = IPv4Network(existing_subnet.subnet)
        if ipv4_start not in subnet:
            raise exceptions.ParserPoolAddressNotInSubnetError(start, subnet)

        if ipv4_end not in subnet:
            raise exceptions.ParserPoolAddressNotInSubnetError(end, subnet)

        pool_str = f"{start}-{end}"
        for existing_pool in existing_subnet.pools:
            if existing_pool.pool == pool_str:
                raise exceptions.ParserSubnetPoolAlreadyExistError(id, pool_str)

        pool = Pool(pool=pool_str, **kwargs)
        existing_subnet.pools.append(pool)
        return existing_subnet

    def get_shared_network_by_subnet(self, subnet: str) -> SharedNetwork4:
        """Attempts to return the first found Shared Network based on subnet CIDR

        Args:
            subnet:     Subnet CIDR (eg. 192.0.2.0/24)
        """
        for shared_network in self.config.shared_networks:
            for existing_subnet in shared_network.subnet4:
                if existing_subnet.subnet == subnet:
                    return shared_network

    def get_shared_network_by_reservation(self, ip_address: str) -> SharedNetwork4:
        """Attempts to return the first found Shared Network based on a reservations
        IP address

        Args:
            ip_address:     IPv4 address of the reservation
        """
        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet4:
                for reservation in subnet.reservations:
                    if reservation.ip_address == ip_address:
                        return shared_network

    def get_subnet_by_reservation(self, ip_address: str) -> Subnet4:
        """Attempts to return the first subnet found based on a reservations IP address
        starting with global subnets first and then shared networks

        Args:
            ip_address:     IPv4 address of the reservation
        """
        for subnet in self.config.subnet4:
            for reservation in subnet.reservations:
                if reservation.ip_address == ip_address:
                    return subnet

        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet4:
                for reservation in subnet.reservations:
                    if reservation.ip_address == ip_address:
                        return subnet

    def get_subnet_by_default_gateway(self, ip_address: str) -> Subnet4:
        """Attempts to return the first subnet found based on the default gateway (option 3)
        starting with global subnets first and then shared networks

        Args:
            ip_address:     IP address of default gateway
        """
        for subnet in self.config.subnet4:
            for option_data in subnet.option_data:
                if option_data.code == 3 and option_data.data == ip_address:
                    return subnet

        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet4:
                for option_data in subnet.option_data:
                    if option_data.code == 3 and option_data.data == ip_address:
                        return subnet

    def get_subnet_by_pool(self, pool: str) -> Subnet4:
        """Attempts to return the first subnet found based on the pool starting with
        global subnets first and then shared networks

        Args:
            pool:       Pool eg. 192.0.2.1-192.0.2.254
        """
        for subnet in self.config.subnet4:
            for existing_pool in subnet.pools:
                if existing_pool.pool == pool:
                    return subnet

        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet4:
                for existing_pool in subnet.pools:
                    if existing_pool.pool == pool:
                        return subnet

    def get_reservation_by(
        self, identifier_type: HostReservationIdentifierEnum, identifier_data: str
    ) -> Reservation4:
        """Attempts to return the first found reservation based on the provided
        identifier_type to look for (eg. ip_address, hw_address, flex_id, etc...)

        Args:
            identifier_type:    HostReservationIdentifierEnum
            identifier_data:    Data to match identifier type
        """
        identifier_type = identifier_type.value.replace("-", "_")
        if not Reservation4.__fields__.get(
            identifier_type
        ):  # Is this the best way to check fields in Pydantic??
            raise exceptions.ParserInvalidHostReservationIdentifierError(
                identifier_type
            )

        for subnet in self.config.subnet4:
            for reservation in subnet.reservations:
                if getattr(reservation, identifier_type) == identifier_data:
                    return reservation

        for network in self.config.shared_networks:
            for subnet in network.subnet4:
                for reservation in subnet.reservations:
                    if getattr(reservation, identifier_type) == identifier_data:
                        return reservation

    def get_reservation_by_ip(self, ip_address: str) -> Reservation4:
        """Attempts to return the first found reservation based on the provided
        IP address reservation by first looking at the global subnets, then
        the shared networks

        Args:
            ip_address:     IP Address of Reservation
        """
        for subnet in self.config.subnet4:
            for reservation in subnet.reservations:
                if reservation.ip_address == ip_address:
                    return reservation

        for network in self.config.shared_networks:
            for subnet in network.subnet4:
                for reservation in subnet.reservations:
                    if reservation.ip_address == ip_address:
                        return reservation

    def get_reservation_by_hw_address(self, hw_address: str) -> Reservation4:
        """Attempts to return the first found reservation based on hw_address

        Args:
            hw_address:     MAC Address
        """
        return self.get_reservation_by(
            HostReservationIdentifierEnum.hw_address, hw_address
        )

    def get_reservation_by_client_id(self, client_id: str) -> Reservation4:
        """Attempts to return the first found reservation based on client_id

        Args:
            client_id:      Client ID
        """
        return self.get_reservation_by(
            HostReservationIdentifierEnum.client_id, client_id
        )

    def get_reservation_by_circuit_id(self, circuit_id: str) -> Reservation4:
        """Attempts to return the first found reservation based on circuit_id

        Args:
            circuit_id:     Circuit ID
        """
        return self.get_reservation_by(
            HostReservationIdentifierEnum.circuit_id, circuit_id
        )

    def get_reservation_by_flex_id(self, flex_id: str) -> Reservation4:
        """Attempts to return the first found reservation based on flex_id

        Args:
            flex_id:        Flex ID
        """
        return self.get_reservation_by(HostReservationIdentifierEnum.flex_id, flex_id)

    def remove_reservation(self, id: int, ip_address: str) -> Reservation4:
        """Attempts to remove a reservation from a given subnet and returns
        the reservation

        Args:
            id:             Subnet ID
            ip_address:     IPv4 address of the subnet
        """
        existing_subnet = self.get_subnet(id)
        if not existing_subnet:
            raise exceptions.ParserSubnetNotFoundError(id)

        for index, existing_reservation in enumerate(existing_subnet.reservations):
            if existing_reservation.ip_address == ip_address:
                reservation = existing_subnet.reservations.pop(index)
                return reservation

    def remove_subnet_pool(self, id: int, pool: str) -> Pool:
        """Attempts to remove a pool from a given subnet and returns
        the reservation

        Args:
            id:     Subnet ID
            pool:   Pool
        """
        existing_subnet = self.get_subnet(id)
        if not existing_subnet:
            raise exceptions.ParserSubnetNotFoundError(id)

        for index, existing_pool in enumerate(existing_subnet.pools):
            if existing_pool.pool == pool:
                pool = existing_subnet.pools.pop(index)
                return pool

    def remove_subnet_from_shared_network(self, id: int, name: str) -> Subnet4:
        """Attempts to remove a subnet from a given shared network and
        returns the subnet

        Args:
            id:     Subnet ID
            name:   Name of the shared network
        """
        existing_shared_network = self.get_shared_network(name)
        if not existing_shared_network:
            raise exceptions.ParserSharedNetworkNotFoundError(name)

        for index, existing_subnet in enumerate(existing_shared_network.subnet4):
            if existing_subnet.id == id:
                subnet = existing_shared_network.subnet4.pop(index)
                return subnet

    def remove_subnet(self, id: int) -> Subnet4:
        """Attempts to remove a subnet from the global subnets and returns
        the subnet

        Args:
            id: Subnet ID
        """
        for index, existing_subnet in enumerate(self.config.subnet4):
            if existing_subnet.id == id:
                subnet = self.config.subnet4.pop(index)
                return subnet

    def remove_shared_network(
        self, name: str, keep_subnets: bool = False
    ) -> SharedNetwork4:
        """Attempts to remove a shared network and returns the
        shared network, if any subnets are found in here, it will also delete them
        unless you specify keep_subnets as True

        Args:
            name:           Name of the shared network
            keep_subnets:   Moves any subnets into the global subnet configuration if True
        """
        for index, existing_shared_network in enumerate(self.config.shared_networks):
            if existing_shared_network.name == name:
                if keep_subnets:
                    for subnet in existing_shared_network.subnet4:
                        self.config.subnet4.append(subnet)

                shared_network = self.config.shared_networks.pop(index)
                return shared_network
