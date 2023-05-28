class GenericParserError(Exception):
    def __init__(self, message: str = "Encountered generic parser error"):
        self.message = message
        super().__init__(self.message)


class ParserSubnetIDAlreadyExistError(GenericParserError):
    def __init__(self, id: int):
        self.message = f"Subnet with same ID {id} already exist in local configuration"
        super().__init__(self.message)


class ParserSubnetCIDRAlreadyExistError(GenericParserError):
    def __init__(self, cidr: str):
        self.message = (
            f"Subnet with same CIDR {cidr} already exist in local configuration"
        )
        super().__init__(self.message)


class ParserSharedNetworkAlreadyExistError(GenericParserError):
    def __init__(self, name: str):
        self.message = f"Shared Network with name {name} already exists"
        super().__init__(self.message)


class ParserSharedNetworkNotFoundError(GenericParserError):
    def __init__(self, name: str):
        self.message = f"Shared Network with name {name} does not exist"
        super().__init__(self.message)


class ParserSubnetNotFoundError(GenericParserError):
    def __init__(self, id: int):
        self.message = f"Subnet with ID {id} does not exist"
        super().__init__(self.message)


class ParserReservationAlreadyExistError(GenericParserError):
    def __init__(self, ip_address: str):
        self.message = f"Reservation with IP Address {ip_address} already exist"
        super().__init__(self.message)


class ParserReservationNotFoundError(GenericParserError):
    def __init__(self, ip_address: str):
        self.message = f"Reservation with IP Address {ip_address} not found"
        super().__init__(self.message)


class ParserOptionDataAlreadyExistError(GenericParserError):
    def __init__(self, object: str, code: int):
        self.message = f"Option {code} already exist on object {object}"
        super().__init__(self.message)


class ParserSubnetPoolAlreadyExistError(GenericParserError):
    def __init__(self, id: int, pool: str):
        self.message = f"Pool {pool} already exist in subnet {id}"
        super().__init__(self.message)


class ParserPoolInvalidAddressError(GenericParserError):
    def __init__(self, start: str, end: str):
        self.message = (
            f"Start ({start}) or End IP ({end}) for pool is not a valid IP address"
        )
        super().__init__(self.message)


class ParserPoolAddressNotInSubnetError(GenericParserError):
    def __init__(self, address: str, subnet: str):
        self.message = (
            f"Pool Start or End address {address} is not within subnet {subnet}"
        )
        super().__init__(self.message)


class ParserInvalidHostReservationIdentifierError(GenericParserError):
    def __init__(self, identifier_type: str):
        self.message = f"Identifier Typer {identifier_type} is not a valid type"
        super().__init__(self.message)


class ParserPDPoolAlreadyExistError(GenericParserError):
    def __init__(self, prefix: str, prefix_len: int, id: int):
        self.message = (
            f"PD Prefix {prefix}/{prefix_len} already exist in a subnet ({id})"
        )
        super().__init__(self.message)


class ParserPDPoolNotFoundError(GenericParserError):
    def __init__(self, id: int, prefix: str, prefix_len: int):
        self.message = f"Unable to find PD Prefix {prefix}/{prefix_len} in subnet {id}"
        super().__init__(self.message)
