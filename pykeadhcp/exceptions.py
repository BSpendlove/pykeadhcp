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
        self.message = f"Subnet with id '{subnet_id}' not found"
        super().__init__(self.message)


class KeaLeaseNotFoundException(KeaException):
    def __init__(self, lease: str):
        self.message = f"Lease '{lease}' not found"
        super().__init__(self.message)
