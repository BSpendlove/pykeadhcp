from pykeadhcp.parsers.generic import GenericParser
from pykeadhcp.models.dhcp6.config import Dhcp6DaemonConfig
from pykeadhcp.models.dhcp6.shared_network import SharedNetwork6
from pykeadhcp.models.dhcp6.subnet import Subnet6
from pykeadhcp.models.dhcp6.reservation import Reservation6
from pykeadhcp.models.generic.pool import Pool
from pykeadhcp.models.dhcp6.pd_pool import PDPool
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.models.enums import HostReservationIdentifierEnum
from pykeadhcp.parsers import exceptions

from ipaddress import IPv6Address, IPv6Network


class Dhcp6Parser(GenericParser):
    """Parser for the ISC Kea Dhcp6 configuration file. This should ideally
    be used with the cached config stored in the Daemon class like this:

    parser = Dhcp6Parser(config=server.dhcp6.cached_config)
    """

    def __init__(self, config: dict):
        self.config = Dhcp6DaemonConfig.parse_obj(config["Dhcp6"])

    def get_shared_network(self, name: str) -> SharedNetwork6:
        """Returns a specific Dhcp6 shared-network

        Args:
            name:       Name of the shared-network
        """
        for shared_network in self.config.shared_networks:
            if shared_network.name == name:
                return shared_network

    def get_subnet(self, id: int) -> Subnet6:
        """Attempts to return the first found subnet based on the subnets id using
        global subnets first then shared-networks last.

        Args:
            id:     ID of the subnet
        """
        for subnet in self.config.subnet6:
            if subnet.id == id:
                return subnet

        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet6:
                if subnet.id == id:
                    return subnet

    def get_subnet_by_cidr(self, cidr: str) -> Subnet6:
        """Attempts to return the first found subnet based on the provided cidr
        using global subnets first and then shared-networks last.

        Args:
            cidr:       IPv6 CIDR (eg. 2001:db8::/64)
        """
        for subnet in self.config.subnet6:
            if subnet.subnet == cidr:
                return subnet

        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet6:
                if subnet.subnet == cidr:
                    return subnet

    def add_shared_network(self, name: str, **kwargs) -> SharedNetwork6:
        """Attempts to add a shared network if it doesn't already
        exist

        Args:
            name:       Name of the shared network
        """
        if self.get_shared_network(name):
            raise exceptions.ParserSharedNetworkAlreadyExistError(name)
        network = SharedNetwork6(name=name, **kwargs)
        self.config.shared_networks.append(network)
        return network

    def add_subnet(self, id: int, subnet: str, **kwargs) -> Subnet6:
        """Attempts to add a Subnet if it doesn't already exist

        Args:
            id:         Subnet Id
            subnet:     Subnet (CIDR eg. 2001:db8::/64)
        """
        if self.get_subnet(id):
            raise exceptions.ParserSubnetIDAlreadyExistError(id)

        if self.get_subnet_by_cidr(subnet):
            raise exceptions.ParserSubnetCIDRAlreadyExistError(subnet)

        subnet = Subnet6(id=id, subnet=subnet, **kwargs)
        self.config.subnet6.append(subnet)
        return subnet

    def add_subnet_to_shared_network(self, id: int, name: str) -> Subnet6:
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

        for index, subnet in enumerate(self.config.subnet6):
            if existing_subnet.id != subnet.id:
                continue

            subnet_to_assosicate = self.config.subnet6.pop(index)
            existing_network.subnet6.append(subnet_to_assosicate)
            return subnet_to_assosicate

    def add_reservation_to_subnet(
        self, id: int, ip_address: str, **kwargs
    ) -> Reservation6:
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

        reservation = Reservation6(ip_addresses=[ip_address], **kwargs)
        existing_subnet.reservations.append(reservation)
        return reservation

    def add_dhcp_option_to_subnet(
        self, id: int, code: int, data: str, **kwargs
    ) -> Subnet6:
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
    ) -> SharedNetwork6:
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

    def add_pool_to_subnet(self, id: int, start: str, end: str, **kwargs) -> Subnet6:
        """Attempts to add a pool to an existing subnet

        Args:
            id:     Subnet ID
            start:  Pool Start
            end:    Pool End
        """
        try:
            ipv6_start = IPv6Address(start)
            ipv6_end = IPv6Address(end)
        except:
            raise exceptions.ParserPoolInvalidAddressError(start, end)

        existing_subnet = self.get_subnet(id)
        if not existing_subnet:
            raise exceptions.ParserSubnetNotFoundError(id)

        subnet = IPv6Network(existing_subnet.subnet)
        if ipv6_start not in subnet:
            raise exceptions.ParserPoolAddressNotInSubnetError(start, subnet)

        if ipv6_end not in subnet:
            raise exceptions.ParserPoolAddressNotInSubnetError(end, subnet)

        pool_str = f"{start}-{end}"
        for existing_pool in existing_subnet.pools:
            if existing_pool.pool == pool_str:
                raise exceptions.ParserSubnetPoolAlreadyExistError(id, pool_str)

        pool = Pool(pool=pool_str, **kwargs)
        existing_subnet.pools.append(pool)
        return existing_subnet

    def get_shared_network_by_subnet(self, subnet: str) -> SharedNetwork6:
        """Attempts to return the first found Shared Network based on subnet CIDR

        Args:
            subnet:     Subnet CIDR (eg. 2001:db8::/64)
        """
        for shared_network in self.config.shared_networks:
            for existing_subnet in shared_network.subnet6:
                if existing_subnet.subnet == subnet:
                    return shared_network

    def get_shared_network_by_reservation(self, ip_address: str) -> SharedNetwork6:
        """Attempts to return the first found Shared Network based on a reservations
        IP address

        Args:
            ip_address:     IPv6 address of the reservation
        """
        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet6:
                for reservation in subnet.reservations:
                    for ip in reservation.ip_addresses:
                        if ip == ip_address:
                            return shared_network

    def get_subnet_by_reservation(self, ip_address: str) -> Subnet6:
        """Attempts to return the first subnet found based on a reservations IP address
        starting with global subnets first and then shared networks

        Args:
            ip_address:     IPv6 address of the reservation
        """
        for subnet in self.config.subnet6:
            for reservation in subnet.reservations:
                for ip in reservation.ip_addresses:
                    if ip == ip_address:
                        return subnet

        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet6:
                for reservation in subnet.reservations:
                    for ip in reservation.ip_addresses:
                        if ip == ip_address:
                            return subnet

    def get_subnet_by_default_gateway(self, ip_address: str) -> Subnet6:
        """Attempts to return the first subnet found based on the default gateway (option 3)
        starting with global subnets first and then shared networks

        Args:
            ip_address:     IP address of default gateway
        """
        for subnet in self.config.subnet6:
            for option_data in subnet.option_data:
                if option_data.code == 3 and option_data.data == ip_address:
                    return subnet

        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet6:
                for option_data in subnet.option_data:
                    if option_data.code == 3 and option_data.data == ip_address:
                        return subnet

    def get_subnet_by_pool(self, pool: str) -> Subnet6:
        """Attempts to return the first subnet found based on the pool starting with
        global subnets first and then shared networks

        Args:
            pool:       Pool eg. 2001:db8::1-2001:db8::FFFF
        """
        for subnet in self.config.subnet6:
            for existing_pool in subnet.pools:
                if existing_pool.pool == pool:
                    return subnet

        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet6:
                for existing_pool in subnet.pools:
                    if existing_pool.pool == pool:
                        return subnet

    def get_reservation_by(
        self, identifier_type: HostReservationIdentifierEnum, identifier_data: str
    ) -> Reservation6:
        """Attempts to return the first found reservation based on the provided
        identifier_type to look for (eg. ip_address, hw_address, flex_id, etc...)

        Args:
            identifier_type:    HostReservationIdentifierEnum
            identifier_data:    Data to match identifier type
        """
        identifier_type = identifier_type.value.replace("-", "_")
        if not Reservation6.__fields__.get(
            identifier_type
        ):  # Is this the best way to check fields in Pydantic??
            raise exceptions.ParserInvalidHostReservationIdentifierError(
                identifier_type
            )

        for subnet in self.config.subnet6:
            for reservation in subnet.reservations:
                if getattr(reservation, identifier_type) == identifier_data:
                    return reservation

        for network in self.config.shared_networks:
            for subnet in network.subnet6:
                for reservation in subnet.reservations:
                    if getattr(reservation, identifier_type) == identifier_data:
                        return reservation

    def get_reservation_by_ip(self, ip_address: str) -> Reservation6:
        """Attempts to return the first found reservation based on the provided
        IP address reservation by first looking at the global subnets, then
        the shared networks

        Args:
            ip_address:     IP Address of Reservation
        """
        for subnet in self.config.subnet6:
            for reservation in subnet.reservations:
                for ip in reservation.ip_addresses:
                    if ip == ip_address:
                        return reservation

        for network in self.config.shared_networks:
            for subnet in network.subnet6:
                for reservation in subnet.reservations:
                    for ip in reservation.ip_addresses:
                        if ip == ip_address:
                            return reservation

    def get_reservation_by_hw_address(self, hw_address: str) -> Reservation6:
        """Attempts to return the first found reservation based on hw_address

        Args:
            hw_address:     MAC Address
        """
        return self.get_reservation_by(
            HostReservationIdentifierEnum.hw_address, hw_address
        )

    def get_reservation_by_flex_id(self, flex_id: str) -> Reservation6:
        """Attempts to return the first found reservation based on flex_id

        Args:
            flex_id:        Flex ID
        """
        return self.get_reservation_by(HostReservationIdentifierEnum.flex_id, flex_id)

    def get_reservation_by_duid(self, duid: str) -> Reservation6:
        """Attempts to return the first found reservation based on duid

        Args:
            duid:   DHCP Unique Identifier
        """
        return self.get_reservation_by(HostReservationIdentifierEnum.duid, duid)

    def remove_reservation(self, id: int, ip_address: str) -> Reservation6:
        """Attempts to remove a reservation from a given subnet and returns
        the reservation

        Args:
            id:             Subnet ID
            ip_address:     IPv6 address of the subnet
        """
        existing_subnet = self.get_subnet(id)
        if not existing_subnet:
            raise exceptions.ParserSubnetNotFoundError(id)

        for index, existing_reservation in enumerate(existing_subnet.reservations):
            for ip in existing_reservation.ip_addresses:
                if ip == ip_address:
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

    def remove_subnet_from_shared_network(self, id: int, name: str) -> Subnet6:
        """Attempts to remove a subnet from a given shared network and
        returns the subnet

        Args:
            id:     Subnet ID
            name:   Name of the shared network
        """
        existing_shared_network = self.get_shared_network(name)
        if not existing_shared_network:
            raise exceptions.ParserSharedNetworkNotFoundError(name)

        for index, existing_subnet in enumerate(existing_shared_network.subnet6):
            if existing_subnet.id == id:
                subnet = existing_shared_network.subnet6.pop(index)
                return subnet

    def remove_subnet(self, id: int) -> Subnet6:
        """Attempts to remove a subnet from the global subnets and returns
        the subnet

        Args:
            id: Subnet ID
        """
        for index, existing_subnet in enumerate(self.config.subnet6):
            if existing_subnet.id == id:
                subnet = self.config.subnet6.pop(index)
                return subnet

    def remove_shared_network(
        self, name: str, keep_subnets: bool = False
    ) -> SharedNetwork6:
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
                    for subnet in existing_shared_network.subnet6:
                        self.config.subnet6.append(subnet)

                shared_network = self.config.shared_networks.pop(index)
                return shared_network

    def get_subnet_from_pd_pool(self, prefix: str, prefix_len: int) -> Subnet6:
        """Attempts to return the first found subnet that has a PD Pool with
        matching prefix/len/delegated-len, searches in global subnets first
        and then shared networks"""
        for subnet in self.config.subnet6:
            for pd_pool in subnet.pd_pools:
                if pd_pool.prefix == prefix and pd_pool.prefix_len == prefix_len:
                    return subnet

        for shared_network in self.config.shared_networks:
            for subnet in shared_network.subnet6:
                for pd_pool in subnet.pd_pools:
                    if pd_pool.prefix == prefix and pd_pool.prefix_len == prefix_len:
                        return subnet

    def add_pd_pool(
        self, id: int, prefix: str, prefix_len: int, delegated_len: int, **kwargs
    ) -> PDPool:
        """Attempts to add a PD Pool to an existing subnet

        Args:
            id:             Subnet ID
            prefix:         IPv6 PD Prefix
            prefix_len:     IPv6 PD Prefix Length
            delegated_len:  IPv6 PD Pool Length (for client)
        """
        existing_subnet = self.get_subnet(id)
        if not existing_subnet:
            raise exceptions.ParserSubnetNotFoundError(id)

        existing_subnet_with_pd_pool = self.get_subnet_from_pd_pool(prefix, prefix_len)
        if existing_subnet_with_pd_pool:
            raise exceptions.ParserPDPoolAlreadyExistError(
                prefix, prefix_len, existing_subnet_with_pd_pool.id
            )

        pool = PDPool(
            prefix=prefix, prefix_len=prefix_len, delegated_len=delegated_len, **kwargs
        )
        existing_subnet.pd_pools.append(pool)
        return pool

    def remove_pd_pool(self, id: int, prefix: str, prefix_len: int) -> PDPool:
        """Attempts to remove a PD Pool from a given subnet

        Args:
            id:         Subnet ID
            prefix:     IPv6 PD Prefix
            prefix_len: IPv6 PD Prefix Length
        """
        existing_subnet_from_pd_pool = self.get_subnet_from_pd_pool(prefix, prefix_len)
        if not existing_subnet_from_pd_pool:
            raise exceptions.ParserPDPoolNotFoundError(id, prefix, prefix_len)

        for index, existing_pd_pool in enumerate(existing_subnet_from_pd_pool.pd_pools):
            if (
                existing_pd_pool.prefix == prefix
                and existing_pd_pool.prefix_len == prefix_len
            ):
                pd_pool = existing_subnet_from_pd_pool.pd_pools.pop(index)
                return pd_pool
