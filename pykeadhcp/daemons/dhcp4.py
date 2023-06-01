from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from pykeadhcp import Kea

from pykeadhcp.models.generic import KeaResponse, StatusGet
from pykeadhcp.models.dhcp4.shared_network import SharedNetwork4
from pykeadhcp.models.dhcp4.subnet import Subnet4
from pykeadhcp.models.dhcp4.lease import Lease4, Lease4Page
from pykeadhcp.exceptions import (
    KeaSharedNetworkNotFoundException,
    KeaSubnetNotFoundException,
    KeaLeaseNotFoundException,
)


class Dhcp4:
    def __init__(self, api: "Kea"):
        self.service = "dhcp4"
        self.api = api

        # Cache config and hooks
        try:
            self.cached_config = None
            self.refresh_cached_config()
            self.hook_libraries = self.api.get_active_hooks(
                hooks=self.cached_config[self.service.capitalize()]["hooks-libraries"]
            )
            self.api.hook_library[self.service] = self.hook_libraries
        except:
            pass

    def refresh_cached_config(self):
        """Sets the cached_config variable

        This function should be called after any interaction with the API that potentially changes the configuration
        eg. subnet4-add, commands like lease4-add won't need a config refresh to keep the cached config up to date
        """
        config = self.config_get()
        self.cached_config = config.arguments

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

    def ha_continue(self) -> KeaResponse:
        raise NotImplementedError

    def ha_heartbeat(self) -> KeaResponse:
        raise NotImplementedError

    def ha_maintenance_canel(self) -> KeaResponse:
        raise NotImplementedError

    def ha_maintenance_notify(self) -> KeaResponse:
        raise NotImplementedError

    def ha_maintenance_start(self) -> KeaResponse:
        raise NotImplementedError

    def ha_reset(self) -> KeaResponse:
        raise NotImplementedError

    def ha_scopes(self) -> KeaResponse:
        raise NotImplementedError

    def ha_sync(self) -> KeaResponse:
        raise NotImplementedError

    def ha_sync_complete_notify(self) -> KeaResponse:
        raise NotImplementedError

    def lease4_add(
        self,
        *,
        ip_address: str,
        **kwargs,
    ) -> KeaResponse:
        """Administratively add a new IPv4 lease

        Args:
            ip_address:         IPv4 Address of lease

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-add
        """
        lease = Lease4(ip_address=ip_address, **kwargs)
        return self.api.send_command_with_arguments(
            command="lease4-add",
            service=self.service,
            arguments=lease.dict(exclude_none=True, by_alias=True),
            required_hook="lease_cmds",
        )

    def lease4_del(self, ip_address: str) -> KeaResponse:
        """Deletes a lease from the lease database

        Args:
            ip_address:     IP address of lease to delete

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-del
        """
        return self.api.send_command_with_arguments(
            command="lease4-del",
            service=self.service,
            arguments={"ip-address": ip_address},
            required_hook="lease_cmds",
        )

    def lease4_get(self, ip_address: str) -> Lease4:
        """Queries the lease database and retrieves existing lease

        Args:
            ip_address:     IP address of lease

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get
        """
        data = self.api.send_command_with_arguments(
            command="lease4-get",
            service=self.service,
            arguments={"ip-address": ip_address},
            required_hook="lease_cmds",
        )

        if data.result == 3:
            raise KeaLeaseNotFoundException(ip_address)

        return Lease4.parse_obj(data.arguments)

    def lease4_get_all(self, subnets: List[int] = []) -> List[Lease4]:
        """Retrieves all IPv4 leases or all leases for the specified subnets

        Args:
            subnets:        List of subnet IDs to fetch leases for

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get-all
        """
        data = self.api.send_command_with_arguments(
            command="lease4-get-all",
            service=self.service,
            arguments={"subnets": subnets},
            required_hook="lease_cmds",
        )

        if data.result == 3:
            raise KeaLeaseNotFoundException(data.text)

        leases = [Lease4.parse_obj(lease) for lease in data.arguments["leases"]]
        return leases

    def lease4_get_by_client_id(self, client_id: str) -> Lease4:
        """Retrieves all IPv4 leases for the specified client id

        Args:
            client_id:      Client ID

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get-by-client-id
        """
        data = self.api.send_command_with_arguments(
            command="lease4-get-by-client-id",
            service=self.service,
            arguments={"client-id": client_id},
            required_hook="lease_cmds",
        )

        if data.result == 3:
            raise KeaLeaseNotFoundException(
                f"Unable to find a lease using client-id '{client_id}'"
            )

        return Lease4.parse_obj(data.arguments)

    def lease4_get_by_hostname(self, hostname: str) -> KeaResponse:
        """Retrieves all IPv4 leases for the specified hostname

        Args:
            hostname:   Hostname

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get-by-hostname
        """
        data = self.api.send_command_with_arguments(
            command="lease4-get-by-hostname",
            service=self.service,
            arguments={"hostname": hostname},
            required_hook="lease_cmds",
        )

        if data.result == 3:
            raise KeaLeaseNotFoundException(
                f"Unable to find lease using hostname '{hostname}'"
            )

        return Lease4.parse_obj(data.arguments)

    def lease4_get_by_hw_address(self, hw_address: str) -> Lease4:
        """Retrieves all IPv4 leases for the specified hardware address

        Args:
            hw_address:     Hardware Address

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get-by-hw-address
        """
        data = self.api.send_command_with_arguments(
            command="lease4-get-by-hw-address",
            service=self.service,
            arguments={"hw-address": hw_address},
            required_hook="lease_cmds",
        )

        if data.result == 3:
            raise KeaLeaseNotFoundException(
                f"Unable to find lease using hw-address '{hw_address}'"
            )

        lease = data.arguments["leases"][0]
        return Lease4.parse_obj(lease)

    def lease4_get_page(self, limit: int, search_from: str) -> Lease4Page:
        """Retrieves all IPv4 leases by page

        Args:
            limit:          Set the limit of IPv4 leases to be returned
            search_from:    Start from either a specific IP address or 'start' for the first

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get-page
        """
        data = self.api.send_command_with_arguments(
            command="lease4-get-page",
            service=self.service,
            arguments={"from": search_from, "limit": limit},
            required_hook="lease_cmds",
        )

        return Lease4Page.parse_obj(data.arguments)

    def lease4_resend_ddns(self, ip_address: str) -> KeaResponse:
        """Sends an internal request to the ddns daemon to update DNS for an existing lease

        Args:
            ip_address:     Lease to update DDNS record

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-resend-ddns
        """
        return self.api.send_command_with_arguments(
            command="lease4-resend-ddns",
            service=self.service,
            arguments={"ip-address": ip_address},
            required_hook="lease_cmds",
        )

    def lease4_update(self, ip_address: str, **kwargs) -> KeaResponse:
        """Updates an existing lease

        Args:
            ip_address:     Lease IPv4 Address

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-update
        """
        lease = Lease4(ip_address=ip_address, **kwargs)
        return self.api.send_command_with_arguments(
            command="lease4-update",
            service=self.service,
            arguments=lease.dict(exclude_none=True, by_alias=True),
            required_hook="lease_cmds",
        )

    def lease4_wipe(self, subnet_id: int) -> KeaResponse:
        """Removes all leases assosicated to the specified subnet id

        Args:
            subnet_id:      ID of the subnet

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-wipe
        """
        return self.api.send_command_with_arguments(
            command="lease4-wipe",
            service=self.service,
            arguments={"subnet-id": subnet_id},
            required_hook="lease_cmds",
        )

    def leases_reclaim(self) -> KeaResponse:
        """Instructs the dhcp4 daemon to reclaim all expired leases

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-leases-reclaim
        """
        return self.api.send_command_with_arguments(
            command="leases-reclaim",
            service=self.service,
            arguments={"remove": True},
            required_hook="lease_cmds",
        )

    def libreload(self) -> KeaResponse:
        """Unloads and then reloads all currently loaded hook libraries

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#libreload
        """
        return self.api.send_command_with_arguments(
            command="libreload", service=self.service, arguments={}
        )

    def list_commands(self) -> KeaResponse:
        """List all commands supported by the server/service

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-list-commands
        """
        return self.api.send_command_with_arguments(
            command="list-commands", service=self.service, arguments={}
        )

    def network4_add(self, shared_networks: List[SharedNetwork4]) -> KeaResponse:
        """Adds a new shared network

        Args:
            shared_networks:        List of shared networks to add

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-network4-add
        """
        return self.api.send_command_with_arguments(
            command="network4-add",
            service=self.service,
            arguments={
                "shared-networks": [
                    network.dict(exclude_none=True, by_alias=True)
                    for network in shared_networks
                ]
            },
            required_hook="subnet_cmds",
        )

    def network4_del(self, name: str) -> KeaResponse:
        """Deletes an existing shared network

        Args:
            name:       Name of shared network

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network4-del
        """
        return self.api.send_command_with_arguments(
            command="network4-del",
            service=self.service,
            arguments={"name": name},
            required_hook="subnet_cmds",
        )

    def network4_get(self, name: str) -> SharedNetwork4:
        """Returns detailed information about a shared network, including subnets

        Args:
            name:       Name of shared network

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network4-get
        """
        data = self.api.send_command_with_arguments(
            command="network4-get",
            service=self.service,
            arguments={"name": name},
            required_hook="subnet_cmds",
        )

        if data.result == 3:
            raise KeaSharedNetworkNotFoundException(name)

        if not data.arguments["shared-networks"]:
            return None

        shared_network = data.arguments["shared-networks"][0]
        return SharedNetwork4.parse_obj(shared_network)

    def network4_list(self) -> List[SharedNetwork4]:
        """Returns a full list of the current shared networks configured

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network4-list
        """
        data = self.api.send_command(
            command="network4-list",
            service=self.service,
            required_hook="subnet_cmds",
        )

        networks = [
            SharedNetwork4.parse_obj(network)
            for network in data.arguments["shared-networks"]
        ]
        return networks

    def network4_subnet_add(self, name: str, subnet_id: int) -> KeaResponse:
        """Add an existing subnet to an existing shared network

        Args:
            name:       Name of shared network
            subnet_id:  ID of the subnet

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network4-subnet-add
        """
        return self.api.send_command_with_arguments(
            command="network4-subnet-add",
            service=self.service,
            arguments={"name": name, "id": subnet_id},
            required_hook="subnet_cmds",
        )

    def network4_subnet_del(self, name: str, subnet_id: int) -> KeaResponse:
        """Remove a subnet that is part of an existing shared network and demotes it to a plain standalone subnet

        Args:
            name:       Name of shared network
            subnet_id:  ID of the subnet

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network4-subnet-del
        """
        return self.api.send_command_with_arguments(
            command="network4-subnet-del",
            service=self.service,
            arguments={"name": name, "id": subnet_id},
            required_hook="subnet_cmds",
        )

    def reservation_add(self) -> KeaResponse:
        raise NotImplementedError

    def reservation_del(self) -> KeaResponse:
        raise NotImplementedError

    def reservation_get(self) -> KeaResponse:
        raise NotImplementedError

    def reservation_get_all(self) -> KeaResponse:
        raise NotImplementedError

    def reservation_get_by_hostname(self) -> KeaResponse:
        raise NotImplementedError

    def reservation_get_by_id(self) -> KeaResponse:
        raise NotImplementedError

    def reservation_get_page(self) -> KeaResponse:
        raise NotImplementedError

    def server_tag_get(self) -> KeaResponse:
        pass

    def shutdown(self) -> KeaResponse:
        """Instructs the server daemon to initiate its shutdown procedure

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-shutdown
        """
        return self.api.send_command_with_arguments(
            command="shutdown", service=self.service, arguments={"exit-value": 3}
        )

    def stat_lease4_get(self) -> KeaResponse:
        pass

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

    def statistic_remove(self) -> KeaResponse:
        raise NotImplementedError

    def statistic_remove_all(self) -> KeaResponse:
        raise NotImplementedError

    def statistic_reset(self) -> KeaResponse:
        raise NotImplementedError

    def statistic_reset_all(self) -> KeaResponse:
        raise NotImplementedError

    def statistic_sample_age_set(self) -> KeaResponse:
        raise NotImplementedError

    def statistic_sample_age_set_all(self) -> KeaResponse:
        raise NotImplementedError

    def statistic_sample_count_set(self) -> KeaResponse:
        raise NotImplementedError

    def statistic_sample_count_set_all(self) -> KeaResponse:
        raise NotImplementedError

    def status_get(self) -> StatusGet:
        """Returns servers runtime information

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-status-get
        """
        data = self.api.send_command(command="status-get", service=self.service)
        return StatusGet.parse_obj(data.arguments)

    def subnet4_add(self, subnets: List[Subnet4]) -> KeaResponse:
        """Creates and adds a new subnet

        Args:
            subnets:        List of subnets to add

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-subnet4-add
        """
        return self.api.send_command_with_arguments(
            command="subnet4-add",
            service=self.service,
            arguments={
                "subnet4": [
                    subnet.dict(exclude_none=True, by_alias=True) for subnet in subnets
                ]
            },
            required_hook="subnet_cmds",
        )

    def subnet4_del(self, subnet_id: int) -> KeaResponse:
        """Removes a subnet

        Args:
            subnet_id:      ID of the subnet

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-del
        """
        data = self.api.send_command_with_arguments(
            command="subnet4-del",
            service=self.service,
            arguments={"id": subnet_id},
            required_hook="subnet_cmds",
        )

        if data.result == 3:
            raise KeaSubnetNotFoundException(subnet_id)

        return data

    def subnet4_delta_add(self, subnets: List[Subnet4]) -> KeaResponse:
        """Updates (adds or overwrites) parts of a single subnet

        Args:
            subnets:        List of subnets to update/add

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-delta-add
        """
        return self.api.send_command_with_arguments(
            command="subnet4-delta-add",
            service=self.service,
            arguments={
                "subnet4": [
                    subnet.dict(exclude_none=True, by_alias=True) for subnet in subnets
                ]
            },
            required_hook="subnet_cmds",
        )

    def subnet4_delta_del(self, subnets: List[Subnet4]) -> KeaResponse:
        """Updates (removes) parts of a single subnet

        Args:
            subnets:        List of subnets to update/delete

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-delta-del
        """
        return self.api.send_command_with_arguments(
            command="subnet4-delta-del",
            service=self.service,
            arguments={
                "subnet4": [
                    subnet.dict(exclude_none=True, by_alias=True) for subnet in subnets
                ]
            },
            required_hook="subnet_cmds",
        )

    def subnet4_get(self, subnet_id: int) -> Subnet4:
        """Gets detailed information about the specified subnet

        Args:
            subnet_id:      ID of the subnet

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-get
        """
        data = self.api.send_command_with_arguments(
            command="subnet4-get",
            service=self.service,
            arguments={"id": subnet_id},
            required_hook="subnet_cmds",
        )

        if data.result == 3:
            raise KeaSubnetNotFoundException(subnet_id)

        if not data.arguments["subnet4"]:
            return None

        subnet = data.arguments["subnet4"][0]
        return Subnet4.parse_obj(subnet)

    def subnet4_list(self) -> List[Subnet4]:
        """List all currently configured subnets

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-list
        """
        data = self.api.send_command(
            command="subnet4-list",
            service=self.service,
            required_hook="subnet_cmds",
        )

        subnets = [Subnet4.parse_obj(subnet) for subnet in data.arguments["subnets"]]
        return subnets

    def subnet4_update(self, subnets: List[Subnet4]) -> List[Subnet4]:
        """Updates (overwrites) a single subnet

        Args:
            subnets:        List of subnets to overwrite

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-update
        """
        return self.api.send_command_with_arguments(
            command="subnet4-update",
            service=self.service,
            arguments={
                "subnet4": [
                    subnet.dict(exclude_none=True, by_alias=True) for subnet in subnets
                ]
            },
            required_hook="subnet_cmds",
        )

    def version_get(self) -> KeaResponse:
        """Returns extended information about the Kea Version that is running

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-version-get
        """
        return self.api.send_command(command="version-get", service=self.service)
