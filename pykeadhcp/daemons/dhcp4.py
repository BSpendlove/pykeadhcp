from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from pykeadhcp import Kea


class Dhcp4:
    def __init__(self, api: "Kea"):
        self.service = "dhcp4"
        self.api = api

    def build_report(self) -> dict:
        """Returns list of compilation options that this particular binary was built with

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-build-report
        """
        return self.api.send_command(command="build-report", service=self.service)

    def config_get(self) -> dict:
        """Retrieves the current configuration used by the server

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-config-get
        """
        return self.api.send_command(command="config-get", service=self.service)

    def config_reload(self) -> dict:
        """Reloads the last good configuration (configuration file on disk)

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-config-reload
        """
        return self.api.send_command(command="config-reload", service=self.service)

    def config_set(self, config: dict) -> dict:
        """Replace the current server configuration with the provided configuration

        Args:
            config:     Configuration to set

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#config-set
        """
        return self.api.send_command_with_arguments(
            command="config-set", service=self.service, arguments=config
        )

    def config_test(self, config: dict) -> dict:
        """Check whether the configuration supplied can be loaded by the dhcp4 daemon

        Args:
            config:     Configuration to test

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#config-test
        """
        return self.api.send_command_with_arguments(
            command="config-test", service=self.service, arguments=config
        )

    def config_write(self, filename: str) -> dict:
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

    def dhcp_disable(self, max_period: int = 20) -> dict:
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

    def dhcp_enable(self) -> dict:
        """Globally enables the DHCP service (dhcp4)

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/arm/ctrl-channel.html#the-dhcp-enable-command
        """
        return self.api.send_command_with_arguments(
            command="dhcp-enable", service=self.service, arguments={"origin": "user"}
        )

    def ha_continue(self) -> dict:
        pass

    def ha_heartbeat(self) -> dict:
        pass

    def ha_maintenance_canel(self) -> dict:
        pass

    def ha_maintenance_notify(self) -> dict:
        pass

    def ha_maintenance_start(self) -> dict:
        pass

    def ha_reset(self) -> dict:
        pass

    def ha_scopes(self) -> dict:
        pass

    def ha_sync(self) -> dict:
        pass

    def ha_sync_complete_notify(self) -> dict:
        pass

    def lease4_add(
        self,
        *,
        ip_address: str,
        identifier_key: str = "hw-address",
        identifier_value: str
    ) -> dict:
        """Administratively add a new IPv4 lease

        Args:
            ip_address:         IPv4 Address of lease
            identifier_key:     Supported identifier (hw-address, flex-id, etc...)
            identifier_value:   Value of key (eg. flex-id data or hw-address MAC address)

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-add
        """
        return self.api.send_command_with_arguments(
            command="lease4-add",
            service=self.service,
            arguments={"ip-address": ip_address, identifier_key: identifier_value},
        )

    def lease4_del(self, ip_address: str) -> dict:
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
        )

    def lease4_get(self, ip_address: str) -> dict:
        """Queries the lease database and retrieves existing lease

        Args:
            ip_address:     IP address of lease

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get
        """
        return self.api.send_command_with_arguments(
            command="lease4-get",
            service=self.service,
            arguments={"ip-address": ip_address},
        )

    def lease4_get_all(self, subnets: List[int] = []) -> dict:
        """Retrieves all IPv4 leases or all leases for the specified subnets

        Args:
            subnets:        List of subnet IDs to fetch leases for

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get-all
        """
        return self.api.send_command_with_arguments(
            command="lease4-get-all",
            service=self.service,
            arguments={"subnets": subnets},
        )

    def lease4_get_by_client_id(self, client_id: str) -> dict:
        """Retrieves all IPv4 leases for the specified client id

        Args:
            client_id:      Client ID

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get-by-client-id
        """
        return self.api.send_command_with_arguments(
            command="lease4-get-by-client-id",
            service=self.service,
            arguments={"client-id": client_id},
        )

    def lease4_get_by_hostname(self, hostname: str) -> dict:
        """Retrieves all IPv4 leases for the specified hostname

        Args:
            hostname:   Hostname

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get-by-hostname
        """
        return self.api.send_command_with_arguments(
            command="lease4-get-by-hostname",
            service=self.service,
            arguments={"hostname": hostname},
        )

    def lease4_get_by_hw_address(self, hw_address: str) -> dict:
        """Retrieves all IPv4 leases for the specified hardware address

        Args:
            hw_address:     Hardware Address

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get-by-hw-address
        """
        return self.api.send_command_with_arguments(
            command="lease4-get-by-hw-address",
            service=self.service,
            arguments={"hw-address": hw_address},
        )

    def lease4_get_page(self, limit: int, search_from: str) -> dict:
        """Retrieves all IPv4 leases by page

        Args:
            limit:          Set the limit of IPv4 leases to be returned
            search_from:    Start from either a specific IP address or 'start' for the first

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get-page
        """
        return self.api.send_command_with_arguments(
            command="lease4-get-page",
            service=self.service,
            arguments={"from": search_from, "limit": limit},
        )

    def lease4_resend_ddns(self, ip_address: str) -> dict:
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
        )

    def lease4_update(
        self,
        ip_address: str,
        hostname: str = "",
        hw_address: str = "",
        subnet_id: int = None,
        force_create: bool = None,
    ) -> dict:
        """Updates an existing lease

        Args:
            ip_address:     Lease IPv4 Address
            hostname:       Hostname of lease
            hw_address:     Ethernet MAC address
            subnet_id:      ID of the subnet
            force_create:   Creates the lease if it doesn't exist

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-update
        """
        payload = {"ip-address": ip_address}
        if hostname:
            payload["hostname"] = hostname
        if hw_address:
            payload["hw-address"] = hw_address
        if subnet_id:
            payload["subnet-id"] = subnet_id
        if force_create:
            payload["force-create"] = force_create

        return self.api.send_command_with_arguments(
            command="lease4-update", service=self.service, arguments=payload
        )

    def lease4_wipe(self, subnet_id: int) -> dict:
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
        )

    def leases_reclaim(self) -> dict:
        """Instructs the dhcp4 daemon to reclaim all expired leases

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-leases-reclaim
        """
        return self.api.send_command_with_arguments(
            command="leases-reclaim", service=self.service, arguments={"remove": True}
        )

    def libreload(self) -> dict:
        """Unloads and then reloads all currently loaded hook libraries

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#libreload
        """
        return self.api.send_command_with_arguments(
            command="libreload", service=self.service, arguments={}
        )

    def list_commands(self) -> dict:
        """List all commands supported by the server/service

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-list-commands
        """
        return self.api.send_command_with_arguments(
            command="list-commands", service=self.service, arguments={}
        )

    def network4_add(self, shared_networks: List[Dict]) -> dict:
        """Adds a new shared network

        Args:
            shared_networks:        List of shared networks to add

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-network4-add
        """
        return self.api.send_command_with_arguments(
            command="network4-add",
            service=self.service,
            arguments={"shared-networks": shared_networks},
        )

    def network4_del(self, name: str) -> dict:
        """Deletes an existing shared network

        Args:
            name:       Name of shared network

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network4-del
        """
        return self.api.send_command_with_arguments(
            command="network4-del", service=self.service, arguments={"name": name}
        )

    def network4_get(self, name: str) -> dict:
        """Returns detailed information about a shared network, including subnets

        Args:
            name:       Name of shared network

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network4-get
        """
        return self.api.send_command_with_arguments(
            command="network4-get", service=self.service, arguments={"name": name}
        )

    def network4_list(self) -> dict:
        """Returns a full list of the current shared networks configured

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#network4-list
        """
        return self.api.send_command(command="network4-list", service=self.service)

    def network4_subnet_add(self, name: str, subnet_id: int) -> dict:
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
        )

    def network4_subnet_del(self, name: str, subnet_id: int) -> dict:
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
        )

    def reservation_add(self) -> dict:
        pass

    def reservation_del(self) -> dict:
        pass

    def reservation_get(self) -> dict:
        pass

    def reservation_get_all(self) -> dict:
        pass

    def reservation_get_by_hostname(self) -> dict:
        pass

    def reservation_get_by_id(self) -> dict:
        pass

    def reservation_get_page(self) -> dict:
        pass

    def server_tag_get(self) -> dict:
        pass

    def shutdown(self) -> dict:
        """Instructs the server daemon to initiate its shutdown procedure

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-shutdown
        """
        return self.api.send_command_with_arguments(
            command="shutdown", service=self.service, arguments={"exit-value": 3}
        )

    def stat_lease4_get(self) -> dict:
        pass

    def statistic_get(self, name: str) -> dict:
        """Returns single statistic

        Args:
            name:       Name of the statistic to get

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-statistic-get
        """
        return self.api.send_command_with_arguments(
            command="statistic-get", service=self.service, arguments={"name": name}
        )

    def statistic_get_all(self) -> dict:
        """Returns all recorded statistics

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-statistic-get-all
        """
        return self.api.send_command_with_arguments(
            command="statistic-get-all", service=self.service, arguments={}
        )

    def statistic_remove(self) -> dict:
        pass

    def statistic_remove_all(self) -> dict:
        pass

    def statistic_reset(self) -> dict:
        pass

    def statistic_reset_all(self) -> dict:
        pass

    def statistic_sample_age_set(self) -> dict:
        pass

    def statistic_sample_age_set_all(self) -> dict:
        pass

    def statistic_sample_count_set(self) -> dict:
        pass

    def statistic_sample_count_set_all(self) -> dict:
        pass

    def status_get(self) -> dict:
        """Returns servers runtime information

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-status-get
        """
        return self.api.send_command(command="status-get", service=self.service)

    def subnet4_add(self, subnets: List[Dict]) -> dict:
        """Creates and adds a new subnet

        Args:
            subnets:        List of subnets to add

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-subnet4-add
        """
        return self.api.send_command_with_arguments(
            command="subnet4-add", service=self.service, arguments={"subnet4": subnets}
        )

    def subnet4_del(self, subnet_id: int) -> dict:
        """Removes a subnet

        Args:
            subnet_id:      ID of the subnet

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-del
        """
        return self.api.send_command_with_arguments(
            command="subnet4-del", service=self.service, arguments={"id": subnet_id}
        )

    def subnet4_delta_add(self, subnets: List[Dict]) -> dict:
        """Updates (adds or overwrites) parts of a single subnet

        Args:
            subnets:        List of subnets to update/add

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-delta-add
        """
        return self.api.send_command_with_arguments(
            command="subnet4-delta-add",
            service=self.service,
            arguments={"subnet4": subnets},
        )

    def subnet4_delta_del(self, subnets: List[Dict]) -> dict:
        """Updates (removes) parts of a single subnet

        Args:
            subnets:        List of subnets to update/delete

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-delta-del
        """
        return self.api.send_command_with_arguments(
            command="subnet4-delta-del",
            service=self.service,
            arguments={"subnet4": subnets},
        )

    def subnet4_get(self, subnet_id: int) -> dict:
        """Gets detailed information about the specified subnet

        Args:
            subnet_id:      ID of the subnet

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-get
        """
        return self.api.send_command_with_arguments(
            command="subnet4-get", service=self.service, arguments={"id": subnet_id}
        )

    def subnet4_list(self) -> dict:
        """List all currently configured subnets

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-list
        """
        return self.api.send_command(command="subnet4-list", service=self.service)

    def subnet4_update(self, subnets: List[Dict]) -> dict:
        """Updates (overwrites) a single subnet

        Args:
            subnets:        List of subnets to overwrite

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet4-update
        """
        return self.api.send_command_with_arguments(
            command="subnet4-update",
            service=self.service,
            arguments={"subnet4": subnets},
        )

    def version_get(self) -> dict:
        """Returns extended information about the Kea Version that is running

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-version-get
        """
        return self.api.send_command(command="version-get", service=self.service)
