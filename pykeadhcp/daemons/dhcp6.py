from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from pykeadhcp import Kea

from pykeadhcp.models.generic import KeaResponse, StatusGet
from pykeadhcp.models.dhcp6.lease import Lease6
from pykeadhcp.models.dhcp6.pd_pool import PDPool
from pykeadhcp.models.dhcp6.reservation import Reservation6
from pykeadhcp.models.dhcp6.shared_network import SharedNetwork6
from pykeadhcp.models.dhcp6.subnet import Subnet6
from pykeadhcp.exceptions import (
    KeaHookLibraryNotConfiguredException,
    KeaSharedNetworkNotFoundException,
    KeaSubnetNotFoundException,
    KeaLeaseNotFoundException,
)


class Dhcp6:
    def __init__(self, api: "Kea"):
        self.service = "dhcp6"
        self.api = api

        # Cache config and hooks
        try:
            self.cached_config = self.config_get().arguments
            self.hook_libraries = self.api.get_active_hooks(
                hooks=self.cached_config[self.service.capitalize()]["hooks-libraries"]
            )
            self.api.hook_library[self.service] = self.hook_libraries
        except:
            pass

    def build_report(self) -> KeaResponse:
        """Returns list of compilation options that this particular binary was built with

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-build-report
        """
        return self.api.send_command(command="build-report", service=self.service)

    def config_get(self) -> KeaResponse:
        """Retrieves the current configuration used by the server

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-config-get
        """
        return self.api.send_command(command="config-get", service=self.service)

    def config_reload(self) -> KeaResponse:
        """Reloads the last good configuration (configuration file on disk)

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-config-reload
        """
        return self.api.send_command(command="config-reload", service=self.service)

    def config_set(self, config: dict) -> KeaResponse:
        """Replace the current server configuration with the provided configuration

        Args:
            config:     Configuration to set

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#config-set
        """
        return self.api.send_command_with_arguments(
            command="config-set", service=self.service, arguments=config
        )

    def config_test(self, config: dict) -> KeaResponse:
        """Check whether the configuration supplied can be loaded by the dhcp4 daemon

        Args:
            config:     Configuration to test

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#config-test
        """
        return self.api.send_command_with_arguments(
            command="config-test", service=self.service, arguments=config
        )

    def config_write(self, filename: str) -> KeaResponse:
        """Write the current configuration to a file on disk

        Args:
            filename:       Name of the configuration file

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#config-write
        """
        return self.api.send_command_with_arguments(
            command="config-write",
            service=self.service,
            arguments={"filename": filename},
        )

    def dhcp_disable(self, max_period: int = 20) -> KeaResponse:
        """Globally disables DHCP service (dhcp4)

        Args:
            max_period:     Time until DHCP service is automatically renabled in seconds

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-dhcp-disable
        """
        return self.api.send_command_with_arguments(
            command="dhcp-disable",
            service=self.service,
            arguments={"max-period": max_period, "origin": "user"},
        )

    def dhcp_enable(self) -> KeaResponse:
        """Globally enables the DHCP service (dhcp4)

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/arm/ctrl-channel.html#the-dhcp-enable-command
        """
        return self.api.send_command_with_arguments(
            command="dhcp-enable", service=self.service, arguments={"origin": "user"}
        )

    def list_commands(self) -> KeaResponse:
        """List all commands supported by the server/service

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-list-commands
        """
        return self.api.send_command_with_arguments(
            command="list-commands", service=self.service, arguments={}
        )

    def network6_add(self, shared_networks: List[SharedNetwork6]) -> KeaResponse:
        """Adds new shared networks

        Args:
            shared_networks:        List of Shared Networks to add

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-network6-add
        """
        return self.api.send_command_with_arguments(
            command="network6-add",
            service=self.service,
            arguments={
                "shared-networks": [
                    network.dict(exclude_none=True) for network in shared_networks
                ]
            },
            required_hook="subnet_cmds",
        )

    def network6_del(self, name: str) -> KeaResponse:
        """Deletes an existing shared network

        Args:
            name:       Name of shared network

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network6-del
        """
        return self.api.send_command_with_arguments(
            command="network6-del",
            service=self.service,
            arguments={"name": name},
            required_hook="subnet_cmds",
        )

    def network6_get(self, name: str) -> SharedNetwork6:
        """Returns detailed information about a shared network, including subnets

        Args:
            name:       Name of shared network

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network6-get
        """
        data = self.api.send_command_with_arguments(
            command="network6-get",
            service=self.service,
            arguments={"name": name},
            required_hook="subnet_cmds",
        )

        if data.result == 3:
            raise KeaSharedNetworkNotFoundException(name)

        if not data.arguments["shared-networks"]:
            return None

        shared_network = data.arguments["shared-networks"][0]
        return SharedNetwork6.parse_obj(shared_network)

    def network6_list(self) -> List[SharedNetwork6]:
        """Returns a full list of the current shared networks configured

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network6-list
        """
        data = self.api.send_command(
            command="network6-list",
            service=self.service,
            required_hook="subnet_cmds",
        )

        networks = [
            SharedNetwork6.parse_obj(network)
            for network in data.arguments["shared-networks"]
        ]
        return networks

    def network6_subnet_add(self, name: str, subnet_id: int) -> KeaResponse:
        """Add an existing subnet to an existing shared network

        Args:
            name:       Name of shared network
            subnet_id:  ID of the subnet

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network6-subnet-add
        """
        return self.api.send_command_with_arguments(
            command="network6-subnet-add",
            service=self.service,
            arguments={"name": name, "id": subnet_id},
            required_hook="subnet_cmds",
        )

    def network6_subnet_del(self, name: str, subnet_id: int) -> KeaResponse:
        """Remove a subnet that is part of an existing shared network and demotes it to a plain standalone subnet

        Args:
            name:       Name of shared network
            subnet_id:  ID of the subnet

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network6-subnet-del
        """
        return self.api.send_command_with_arguments(
            command="network6-subnet-del",
            service=self.service,
            arguments={"name": name, "id": subnet_id},
            required_hook="subnet_cmds",
        )

    def shutdown(self) -> KeaResponse:
        """Instructs the server daemon to initiate its shutdown procedure

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-shutdown
        """
        return self.api.send_command_with_arguments(
            command="shutdown", service=self.service, arguments={"exit-value": 3}
        )

    def statistic_get(self, name: str) -> KeaResponse:
        """Returns single statistic

        Args:
            name:       Name of the statistic to get

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-statistic-get
        """
        return self.api.send_command_with_arguments(
            command="statistic-get", service=self.service, arguments={"name": name}
        )

    def statistic_get_all(self) -> KeaResponse:
        """Returns all recorded statistics

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-statistic-get-all
        """
        return self.api.send_command_with_arguments(
            command="statistic-get-all", service=self.service, arguments={}
        )

    def status_get(self) -> StatusGet:
        """Returns servers runtime information

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-status-get
        """
        data = self.api.send_command(command="status-get", service=self.service)
        return StatusGet.parse_obj(data.arguments)

    def subnet6_add(self, subnets: List[Subnet6]) -> KeaResponse:
        """Creates and adds a new subnet

        Args:
            subnets:        List of subnets to add

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet6-add
        """
        return self.api.send_command_with_arguments(
            command="subnet6-add",
            service=self.service,
            arguments={
                "subnet6": [subnet.dict(exclude_none=True) for subnet in subnets]
            },
            required_hook="subnet_cmds",
        )

    def subnet6_del(self, subnet_id: int) -> KeaResponse:
        """Removes a subnet

        Args:
            subnet_id:      ID of the subnet

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet6-del
        """
        data = self.api.send_command_with_arguments(
            command="subnet6-del",
            service=self.service,
            arguments={"id": subnet_id},
            required_hook="subnet_cmds",
        )

        if data.result == 3:
            raise KeaSubnetNotFoundException(subnet_id)

        return data

    def subnet6_delta_add(self) -> None:
        raise NotImplementedError

    def subnet6_delta_del(self) -> None:
        raise NotImplementedError

    def subnet6_get(self, subnet_id: int) -> Subnet6:
        """Gets detailed information about the specified subnet

        Args:
            subnet_id:      ID of the subnet

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet6-get
        """
        data = self.api.send_command_with_arguments(
            command="subnet6-get",
            service=self.service,
            arguments={"id": subnet_id},
            required_hook="subnet_cmds",
        )

        if data.result == 3:
            raise KeaSubnetNotFoundException(subnet_id)

        if not data.arguments["subnet4"]:
            return None

        subnet = data.arguments["subnet4"][0]
        return Subnet6.parse_obj(subnet)

    def subnet6_list(self) -> None:
        raise NotImplementedError

    def subnet6_update(self) -> None:
        raise NotImplementedError

    def version_get(self) -> KeaResponse:
        """Returns extended information about the Kea Version that is running

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-version-get
        """
        return self.api.send_command(command="version-get", service=self.service)
