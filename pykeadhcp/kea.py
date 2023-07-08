import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from pathlib import Path
from typing import List, Union
from pydantic import ValidationError

from pykeadhcp.daemons import CtrlAgent, Ddns, Dhcp4, Dhcp6
from pykeadhcp.models.generic import KeaResponse
from pykeadhcp.models.generic.hook import Hook
from pykeadhcp.models.generic.remote_map import RemoteMap
from pykeadhcp.exceptions import (
    KeaGenericException,
    KeaCommandNotSupportedException,
    KeaObjectNotFoundException,
    KeaServerConflictException,
    KeaUnauthorizedAccessException,
    KeaHookLibraryNotConfiguredException,
    KeaInvalidRemoteMapException,
)


class Kea:
    """Basic wrapper around requests module for interacting with the
    Kea Management API for the various daemons supported.

    Args:
        ip:                     IP address of the Kea server
        port:                   TCP Port of the Kea Server to access the API
        headers:                Headers to inject in every POST request sent to the API
        use_basic_auth:         Use HTTP Basic Auth if Kea is configured for it
        username:               Username for HTTP Basic Auth
        password:               Password for HTTP Basic Auth
        raise_generic_errors:   If True, it will raise a generic error based on Kea Documentation
            (as per self.RESPONSE_CODES). Set this to False if you want to catch the API endpoint specific
            errors such as `v4 Shared Network not found` vs `Code 3: the requested operation has been completed but the requested resource was not found.
            This status code is returned when a command returns no resources or affects no resources.`
        verify:                 Boolean is used if the server TLS cert is verified or not, however you can
            pass in a string which should be a path to a CA bundle to use with each request.
    """

    def __init__(
        self,
        host: str,
        port: int,
        headers: dict = {"Content-Type": "application/json"},
        use_basic_auth: bool = False,
        username: str = "",
        password: str = "",
        raise_generic_errors: bool = False,
        verify: Union[bool, str] = True,
    ):
        self.host = host
        self.port = port
        self.headers = headers
        self.use_basic_auth = use_basic_auth
        self.basic_auth = HTTPBasicAuth(username, password)
        self.services = ["dhcp4", "dhcp6", "ddns", None]  # None = Control-Agent Daemon
        self.url = f"{self.host}:{self.port}"
        self.raise_generic_errors = raise_generic_errors
        self.verify = verify
        self.RESPONSE_CODES = {
            1: KeaGenericException,
            2: KeaCommandNotSupportedException,
            3: KeaObjectNotFoundException,
            4: KeaServerConflictException,
        }
        self.hook_library = {}
        self.ctrlagent = CtrlAgent(self)
        self.ddns = Ddns(self)
        self.dhcp4 = Dhcp4(self)
        self.dhcp6 = Dhcp6(self)

    def get_active_hooks(self, hooks: List[dict]) -> List[Hook]:
        """Returns a list of Hook objects

        Args:
            hooks:      List of hook libraries
        """
        hook_libraries = [
            Hook(
                library=hook["library"],
                parameters=hook.get("parameters", {}),
                name=self.get_hook_name(hook["library"]),
            )
            for hook in hooks
        ]
        return hook_libraries

    def get_hook_name(self, hook_path: str) -> str:
        """Returns a friendly name for the hook library similar to Kea Documentation

        eg. if the library path is: /usr/lib/x86_64-linux-gnu/kea/hooks/libdhcp_lease_cmds.so
        then we can simply take the file name, remove the suffix and `libdhcp_` part to get `lease_cmds`.

        Args:
            hook_path:      Hook Library Path
        """
        file = Path(hook_path)
        filename = file.stem.split("libdhcp_")[-1]
        return filename

    def is_hook_enabled(self, hook: str, hook_library: List[Hook]) -> bool:
        """Checks the provided hook library if the hook is configured on the specific Daemon config

        Args:
            hook:           Name of hook (shortname as per documentation) to check
            hook_library:   List of Hooks enabled
        """
        for configured_hook in hook_library:
            if not configured_hook.name:
                continue

            if hook == configured_hook.name:
                return True

        return False

    def post(self, endpoint: str, body: dict, **kwargs) -> KeaResponse:
        """Handles simple POST operation and basic header injection

        Args:
            endpoint:       API Endpoint
            body:           JSON body to send
        """
        url = self.url + endpoint
        response = requests.post(
            url=url,
            json=body,
            headers=self.headers,
            auth=self.basic_auth if self.use_basic_auth else None,
            verify=self.verify,
            **kwargs,
        )

        if response.status_code == 401:
            raise KeaUnauthorizedAccessException

        if response.status_code >= 400 and response.status_code <= 500:
            response.raise_for_status()

        data = response.json()
        if not data:
            return None

        data = data[0]  # Kea API returns everything in a list
        result_code = data["result"]
        if self.raise_generic_errors and result_code != 0:
            raise self.RESPONSE_CODES.get(
                result_code, KeaGenericException
            )  # Return Generic Exception if code not found

        return KeaResponse(**data)

    def send_command(
        self, command: str, service: str, required_hook: str = ""
    ) -> KeaResponse:
        """Sends a command to the specific API daemon

        Args:
            command:        Supported command by the daemons API
            service:        Service to send request to
            required_hook:  Precheck if hook library is enabled
        """
        if service and service.lower() not in self.services:
            raise TypeError(
                f"Service {service} is not a supported service. The supported services are {self.services}"
            )

        if required_hook and not self.is_hook_enabled(
            required_hook, self.hook_library[service]
        ):
            raise KeaHookLibraryNotConfiguredException(service, required_hook)

        command_results = self.post(
            endpoint="/",
            body={"command": command, "service": [service] if service else []},
        )
        return command_results

    def send_command_with_arguments(
        self, command: str, service: str, arguments: dict, required_hook: str = ""
    ) -> KeaResponse:
        """Sends a command to the specific API daemon with provided arguments

        Args:
            command:        Supported command by the daemons API
            service:        Service to send request to
            arguments:      Argument parameters to pass to the command/service
            required_hook:  Precheck if hook library is enabled
        """
        if service and service.lower() not in self.services:
            raise TypeError(
                f"Service {service} is not a supported service. The supported services are {self.services}"
            )

        if required_hook and not self.is_hook_enabled(
            required_hook, self.hook_library[service]
        ):
            raise KeaHookLibraryNotConfiguredException(service, required_hook)

        command_results = self.post(
            endpoint="/",
            body={
                "command": command,
                "service": [service] if service else [],
                "arguments": arguments,
            },
        )
        return command_results

    def send_command_remote(
        self, command: str, service: str, arguments: dict = {}, remote_map: dict = {}
    ):
        """Sends a command to the specific API daemon with provided arguments and remote map settings

        This command should only be used with the cb_cmds hook.

        Args:
            command:        Supported command by the daemons API
            service:        Service to send request to
            arguments:      Argument parameters to pass to the command/service
            required_hook:  Precheck if hook library is enabled
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database
        """
        if service and service.lower() not in self.services:
            raise TypeError(
                f"Service {service} is not a supported service. The supported services are {self.services}"
            )

        # All remote commands require cb_cmds hook to be loaded
        if not self.is_hook_enabled("cb_cmds", self.hook_library[service]):
            raise KeaHookLibraryNotConfiguredException(service, "cb_cmds")

        # Build remote payload if user wants to select a specific database instance as per API documentation
        # https://kea.readthedocs.io/en/kea-2.2.0/arm/hooks.html#command-structure
        if remote_map:
            try:
                remote_map_parsed = RemoteMap.parse_obj(remote_map)
            except ValidationError as err:
                raise KeaInvalidRemoteMapException(str(err))
            except Exception as err:
                raise KeaInvalidRemoteMapException(f"Generic Exception caught: {err}")

            arguments["remote"] = remote_map_parsed.dict(
                exclude_unset=True, exclude_none=True
            )

        command_results = self.post(
            endpoint="/",
            body={
                "command": command,
                "service": [service] if service else [],
                "arguments": arguments,
            },
        )
        return command_results

    def get_next_available_subnet_id(self, subnet_ids: List[int]) -> int:
        """Returns the next available subnet-id based on a given list of
        existing subnet-ids

        Args:
            subnet_ids:     Existing list of subnet-ids gathered via
                subnet4_list/subnet6_list or manually gathered via parser
        """
        next_id = next(
            i for i, e in enumerate(sorted(subnet_ids) + [None], 1) if i != e
        )
        return next_id
