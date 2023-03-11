from requests.models import Response
import requests

from pykeadhcp.daemons import CtrlAgent, Ddns, Dhcp4, Dhcp6


class Kea:
    """Basic wrapper around requests module for interacting with the
    Kea Management API for the various daemons supported.

    Args:
        ip:         IP address of the Kea server
        port:       TCP Port of the Kea Server to access the API
        headers:    Headers to inject in every POST request sent to the API
    """

    def __init__(
        self, host: str, port: int, headers: dict = {"Content-Type": "application/json"}
    ):
        self.host = host
        self.port = port
        self.headers = headers
        self.ctrlagent = CtrlAgent(self)
        self.ddns = Ddns(self)
        self.dhcp4 = Dhcp4(self)
        self.dhcp6 = Dhcp6(self)
        self.services = ["dhcp4", "dhcp6", "ddns", None]  # None = Control-Agent Daemon

        self.url = f"{self.host}:{self.port}"

    def post(self, endpoint: str, body: dict, **kwargs) -> dict:
        """Handles simple POST operation and basic header injection

        Args:
            endpoint:       API Endpoint
            body:           JSON body to send
        """
        url = self.url + endpoint
        response = requests.post(url=url, json=body, headers=self.headers, **kwargs)

        if response.status_code >= 400 and response.status_code <= 500:
            response.raise_for_status()

        data = response.json()
        return data[0]  # Kea API returns all data in a list, lets normalize that...

    def send_command(self, command: str, service: str) -> dict:
        """Sends a command to the specific API daemon

        Args:
            command:        Supported command by the daemons API
            service:        Service to send request to
        """
        if service and service.lower() not in self.services:
            raise TypeError(
                f"Service {service} is not a supported service. The supported services are {self.services}"
            )

        return self.post(
            endpoint="/",
            body={"command": command, "service": [service] if service else []},
        )

    def send_command_with_arguments(
        self, command: str, service: str, arguments: dict
    ) -> dict:
        """Sends a command to the specific API daemon with provided arguments

        Args:
            command:        Supported command by the daemons API
            service:        Service to send request to
            arguments:      Argument parameters to pass to the command/service
        """
        if service and service.lower() not in self.services:
            raise TypeError(
                f"Service {service} is not a supported service. The supported services are {self.services}"
            )

        return self.post(
            endpoint="/",
            body={
                "command": command,
                "service": [service] if service else [],
                "arguments": arguments,
            },
        )
