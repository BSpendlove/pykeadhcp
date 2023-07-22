from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from pykeadhcp import Kea

from pykeadhcp.models.generic import KeaResponse, StatusGet
from pykeadhcp.models.generic.remote_server import RemoteServer
from pykeadhcp.models.generic.option_def import OptionDef
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.models.dhcp4.shared_network import SharedNetwork4
from pykeadhcp.models.dhcp4.subnet import Subnet4
from pykeadhcp.models.dhcp4.lease import Lease4, Lease4Page
from pykeadhcp.models.dhcp4.reservation import Reservation4
from pykeadhcp.models.dhcp4.client_class import ClientClass4
from pykeadhcp.models.enums import HostReservationIdentifierEnum
from pykeadhcp.exceptions import (
    KeaException,
    KeaSharedNetworkNotFoundException,
    KeaSubnetNotFoundException,
    KeaLeaseNotFoundException,
    KeaRemoteServerNotFoundException,
    KeaConfigBackendNotConfiguredException,
    KeaUnknownHostReservationTypeException,
    KeaReservationNotFoundException,
    KeaClientClassNotFoundException,
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

    def get_next_available_subnet_id(self) -> int:
        """Returns the next available subnet-id for use with Dhcp4 subnets"""
        subnets = self.subnet4_list()
        subnet_ids = [subnet.id for subnet in subnets]
        next_id = self.api.get_next_available_subnet_id(subnet_ids=subnet_ids)
        return next_id

    def build_report(self) -> KeaResponse:
        """Returns list of compilation options that this particular binary was built with

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-build-report
        """
        return self.api.send_command(command="build-report", service=self.service)

    def cache_clear(self) -> KeaResponse:
        """Removes all cached host reservations

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#cache-clear
        """
        return self.api.send_command(
            command="cache-clear", service=self.service, required_hook="host_cache"
        )

    def cache_flush(self, number: int) -> KeaResponse:
        """Removes certain number of entries in the host cache

        Args:
            number:     Number of host caches to clear

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#cache-flush
        """
        return self.api.send_command_with_arguments(
            command="cache-flush",
            service=self.service,
            arguments=number,  # Inconsistent API....
            required_hook="host_cache",
        )

    def cache_get(self) -> List[Reservation4]:
        """Gets full content of the host cache

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#cache-get
        """
        data = self.api.send_command(
            command="cache-get", service=self.service, required_hook="host_cache"
        )

        if data.result == 3:
            return []

        return [Reservation4.parse_obj(reservation) for reservation in data.arguments]

    def cache_get_by_id(
        self, identifier_type: HostReservationIdentifierEnum, identifier: str
    ) -> List[Reservation4]:
        """Returns entries matching the given identifier from the host cache

        Args:
            identifier_type:        Type of Identifier
            identifier:             Identifier data

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#cache-get-by-id
        """
        try:
            HostReservationIdentifierEnum(identifier_type)
        except ValueError:
            raise KeaUnknownHostReservationTypeException(identifier_type)

        data = self.api.send_command_with_arguments(
            command="cache-get-by-id",
            service=self.service,
            arguments={identifier_type: identifier},
            required_hook="host_cache",
        )

        if data.result == 3:
            return []

        return [Reservation4.parse_obj(reservation) for reservation in data.arguments]

    def cache_insert(self, subnet_id: int, reservation: Reservation4) -> KeaResponse:
        """Manually insert a host into the cache

        Args:
            reservation:    Reservation4 Object

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#cache-insert
        """
        return self.api.send_command_with_arguments(
            command="cache-insert",
            service=self.service,
            arguments={
                "subnet-id4": subnet_id,
                "subnet-id6": 0,
                **reservation.dict(
                    exclude_none=True, exclude_unset=True, by_alias=True
                ),
            },
            required_hook="host_cache",
        )

    def cache_load(self, filepath: str) -> KeaResponse:
        """Instructs Kea to load from a previously dumped cache into its existing host cache

        Args:
            filepath:   File Path to load

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#cache-load
        """
        return self.api.send_command_with_arguments(
            command="cache-load",
            service=self.service,
            arguments=filepath,  # Inconsistent API....
            required_hook="host_cache",
        )

    def cache_remove(self, subnet_id: int, ip_address: str) -> KeaResponse:
        """Remove an entry from the host cache

        Args:
            subnet_id:      Subnet ID
            ip_address:     IP Address

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#cache-remove
        """
        return self.api.send_command_with_arguments(
            command="cache-remove",
            service=self.service,
            arguments={"ip-address": ip_address, "subnet-id": subnet_id},
            required_hook="host_cache",
        )

    def cache_size(self) -> KeaResponse:
        """Returns the number of entries in the host cache

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#cache-size
        """
        return self.api.send_command(
            command="cache-size", service=self.service, required_hook="host_cache"
        )

    def cache_write(self, filepath: str) -> KeaResponse:
        """Instructs Kea to write host cache content to disk

        Args:
            filepath:   File Path to save

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#cache-write
        """
        return self.api.send_command_with_arguments(
            command="cache-write",
            service=self.service,
            arguments=filepath,  # Inconsistent API....
            required_hook="host_cache",
        )

    def class_add(self, client_class: ClientClass4) -> KeaResponse:
        """Adds a new class to the existing server configuration

        Args:
            client_class:       ClientClass4 Object

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#class-add
        """
        return self.api.send_command_with_arguments(
            command="class-add",
            service=self.service,
            arguments={
                "client-classes": [
                    client_class.dict(
                        exclude_none=True, exclude_unset=True, by_alias=True
                    )
                ]
            },
            required_hook="class_cmds",
        )

    def class_del(self, name: str) -> KeaResponse:
        """Removes a client class from the server configuration

        Args:
            name:   Name of Class

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#class-del
        """
        return self.api.send_command_with_arguments(
            command="class-del",
            service=self.service,
            arguments={"name": name},
            required_hook="class_cmds",
        )

    def class_get(self, name: str) -> ClientClass4:
        """Returns detailed information about an existing client class

        Args:
            name:   Name of Class

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#class-get
        """
        data = self.api.send_command_with_arguments(
            command="class-get",
            service=self.service,
            arguments={"name": name},
            required_hook="class_cmds",
        )

        if data.result == 3:
            raise KeaClientClassNotFoundException(client_class=name)

        if not data.arguments.get("client-classes"):
            return None

        client_class = data.arguments["client-classes"][0]
        return ClientClass4.parse_obj(client_class)

    def class_list(self) -> List[ClientClass4]:
        """Retrieves a list of all client classes from server configuration

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#class-list
        """
        data = self.api.send_command(
            command="class-list", service=self.service, required_hook="class_cmds"
        )

        client_classes = data.arguments.get("client-classes")
        return [ClientClass4.parse_obj(client_class) for client_class in client_classes]

    def class_update(self, client_class: ClientClass4) -> KeaResponse:
        """Updates an existing client class in the server configuration

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#class-update
        """
        return self.api.send_command_with_arguments(
            command="class-update",
            service=self.service,
            arguments={
                "client-classes": [
                    client_class.dict(
                        exclude_none=True, exclude_unset=True, by_alias=True
                    )
                ]
            },
        )

    def config_backend_pull(self) -> KeaResponse:
        """Forces an immediate update of the servers using the configuration database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#config-backend-pull
        """
        data = self.api.send_command(
            command="config-backend-pull", service=self.service
        )

        if data.result == 3:
            raise KeaConfigBackendNotConfiguredException

        return data

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
        """Resumes operation of a paused HA state machine.

        Kea API Reference:
            https://kea.readthedocs.io/en/latest/api.html#ha-continue
        """
        return self.api.send_command(
            command="ha-continue", service=self.service, required_hook="ha"
        )

    def ha_heartbeat(self) -> KeaResponse:
        """Manually verify the HA state of local and remote servers.

        Kea API Reference:
            https://kea.readthedocs.io/en/latest/api.html#ha-heartbeat
        """
        return self.api.send_command(
            command="ha-heartbeat",
            service=self.service,
            required_hook="ha",
        )

    def ha_maintenance_cancel(self) -> KeaResponse:
        """Cancel maintenance via API

        Kea API Reference:
            https://kea.readthedocs.io/en/latest/api.html#ha-maintenance-cancel
        """
        return self.api.send_command(
            command="ha-maintenance-cancel", service=self.service, required_hook="ha"
        )

    def ha_maintenance_notify(self, cancel: bool) -> KeaResponse:
        """Typically used by servers and not an administrator, however this informs the partner HA
        servers to transition to the in-maintenance state or revert from it

        Args:
            cancel:     Indicates server should transition to the in-maintenance state if False

        Kea API Reference:
            https://kea.readthedocs.io/en/latest/api.html#ha-maintenance-notify
        """
        return self.api.send_command_with_arguments(
            command="ha-maintenance-notify",
            service=self.service,
            arguments={"cancel": cancel},
            required_hook="ha",
        )

    def ha_maintenance_start(self) -> KeaResponse:
        """Instruct the server to transition to the 'partner-in-maintenance' state

        Kea API Reference:
            https://kea.readthedocs.io/en/latest/api.html#ha-maintenance-start
        """
        return self.api.send_command(
            command="ha-maintenance-start", service=self.service, required_hook="ha"
        )

    def ha_reset(self) -> KeaResponse:
        """Resets the HA state machine by forcing its state to 'waiting' state

        Kea API Reference:
            https://kea.readthedocs.io/en/latest/api.html#ha-reset
        """
        return self.api.send_command(
            command="ha-reset", service=self.service, required_hook="ha"
        )

    def ha_scopes(self, ha_servers: List[str]) -> KeaResponse:
        """Modifies the scope that the server is responsible for serving

        Args:
            ha_servers:     List of servers (defined in the configuration file)

        Kea API Reference:
            https://kea.readthedocs.io/en/latest/api.html#ha-scopes
        """
        return self.api.send_command_with_arguments(
            command="ha-scopes",
            service=self.service,
            arguments={"scopes": ha_servers},
            required_hook="ha",
        )

    def ha_sync(self, partner_server: str, max_period: int) -> KeaResponse:
        """Instructs the server to sync its local lease database with a selected partner server

        Args:
            partner_server:     Name of the partner server to sync with
            max_period:         Max Period

        Kea API Reference:
            https://kea.readthedocs.io/en/latest/api.html#ha-sync
        """
        return self.api.send_command_with_arguments(
            command="ha-sync",
            service=self.service,
            arguments={"server-name": partner_server, "max-period": max_period},
            required_hook="ha",
        )

    def ha_sync_complete_notify(self) -> KeaResponse:
        """Typically used by the servers directly and not called via the API by an admin

        Kea API Reference:
            https://kea.readthedocs.io/en/latest/api.html#ha-sync-complete-notify
        """
        return self.api.send_command(
            command="ha-sync-complete-notify", service=self.service, required_hook="ha"
        )

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
            arguments=lease.dict(exclude_none=True, exclude_unset=True, by_alias=True),
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
        if subnets:
            data = self.api.send_command_with_arguments(
                command="lease4-get-all",
                service=self.service,
                arguments={"subnets": subnets},
                required_hook="lease_cmds",
            )
        else:
            data = self.api.send_command(
                command="lease4-get-all",
                service=self.service,
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
            arguments=lease.dict(exclude_none=True, exclude_unset=True, by_alias=True),
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
                    network.dict(exclude_none=True, exclude_unset=True, by_alias=True)
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

    def remote_class4_del(self, name: str, remote_map: dict = {}) -> KeaResponse:
        """Deletes a DHCPv4 client class from the configuration database

        Args:
            name:       Name of the client class
            remote_map: (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-class4-del
        """
        return self.api.send_command_remote(
            command="remote-class4-del",
            service=self.service,
            arguments={"client-classes": [{"name": name}]},
            remote_map=remote_map,
        )

    def remote_class4_get(self, name: str, remote_map: dict = {}) -> ClientClass4:
        """Gets a DHCPv4 client class from the configuration database

        Args:
            name:       Name of the client class
            remote_map: (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-class4-get
        """
        data = self.api.send_command_remote(
            command="remote-class4-get",
            service=self.service,
            arguments={"client-classes": [{"name": name}]},
            remote_map=remote_map,
        )

        if data.result == 3:
            raise KeaClientClassNotFoundException(client_class=name)

        if not data.arguments.get("client-classes"):
            return None

        client_class = data.arguments["client-classes"][0]
        return ClientClass4.parse_obj(client_class)

    def remote_class4_get_all(
        self, server_tags: List[str] = ["all"], remote_map: dict = {}
    ) -> ClientClass4:
        """Gets all DHCPv4 client classes from the configuration database

        Args:
            server_tags:    List of Server Tags
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-class4-get-all
        """
        data = self.api.send_command_remote(
            command="remote-class4-get-all",
            service=self.service,
            arguments={"server-tags": server_tags},
            remote_map=remote_map,
        )

        client_classes = data.arguments.get("client-classes")
        return [ClientClass4.parse_obj(client_class) for client_class in client_classes]

    def remote_class4_set(
        self,
        client_class: ClientClass4,
        server_tags: List[str] = ["all"],
        follow_class_name: str = None,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Creates/Replaces a DHCPv4 Client Class in the configuration database

        Args:
            client_class:       ClientClass4 Object
            follow_class_name:  Places client class after existing class in the hierarchy
            remote_map:         (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-class4-set
        """
        data = client_class.dict(exclude_none=True, exclude_unset=True, by_alias=True)
        if follow_class_name:
            data["follow-class-name"] = follow_class_name

        return self.api.send_command_remote(
            command="remote-class4-set",
            service=self.service,
            arguments={"client-classes": [data], "server-tags": server_tags},
            remote_map=remote_map,
        )

    def remote_global_parameter4_del(
        self, parameter: str, server_tag: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes a global DHCPv4 parameter from the configuration database

        Args:
            parameter:      Parameter to delete
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-global-parameter4-del
        """
        return self.api.send_command_remote(
            command="remote-global-parameter4-del",
            service=self.service,
            arguments={"parameters": [parameter], "server-tags": [server_tag]},
            remote_map=remote_map,
        )

    def remote_global_parameter4_get(
        self, parameter: str, server_tag: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Get a specific global parameter from the configuration database

        Args:
            parameter:      Parameter to delete
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-global-parameter4-get
        """
        return self.api.send_command_remote(
            command="remote-global-parameter4-get",
            service=self.service,
            arguments={"parameters": [parameter], "server-tags": [server_tag]},
            remote_map=remote_map,
        )

    def remote_global_parameter4_get_all(
        self, server_tag: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Gets all global parameter from the configuration database

        Args:
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-global-parameter4-get-all
        """
        return self.api.send_command_remote(
            command="remote-global-parameter4-get-all",
            service=self.service,
            arguments={"server-tags": [server_tag]},
            remote_map=remote_map,
        )

    def remote_global_parameter4_set(
        self, parameters: dict, server_tag: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Creates/Updates one or more global parameters in the configuration database

        Args:
            parameters:     Dictionary of parameters (key) and their config (values)
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-global-parameter4-set
        """
        return self.api.send_command_remote(
            command="remote-global-parameter4-set",
            service=self.service,
            arguments={"parameters": parameters, "server-tags": [server_tag]},
            remote_map=remote_map,
        )

    def remote_option_def4_del(
        self,
        option_code: int,
        option_space: str,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Delete a DHCPv4 option defined in the configuration database

        Args:
            option_code:    Option Code
            option_space:   Option Space
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option-def4-del
        """
        return self.api.send_command_remote(
            command="remote-option-def4-del",
            service=self.service,
            arguments={
                "option-defs": [{"code": option_code, "space": option_space}],
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option_def4_get(
        self,
        option_code: int,
        option_space: str,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Delete a DHCPv4 option defined in the configuration database

        Args:
            option_code:    Option Code
            option_space:   Option Space
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option-def4-get
        """
        return self.api.send_command_remote(
            command="remote-option-def4-get",
            service=self.service,
            arguments={
                "option-defs": [{"code": option_code, "space": option_space}],
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option_def4_get_all(self, server_tag: str, remote_map: dict = {}):
        """Fetches all Dhcpv4 option defs from the configuration database

        Args:
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option-def4-get-all
        """
        return self.api.send_command_remote(
            command="remote-option-def4-get-all",
            service=self.service,
            arguments={"server-tags": [server_tag]},
            remote_map=remote_map,
        )

    def remote_option_def4_set(
        self,
        option_def: OptionDef,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Creates/Delete a DHCPv4 option defined in the configuration database

        Args:
            option_def:     OptionDef Object
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option-def4-set
        """
        return self.api.send_command_remote(
            command="remote-option-def4-set",
            service=self.service,
            arguments={
                "option-defs": [
                    option_def.dict(
                        exclude_none=True, exclude_unset=True, by_alias=True
                    )
                ],
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option4_global_del(
        self,
        option_code: int,
        option_space: str,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Delete a DHCPv4 global option defined in the configuration database

        Args:
            option_code:    Option Code
            option_space:   Option Space
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option4-global-del
        """
        return self.api.send_command_remote(
            command="remote-option4-global-del",
            service=self.service,
            arguments={
                "options": [{"code": option_code, "space": option_space}],
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option4_global_get(
        self,
        option_code: int,
        option_space: str,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Gets a DHCPv4 global option defined in the configuration database

        Args:
            option_code:    Option Code
            option_space:   Option Space
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option4-global-get
        """
        return self.api.send_command_remote(
            command="remote-option4-global-get",
            service=self.service,
            arguments={
                "options": [{"code": option_code, "space": option_space}],
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option4_global_get_all(
        self,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Gets all DHCPv4 global option defined in the configuration database

        Args:
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option4-global-get-all
        """
        return self.api.send_command_remote(
            command="remote-option4-global-get-all",
            service=self.service,
            arguments={
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option4_global_set(
        self,
        option_data: OptionData,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Creates/Replaces a DHCPv4 option defined in the configuration database

        Args:
            option_data:    OptionData Object
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option4-global-set
        """
        return self.api.send_command_remote(
            command="remote-option4-global-set",
            service=self.service,
            arguments={
                "options": [
                    option_data.dict(
                        exclude_none=True, exclude_unset=True, by_alias=True
                    )
                ],
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option4_network_del(
        self,
        shared_network: str,
        option_code: int,
        option_space: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Delete a DHCPv4 option from a shared network in the configuration database

        Args:
            shared_network:     Name of shared network
            option_code:        Option Code
            option_space:       Option Space
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option4-network-del
        """
        return self.api.send_command_remote(
            command="remote-option4-network-del",
            service=self.service,
            arguments={
                "shared-networks": [{"name": shared_network}],
                "options": [{"code": option_code, "space": option_space}],
            },
            remote_map=remote_map,
        )

    def remote_option4_network_set(
        self,
        shared_network: str,
        option_data: OptionData,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Delete a DHCPv4 option from a shared network in the configuration database

        Args:
            shared_network:     Name of shared network
            option_data:        OptionData Object
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option4-network-set
        """
        return self.api.send_command_remote(
            command="remote-option4-network-set",
            service=self.service,
            arguments={
                "shared-networks": [{"name": shared_network}],
                "options": [
                    option_data.dict(
                        exclude_none=True, exclude_unset=True, by_alias=True
                    )
                ],
            },
            remote_map=remote_map,
        )

    def remote_option4_pool_del(
        self, pool: str, option_code: int, option_space: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes a DHCPv4 option from an address pool in the configuration database

        Args:
            pool:           Pool Range
            option_code:    Option Code
            option_space:   Option Space
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option4-pool-del
        """
        return self.api.send_command_remote(
            command="remote-option4-pool-del",
            service=self.service,
            arguments={
                "pools": [{"pool": pool}],
                "options": [{"code": option_code, "space": option_space}],
            },
            remote_map=remote_map,
        )

    def remote_option4_pool_set(
        self, pool: str, option_data: OptionData, remote_map: dict = {}
    ) -> KeaResponse:
        """Creates/Replaces a DHCPv4 option in an address pool in the configuration database

        Args:
            pool:           Pool Range
            option_data:    OptionData Object
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option4-pool-set
        """
        return self.api.send_command_remote(
            command="remote-option4-pool-set",
            service=self.service,
            arguments={
                "pools": [{"pool": pool}],
                "options": [
                    option_data.dict(
                        exclude_none=True, exclude_unset=True, by_alias=True
                    )
                ],
            },
            remote_map=remote_map,
        )

    def remote_option4_subnet_del(
        self, subnet_id: int, option_code: int, option_space: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes a DHCPv4 option from a subnet in the configuration database

        Args:
            subnet_id:      Subnet ID
            option_code:    Option Code
            option_space:   Option Space
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option4-subnet-del
        """
        return self.api.send_command_remote(
            command="remote-option4-subnet-del",
            service=self.service,
            arguments={
                "subnets": [{"id": subnet_id}],
                "options": [{"code": option_code, "space": option_space}],
            },
            remote_map=remote_map,
        )

    def remote_option4_subnet_set(
        self, subnet_id: int, option_data: OptionData, remote_map: dict = {}
    ) -> KeaResponse:
        """Creates/Replaces a DHCPv4 option in a subnet in the configuration database

        Args:
            subnet_id:      Subnet ID
            option_data:    OptionData Object
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database
        """
        return self.api.send_command_remote(
            command="remote-option4-subnet-set",
            service=self.service,
            arguments={
                "subnets": [{"id": subnet_id}],
                "options": [
                    option_data.dict(
                        exclude_none=True, exclude_unset=True, by_alias=True
                    )
                ],
            },
            remote_map=remote_map,
        )

    def remote_network4_del(
        self, name: str, keep_subnets: bool = True, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes an existing Shared Network from the configuration database

        Args:
            name:           Name of shared network
            keep_subnets:   Keeps any existing subnets if True
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-network4-del
        """
        return self.api.send_command_remote(
            command="remote-network4-del",
            service=self.service,
            arguments={
                "shared-networks": [{"name": name}],
                "subnets-action": "keep" if keep_subnets else "delete",
            },
            remote_map=remote_map,
        )

    def remote_network4_get(
        self, name: str, include_subnets: bool = True, remote_map: dict = {}
    ) -> SharedNetwork4:
        """Returns detailed information about a shared network, including subnets

        Args:
            name:               Name of shared network
            include_subnets:    Include detailed information about subnets
            remote_map:         (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-network4-get
        """
        data = self.api.send_command_remote(
            command="remote-network4-get",
            service=self.service,
            arguments={
                "shared-networks": [{"name": name}],
                "subnets-include": "full" if include_subnets else "no",
            },
            remote_map=remote_map,
        )

        if data.result == 3:
            raise KeaSharedNetworkNotFoundException(name)

        if not data.arguments["shared-networks"]:
            return None

        shared_network = data.arguments["shared-networks"][0]
        return SharedNetwork4.parse_obj(shared_network)

    def remote_network4_list(
        self, server_tags: List[str], remote_map: dict = {}
    ) -> List[SharedNetwork4]:
        """Gets all shared networks in the configuration database:

        Args:
            server_tags:        List of server tags (at least 1 one must be present)
            remote_map:         (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-network4-list
        """
        data = self.api.send_command_remote(
            command="remote-network4-list",
            service=self.service,
            arguments={"server-tags": server_tags},
            remote_map=remote_map,
        )

        shared_networks = [
            SharedNetwork4.parse_obj(shared_network)
            for shared_network in data.arguments["shared-networks"]
        ]
        return shared_networks

    def remote_network4_set(
        self,
        shared_networks: List[SharedNetwork4],
        server_tags: List[str],
        remote_map: dict = {},
    ) -> KeaResponse:
        """Adds or replaces shared-network configuration in the configuration database

        Args:
            shared_networks:    List of shared networks to add
            server_tags:        List of server tags (at least 1 one must be present)
            remote_map:         (remote_type, remote_host or remote_port) to select a specific remote database
        """

        # Shared networks must not contain subnets in this API call
        for shared_network in shared_networks:
            if shared_network.subnet4:
                raise KeaException(
                    message=f"Shared Network {shared_network.name} contains a list of 1 or more subnets. Please refer to documentation on how to use this command."
                )

        return self.api.send_command_remote(
            command="remote-network4-set",
            service=self.service,
            arguments={
                "shared-networks": [
                    network.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                    for network in shared_networks
                ],
                "server-tags": server_tags,
            },
            remote_map=remote_map,
        )

    def remote_server4_del(self, servers: List[str], remote_map: dict = {}):
        """Delete information about a selected DHCP server from the configuration database

        Args:
            servers:    List of servers to delete
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-server4-del
        """
        servers = [RemoteServer(server_tag=server) for server in servers]

        return self.api.send_command_remote(
            command="remote-server4-del",
            service=self.service,
            arguments={
                "servers": [
                    server.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                ]
                for server in servers
            },
            remote_map=remote_map,
        )

    def remote_server4_get(self, server_tag: str, remote_map: dict = {}):
        """Get information about a specific DHCP server from the configuration database

        Args:
            server_tag:     Server tag to get
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-server4-get

        """
        server = RemoteServer(server_tag=server_tag)
        data = self.api.send_command_remote(
            command="remote-server4-get",
            service=self.service,
            arguments={
                "servers": [
                    server.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                ]
            },
            remote_map=remote_map,
        )

        if data.result == 3:
            raise KeaRemoteServerNotFoundException(server_tag)

        if not data.arguments["servers"]:
            return None

        remote_server = data.arguments["servers"][0]
        return RemoteServer.parse_obj(remote_server)

    def remote_server4_get_all(self, remote_map: dict = {}) -> KeaResponse:
        """Fetches all user-defined DHCPv4 servers from the database

        Args:
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-remote-server4-get-all
        """
        data = self.api.send_command_remote(
            command="remote-server4-get-all",
            service=self.service,
            remote_map=remote_map,
        )

        return [
            RemoteServer.parse_obj(server) for server in data.arguments.get("servers")
        ]

    def remote_server4_set(self, servers: List[RemoteServer], remote_map: dict = {}):
        """Creates or replaces information about a DHCP server in the database

        Args:
            servers:        List of Servers to set
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-server4-set

        """
        return self.api.send_command_remote(
            command="remote-server4-set",
            service=self.service,
            arguments={
                "servers": [
                    server.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                ]
                for server in servers
            },
            remote_map=remote_map,
        )

    def remote_subnet4_del_by_id(
        self, subnet_id: int, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes a subnet from the configuration database

        Args:
            subnet_id:      Subnet ID
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-subnet4-del-by-id
        """
        return self.api.send_command_remote(
            command="remote-subnet4-del-by-id",
            service=self.service,
            arguments={"subnets": [{"id": subnet_id}]},
            remote_map=remote_map,
        )

    def remote_subnet4_del_by_prefix(
        self, prefix: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes a subnet from the configuration database

        Args:
            prefix:         Subnet Prefix
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database
        """
        return self.api.send_command_remote(
            command="remote-subnet4-del-by-prefix",
            service=self.service,
            arguments={"subnets": [{"subnet": prefix}]},
            remote_map=remote_map,
        )

    def remote_subnet4_get_by_id(
        self, subnet_id: int, remote_map: dict = {}
    ) -> Subnet4:
        """Gets a Subnet based on id from the configuration database

        Args:
            subnet_id:      Subnet ID
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-subnet4-get-by-id
        """
        data = self.api.send_command_remote(
            command="remote-subnet4-get-by-id",
            service=self.service,
            arguments={"subnets": [{"id": subnet_id}]},
            remote_map=remote_map,
        )

        if data.result == 3:
            raise KeaSubnetNotFoundException(subnet_id)

        if not data.arguments.get("subnets"):
            return None

        subnet = data.arguments["subnets"][0]
        return Subnet4.parse_obj(subnet)

    def remote_subnet4_get_by_prefix(
        self, prefix: str, remote_map: dict = {}
    ) -> Subnet4:
        """Gets a Subnet based on subnet CIDR from the configuration database

        Args:
            prefix:         Subnet CIDR
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-subnet4-get-by-prefix
        """
        data = self.api.send_command_remote(
            command="remote-subnet4-get-by-prefix",
            service=self.service,
            arguments={"subnets": [{"subnet": prefix}]},
            remote_map=remote_map,
        )

        if data.result == 3:
            raise KeaSubnetNotFoundException(prefix)

        if not data.arguments.get("subnets"):
            return None

        subnet = data.arguments["subnets"][0]
        return Subnet4.parse_obj(subnet)

    def remote_subnet4_list(
        self, server_tags: List[str], remote_map: dict = {}
    ) -> List[Subnet4]:
        """List all currently configured subnets in the configuration database

        Args:
            server_tags:    List of server tags (at least 1 one must be present)
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-subnet4-list
        """
        data = self.api.send_command_remote(
            command="remote-subnet4-list",
            service=self.service,
            arguments={"server-tags": server_tags},
            remote_map=remote_map,
        )

        subnets = [Subnet4.parse_obj(subnet) for subnet in data.arguments["subnets"]]
        return subnets

    def remote_subnet4_set(
        self,
        subnet: Subnet4,
        server_tags: List[str],
        shared_network_name: str = None,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Creates or replaces a subnet in the configuration database

        shared_network:     Name of shared-network (if global subnet, use None)
        subnets:            List of Subnets to configure under shared-network
        server_tags:        List of server tags (at least 1 one must be present)
        remote_map:         (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-subnet4-set

        """
        data = subnet.dict(
            exclude_none=True,
            exclude_unset=True,
            by_alias=True,
        )

        data["shared-network-name"] = shared_network_name

        return self.api.send_command_remote(
            command="remote-subnet4-set",
            service=self.service,
            arguments={
                "subnets": [data],
                "server-tags": server_tags,
            },
            remote_map=remote_map,
        )

    def reservation_add(self, ip_address: str, **kwargs) -> KeaResponse:
        """Creates a new host reservation

        Args:
            reservation:        Reservation Object

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#reservation-add
        """
        reservation = Reservation4(ip_address=ip_address, **kwargs)

        return self.api.send_command_with_arguments(
            command="reservation-add",
            service=self.service,
            arguments={
                "reservation": reservation.dict(
                    exclude_none=True, exclude_unset=True, by_alias=True
                )
            },
            required_hook="host_cmds",
        )

    def reservation_del_by_ip(self, ip_address: str, subnet_id: int) -> KeaResponse:
        """Delete a reservation in the host database based on IP and subnet ID

        Args:
            ip_address:     IP address of the reservation
            subnet_id:      Subnet ID reservation belongs to

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#reservation-del
        """
        return self.api.send_command_with_arguments(
            command="reservation-del",
            service=self.service,
            arguments={"subnet-id": subnet_id, "ip-address": ip_address},
            required_hook="host_cmds",
        )

    def reservation_del_by_identifier(
        self,
        subnet_id: int,
        identifier_type: HostReservationIdentifierEnum,
        identifier: str,
    ) -> KeaResponse:
        """Delete a reservation in the host database based on IP and subnet ID

        Args:
            subnet_id:          Subnet ID reservation belongs to
            identifier_type:    Identifier Type
            identifier:         Identifier Data

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#reservation-del
        """
        try:
            HostReservationIdentifierEnum(identifier_type)
        except ValueError:
            raise KeaUnknownHostReservationTypeException(identifier_type)

        return self.api.send_command_with_arguments(
            command="reservation-del",
            service=self.service,
            arguments={
                "subnet-id": subnet_id,
                "identifier-type": identifier_type,
                "identifier": identifier,
            },
            required_hook="host_cmds",
        )

    def reservation_get_by_ip_address(
        self, subnet_id: int, ip_address: str
    ) -> Reservation4:
        """Gets an existing host reservation

        Args:
            ip_address:     IP address of the reservation
            subnet_id:      Subnet ID reservation belongs to

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#reservation-get
        """

        data = self.api.send_command_with_arguments(
            command="reservation-get",
            service=self.service,
            arguments={"subnet-id": subnet_id, "ip-address": ip_address},
            required_hook="host_cmds",
        )

        if data.result == 3:
            raise KeaReservationNotFoundException(reservation_data=ip_address)

        return Reservation4.parse_obj(data.arguments)

    def reservation_get_by_identifier(
        self,
        subnet_id: int,
        identifier_type: HostReservationIdentifierEnum,
        identifier: str,
    ) -> Reservation4:
        """Gets an existing host reservation

        Args:
            subnet_id:          Subnet ID
            identifier_type:    Identifier Type
            identifier:         Identifier Data

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#reservation-get
        """
        try:
            HostReservationIdentifierEnum(identifier_type)
        except ValueError:
            raise KeaUnknownHostReservationTypeException

        data = self.api.send_command_with_arguments(
            command="reservation-get",
            service=self.service,
            arguments={
                "subnet-id": subnet_id,
                "identifier-type": identifier_type,
                "identifier": identifier,
            },
            required_hook="host_cmds",
        )

        if data.result == 3:
            raise KeaReservationNotFoundException(
                reservation_data=f"({identifier_type}) {identifier}"
            )

        return Reservation4.parse_obj(data.arguments)

    def reservation_get_all(self, subnet_id: int) -> KeaResponse:
        """Gets all host reservations for a given subnet id

        Args:
            subnet_id:      Subnet ID

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#reservation-get-all
        """
        reservations = self.api.send_command_with_arguments(
            command="reservation-get-all",
            service=self.service,
            arguments={"subnet-id": subnet_id},
            required_hook="host_cmds",
        )

        return [
            Reservation4.parse_obj(reservation)
            for reservation in reservations.arguments.get("hosts")
        ]

    def reservation_get_by_hostname(
        self, hostname: str, subnet_id: int
    ) -> Reservation4:
        """Gets a reservation based on a hostname

        Args:
            hostname:       Reservation Hostname
            subnet_id:      Subnet ID

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#reservation-get-by-hostname
        """
        data = self.api.send_command_with_arguments(
            command="reservation-get-by-hostname",
            service=self.service,
            arguments={"hostname": hostname, "subnet-id": subnet_id},
            required_hook="host_cmds",
        )

        if data.result == 3:
            raise KeaReservationNotFoundException(
                reservation_data=f"(hostname) {hostname}"
            )

        if not data.arguments.get("hosts"):
            return None

        return Reservation4.parse_obj(data.arguments["hosts"][0])

    def reservation_get_page(
        self,
        subnet_id: int = None,
        limit: int = 1000,
        source_index: int = 0,
        from_host_id: int = 0,
    ) -> List[Reservation4]:
        """Gathers all host reservations with paging functionality

        Args:
            subnet_id:      Subnet ID to filter if provided
            limit:          Limit reservations to return
            source_index:   Refer to https://kea.readthedocs.io/en/kea-2.2.0/arm/hooks.html#command-reservation-get-page
            from_host_id:   Refer to https://kea.readthedocs.io/en/kea-2.2.0/arm/hooks.html#command-reservation-get-page

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#reservation-get-page
        """
        params = {"limit": limit, "source-index": source_index, "from": from_host_id}

        if subnet_id:
            params["subnet-id"] = subnet_id

        data = self.api.send_command_with_arguments(
            command="reservation-get-page",
            service=self.service,
            arguments=params,
            required_hook="host_cmds",
        )

        if data.result == 1:
            raise KeaException(message=data.text)

        if not data.arguments or not data.arguments.get("hosts"):
            return None

        return [
            Reservation4.parse_obj(reservation)
            for reservation in data.arguments["hosts"]
        ]

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
                    subnet.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                    for subnet in subnets
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
                    subnet.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                    for subnet in subnets
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
                    subnet.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                    for subnet in subnets
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
                    subnet.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                    for subnet in subnets
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
