class KeaException(Exception):
    def __init__(self, message: str = "Kea Exception encountered"):
        self.message = message
        super().__init__(self.message)


class KeaGenericException(KeaException):
    # Result code 1
    def __init__(
        self,
        message: str = "Code 1: a general error or failure has occurred during the command processing.",
    ):
        self.message = message
        super().__init__(self.message)


class KeaCommandNotSupportedException(KeaException):
    # Result code 2
    def __init__(
        self,
        message: str = "Code 2: the specified command is unsupported by the server receiving it.",
    ):
        self.message = message
        super().__init__(self.message)


class KeaObjectNotFoundException(KeaException):
    # Result code 3
    def __init__(
        self,
        message: str = "Code 3: the requested operation has been completed but the requested resource was not found. This status code is returned when a command returns no resources or affects no resources.",
    ):
        self.message = message
        super().__init__(self.message)


class KeaServerConflictException(KeaException):
    # Result code 4
    def __init__(
        self,
        message: str = "Code 4: the well-formed command has been processed but the requested changes could not be applied, because they were in conflict with the server state or its notion of the configuration.",
    ):
        self.message = message
        super().__init__(self.message)


class KeaUnauthorizedAccessException(KeaException):
    def __init__(
        self,
        message: str = "Received 401 (Unauthorized response), please ensure username and password is configured, and use_basic_auth is set to True for the Kea object",
    ):
        self.message = message
        super().__init__(self.message)


class KeaHookLibraryNotConfiguredException(KeaException):
    def __init__(self, service: str, hook: str):
        self.message = f"Hook library '{hook}' is not configured for '{service}' service. Please ensure this is enabled in the configuration for the '{service}' daemon"
        super().__init__(self.message)


class KeaSharedNetworkNotFoundException(KeaException):
    def __init__(self, name: str):
        self.message = f"Shared Network '{name}' not found"
        super().__init__(self.message)


class KeaSubnetNotFoundException(KeaException):
    def __init__(self, subnet_id: int):
        self.message = f"Subnet '{subnet_id}' not found"
        super().__init__(self.message)


class KeaLeaseNotFoundException(KeaException):
    def __init__(self, lease: str):
        self.message = f"Lease '{lease}' not found"
        super().__init__(self.message)


class KeaInvalidRemoteMapException(KeaException):
    def __init__(self, detailed_error: str):
        self.message = f"Remote map for cm_cmd remote API call is not correctly formatted. Detailed Error: {detailed_error}"
        super().__init__(self.message)


class KeaRemoteServerNotFoundException(KeaException):
    def __init__(self, server_tag: str):
        self.message = f"Server with server_tag '{server_tag}' not found"
        super().__init__(self.message)


class KeaConfigBackendNotConfiguredException(KeaException):
    def __init__(self):
        self.message = "Kea API reports that there is no configuration backends"
        super().__init__(self.message)


class KeaUnknownHostReservationTypeException(KeaException):
    def __init__(self, reservation_type: str):
        self.message = (
            f"Reservation type '{reservation_type}' is not a valid reservation type"
        )
        super().__init__(self.message)


class KeaReservationNotFoundException(KeaException):
    def __init__(self, reservation_data: str):
        self.message = f"Reservation '{reservation_data}' not found"
        super().__init__(self.message)


class KeaClientClassNotFoundException(KeaException):
    def __init__(self, client_class: str):
        self.message = f"Client Class '{client_class}' not found"
        super().__init__(self.message)
