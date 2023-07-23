from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from pykeadhcp import Kea

from pykeadhcp.models.generic import KeaResponse, StatusGet
from pykeadhcp.models.generic.remote_server import RemoteServer
from pykeadhcp.models.generic.option_def import OptionDef
from pykeadhcp.models.generic.option_data import OptionData
from pykeadhcp.models.dhcp6.lease import Lease6, Lease6Page, Lease6TypeEnum
from pykeadhcp.models.dhcp6.pd_pool import PDPool
from pykeadhcp.models.dhcp6.reservation import Reservation6
from pykeadhcp.models.dhcp6.shared_network import SharedNetwork6
from pykeadhcp.models.dhcp6.subnet import Subnet6
from pykeadhcp.models.dhcp6.client_class import ClientClass6
from pykeadhcp.models.enums import HostReservationIdentifierEnum
from pykeadhcp.exceptions import (
    KeaException,
    KeaSharedNetworkNotFoundException,
    KeaSubnetNotFoundException,
    KeaLeaseNotFoundException,
    KeaConfigBackendNotConfiguredException,
    KeaRemoteServerNotFoundException,
    KeaUnknownHostReservationTypeException,
    KeaReservationNotFoundException,
    KeaClientClassNotFoundException,
)


class Dhcp6:
    def __init__(self, api: "Kea"):
        self.service = "dhcp6"
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
        eg. subnet6-add, commands like lease6-add won't need a config refresh to keep the cached config up to date
        """
        config = self.config_get()
        self.cached_config = config.arguments

    def get_next_available_subnet_id(self) -> int:
        """Returns the next available subnet-id for use with Dhcp4 subnets"""
        subnets = self.subnet6_list()
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

    def cache_get(self) -> List[Reservation6]:
        """Gets full content of the host cache

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#cache-get
        """
        data = self.api.send_command(
            command="cache-get", service=self.service, required_hook="host_cache"
        )

        if data.result == 3:
            return []

        return [Reservation6.parse_obj(reservation) for reservation in data.arguments]

    def cache_get_by_id(
        self, identifier_type: HostReservationIdentifierEnum, identifier: str
    ) -> List[Reservation6]:
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

        return [Reservation6.parse_obj(reservation) for reservation in data.arguments]

    def cache_insert(self, subnet_id: int, reservation: Reservation6) -> KeaResponse:
        """Manually insert a host into the cache

        Args:
            reservation:    Reservation6 Object

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#cache-insert
        """
        return self.api.send_command_with_arguments(
            command="cache-insert",
            service=self.service,
            arguments={
                "subnet-id4": 0,
                "subnet-id6": subnet_id,
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

    def class_add(self, client_class: ClientClass6) -> KeaResponse:
        """Adds a new class to the existing server configuration

        Args:
            client_class:       ClientClass6 Object

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

    def class_get(self, name: str) -> ClientClass6:
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
        return ClientClass6.parse_obj(client_class)

    def class_list(self) -> List[ClientClass6]:
        """Retrieves a list of all client classes from server configuration

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#class-list
        """
        data = self.api.send_command(
            command="class-list", service=self.service, required_hook="class_cmds"
        )

        client_classes = data.arguments.get("client-classes")
        return [ClientClass6.parse_obj(client_class) for client_class in client_classes]

    def class_update(self, client_class: ClientClass6) -> KeaResponse:
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

    def lease6_add(
        self, *, ip_address: str, duid: str, iaid: int, **kwargs
    ) -> KeaResponse:
        """Administratively add a new IPv6 lease

        Args:
            ip_address:         IPv6 Address of lease
            duid:               DHCP Unique Identifier
            iaid:               Identity Assosication Identifer

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease6-add
        """
        lease = Lease6(ip_address=ip_address, duid=duid, iaid=iaid, **kwargs)

        return self.api.send_command_with_arguments(
            command="lease6-add",
            service=self.service,
            arguments=lease.dict(exclude_none=True, exclude_unset=True, by_alias=True),
            required_hook="lease_cmds",
        )

    def lease6_del(self, ip_address: str) -> KeaResponse:
        """Deletes a lease from the lease database

        Args:
            ip_address:     IP address of lease to delete

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease6-del
        """
        return self.api.send_command_with_arguments(
            command="lease6-del",
            service=self.service,
            arguments={"ip-address": ip_address},
            required_hook="lease_cmds",
        )

    def lease6_get(self, ip_address: str, type: Lease6TypeEnum = None) -> Lease6:
        """Queries the lease database and retrieves existing lease

        Args:
            ip_address:     IP address of lease

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-get
        """
        payload = {"ip-address": ip_address}
        if type:
            payload.update["type"] = type

        data = self.api.send_command_with_arguments(
            command="lease6-get",
            service=self.service,
            arguments=payload,
            required_hook="lease_cmds",
        )

        if data.result == 3:
            raise KeaLeaseNotFoundException(ip_address)

        return Lease6.parse_obj(data.arguments)

    def lease6_get_all(self, subnets: List[int] = []) -> List[Lease6]:
        """Retrieves all IPv6 leases or all leases for the specified subnets

        Args:
            subnets:        List of subnet IDs to fetch leases for

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease6-get-all
        """
        if subnets:
            data = self.api.send_command_with_arguments(
                command="lease6-get-all",
                service=self.service,
                arguments={"subnets": subnets},
                required_hook="lease_cmds",
            )
        else:
            data = self.api.send_command(
                command="lease6-get-all",
                service=self.service,
                required_hook="lease_cmds",
            )

        if data.result == 3:
            raise KeaLeaseNotFoundException(data.text)

        leases = [Lease6.parse_obj(lease) for lease in data.arguments["leases"]]
        return leases

    def lease6_get_by_duid(self, duid: str) -> Lease6:
        """Retrieves a lease for the specified duid

        Args:
            duid:       DHCP Unique Identifier

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease6-get-by-duid
        """
        data = self.api.send_command_with_arguments(
            command="lease6-get-by-duid",
            service=self.service,
            arguments={"duid": duid},
            required_hook="lease_cmds",
        )

        if data.result == 3:
            raise KeaLeaseNotFoundException(
                f"Unable to find a lease using duid '{duid}'"
            )

        lease = data.arguments["leases"][0]
        return Lease6.parse_obj(lease)

    def lease6_get_by_hostname(self, hostname: str) -> Lease6:
        """Retrieves all IPv6 leases for the specified hostname

        Args:
            hostname:   Hostname

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease6-get-by-hostname
        """
        data = self.api.send_command_with_arguments(
            command="lease6-get-by-hostname",
            service=self.service,
            arguments={"hostname": hostname},
            required_hook="lease_cmds",
        )

        if data.result == 3:
            raise KeaLeaseNotFoundException(
                f"Unable to find lease using hostname '{hostname}'"
            )

        lease = data.arguments["leases"][0]
        return Lease6.parse_obj(lease)

    def lease6_get_page(self, limit: int, search_from: str) -> Lease6Page:
        """Retrieves all IPv6 leases by page

        Args:
            limit:          Set the limit of IPv6 leases to be returned
            search_from:    Start from either a specific IP address or 'start' for the first

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease6-get-page
        """
        data = self.api.send_command_with_arguments(
            command="lease6-get-page",
            service=self.service,
            arguments={"from": search_from, "limit": limit},
            required_hook="lease_cmds",
        )

        return Lease6Page.parse_obj(data.arguments)

    def lease6_resend_ddns(self, ip_address: str) -> KeaResponse:
        """Sends an internal request to the ddns daemon to update DNS for an existing lease

        Args:
            ip_address:     Lease to update DDNS record

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease6-resend-ddns
        """
        return self.api.send_command_with_arguments(
            command="lease6-resend-ddns",
            service=self.service,
            arguments={"ip-address": ip_address},
            required_hook="lease_cmds",
        )

    def lease6_update(
        self, ip_address: str, duid: str, iaid: int, **kwargs
    ) -> KeaResponse:
        """Updates an existing lease

        Args:
            ip_address:     Lease IPv6 Address
            duid:           DHCP Unique Identifier
            iaid:           IAID

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#lease4-update
        """
        lease = Lease6(ip_address=ip_address, duid=duid, iaid=iaid, **kwargs)

        return self.api.send_command_with_arguments(
            command="lease6-update",
            service=self.service,
            arguments=lease.dict(exclude_none=True, exclude_unset=True, by_alias=True),
            required_hook="lease_cmds",
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
                    network.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                    for network in shared_networks
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

    def remote_class6_del(self, name: str, remote_map: dict = {}) -> KeaResponse:
        """Deletes a DHCPv6 client class from the configuration database

        Args:
            name:       Name of the client class
            remote_map: (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-class6-del
        """
        return self.api.send_command_remote(
            command="remote-class6-del",
            service=self.service,
            arguments={"client-classes": [{"name": name}]},
            remote_map=remote_map,
        )

    def remote_class6_get(self, name: str, remote_map: dict = {}) -> ClientClass6:
        """Gets a DHCPv6 client class from the configuration database

        Args:
            name:       Name of the client class
            remote_map: (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-class6-get
        """
        data = self.api.send_command_remote(
            command="remote-class6-get",
            service=self.service,
            arguments={"client-classes": [{"name": name}]},
            remote_map=remote_map,
        )

        if data.result == 3:
            raise KeaClientClassNotFoundException(client_class=name)

        if not data.arguments.get("client-classes"):
            return None

        client_class = data.arguments["client-classes"][0]
        return ClientClass6.parse_obj(client_class)

    def remote_class6_get_all(
        self, server_tags: List[str] = ["all"], remote_map: dict = {}
    ) -> ClientClass6:
        """Gets all DHCPv6 client classes from the configuration database

        Args:
            server_tags:    List of Server Tags
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-class6-get-all
        """
        data = self.api.send_command_remote(
            command="remote-class6-get-all",
            service=self.service,
            arguments={"server-tags": server_tags},
            remote_map=remote_map,
        )

        client_classes = data.arguments.get("client-classes")
        return [ClientClass6.parse_obj(client_class) for client_class in client_classes]

    def remote_class6_set(
        self,
        client_class: ClientClass6,
        server_tags: List[str] = ["all"],
        follow_class_name: str = None,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Creates/Replaces a DHCPv6 Client Class in the configuration database

        Args:
            client_class:       ClientClass6 Object
            follow_class_name:  Places client class after existing class in the hierarchy
            remote_map:         (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-class6-set
        """
        data = client_class.dict(exclude_none=True, exclude_unset=True, by_alias=True)
        if follow_class_name:
            data["follow-class-name"] = follow_class_name

        return self.api.send_command_remote(
            command="remote-class6-set",
            service=self.service,
            arguments={"client-classes": [data], "server-tags": server_tags},
            remote_map=remote_map,
        )

    def remote_global_parameter6_del(
        self, parameter: str, server_tag: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes a global DHCPv6 parameter from the configuration database

        Args:
            parameter:      Parameter to delete
            server_tag:     Single Server Tag
            remote_map:     remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-global-parameter6-del
        """
        return self.api.send_command_remote(
            command="remote-global-parameter6-del",
            service=self.service,
            arguments={"parameters": [parameter], "server-tags": [server_tag]},
            remote_map=remote_map,
        )

    def remote_global_parameter6_get(
        self, parameter: str, server_tag: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Get a specific global parameter from the configuration database

        Args:
            parameter:      Parameter to delete
            server_tag:     Single Server Tag
            remote_map:     remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-global-parameter6-get
        """
        return self.api.send_command_remote(
            command="remote-global-parameter6-get",
            service=self.service,
            arguments={"parameters": [parameter], "server-tags": [server_tag]},
            remote_map=remote_map,
        )

    def remote_global_parameter6_get_all(
        self, server_tag: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Gets all global parameter from the configuration database

        Args:
            server_tag:     Single Server Tag
            remote_map:     remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-global-parameter6-get-all
        """
        return self.api.send_command_remote(
            command="remote-global-parameter6-get-all",
            service=self.service,
            arguments={"server-tags": [server_tag]},
            remote_map=remote_map,
        )

    def remote_global_parameter6_set(
        self, parameters: dict, server_tag: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Creates/Updates one or more global parameters in the configuration database

        Args:
            parameters:     Dictionary of parameters (key) and their config (values)
            server_tag:     Single Server Tag
            remote_map:     remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-global-parameter6-set
        """
        return self.api.send_command_remote(
            command="remote-global-parameter6-set",
            service=self.service,
            arguments={"parameters": parameters, "server-tags": [server_tag]},
            remote_map=remote_map,
        )

    def remote_option_def6_del(
        self,
        option_code: int,
        option_space: str,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Delete a DHCPv6 option defined in the configuration database

        Args:
            option_code:    Option Code
            option_space:   Option Space
            server_tag:     Single Server Tag
            remote_map:     remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option-def6-del
        """
        return self.api.send_command_remote(
            command="remote-option-def6-del",
            service=self.service,
            arguments={
                "option-defs": [{"code": option_code, "space": option_space}],
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option_def6_get(
        self,
        option_code: int,
        option_space: str,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Delete a DHCPv6 option defined in the configuration database

        Args:
            option_code:    Option Code
            option_space:   Option Space
            server_tag:     Single Server Tag
            remote_map:     remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option-def6-get
        """
        return self.api.send_command_remote(
            command="remote-option-def6-get",
            service=self.service,
            arguments={
                "option-defs": [{"code": option_code, "space": option_space}],
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option_def6_get_all(self, server_tag: str, remote_map: dict = {}):
        """Fetches all Dhcpv6 option defs from the configuration database

        Args:
            server_tag:     Single Server Tag
            remote_map:     remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option-def6-get-all
        """
        return self.api.send_command_remote(
            command="remote-option-def6-get-all",
            service=self.service,
            arguments={"server-tags": [server_tag]},
            remote_map=remote_map,
        )

    def remote_option_def6_set(
        self,
        option_def: OptionDef,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Delete a DHCPv6 option defined in the configuration database

        Args:
            option_def:     OptionDef Object
            server_tag:     Single Server Tag
            remote_map:     remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option-def63-set
        """
        return self.api.send_command_remote(
            command="remote-option-def6-set",
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

    def remote_option6_global_del(
        self,
        option_code: int,
        option_space: str,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Delete a DHCPv6 global option defined in the configuration database

        Args:
            option_code:    Option Code
            option_space:   Option Space
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option6-global-del
        """
        return self.api.send_command_remote(
            command="remote-option6-global-del",
            service=self.service,
            arguments={
                "options": [{"code": option_code, "space": option_space}],
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option6_global_get(
        self,
        option_code: int,
        option_space: str,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Gets a DHCPv6 global option defined in the configuration database

        Args:
            option_code:    Option Code
            option_space:   Option Space
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option6-global-get
        """
        return self.api.send_command_remote(
            command="remote-option6-global-get",
            service=self.service,
            arguments={
                "options": [{"code": option_code, "space": option_space}],
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option6_global_get_all(
        self,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Gets all DHCPv6 global option defined in the configuration database

        Args:
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option6-global-get-all
        """
        return self.api.send_command_remote(
            command="remote-option6-global-get-all",
            service=self.service,
            arguments={
                "server-tags": [server_tag],
            },
            remote_map=remote_map,
        )

    def remote_option6_global_set(
        self,
        option_data: OptionData,
        server_tag: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Creates/Replaces a DHCPv6 option defined in the configuration database

        Args:
            option_data:    OptionData Object
            server_tag:     Single Server Tag
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option6-global-set
        """
        return self.api.send_command_remote(
            command="remote-option6-global-set",
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

    def remote_option6_network_del(
        self,
        shared_network: str,
        option_code: int,
        option_space: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Delete a DHCPv6 option from a shared network in the configuration database

        Args:
            shared_network:     Name of shared network
            option_code:        Option Code
            option_space:       Option Space
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option6-network-del
        """
        return self.api.send_command_remote(
            command="remote-option6-network-del",
            service=self.service,
            arguments={
                "shared-networks": [{"name": shared_network}],
                "options": [{"code": option_code, "space": option_space}],
            },
            remote_map=remote_map,
        )

    def remote_option6_network_set(
        self,
        shared_network: str,
        option_data: OptionData,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Delete a DHCPv6 option from a shared network in the configuration database

        Args:
            shared_network:     Name of shared network
            option_data:        OptionData Object
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option6-network-set
        """
        return self.api.send_command_remote(
            command="remote-option6-network-set",
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

    def remote_option6_pd_pool_del(
        self,
        prefix: str,
        prefix_len: int,
        option_code: int,
        option_space: str,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Deletes a DHCPv6 option from a prefix delegation pool in the configuration database

        Args:
            prefix:         Delegated Prefix
            prefix_len:     Delegated Prefix Length
            option_code:    Option Code
            option_space:   Option Space
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option6-pd-pool-del
        """
        return self.api.send_command_remote(
            command="remote-option6-pd-pool-del",
            service=self.service,
            arguments={
                "pd-pools": [{"prefix": prefix, "prefix-len": prefix_len}],
                "options": [{"code": option_code, "space": option_space}],
            },
            remote_map=remote_map,
        )

    def remote_option6_pd_pool_set(
        self,
        prefix: str,
        prefix_len: int,
        option_data: OptionData,
        remote_map: dict = {},
    ) -> KeaResponse:
        """Creates/Replaces a DHCPv6 option in a prefix delegation pool in the configuration database

        Args:
            prefix:         Delegated Prefix
            prefix_len:     Delegated Prefix Length
            option_data:    OptionData Object
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option6-pd-pool-set
        """
        return self.api.send_command_remote(
            command="remote-option6-pd-pool-set",
            service=self.service,
            arguments={
                "pd-pools": [{"prefix": prefix, "prefix-len": prefix_len}],
                "options": [
                    option_data.dict(
                        exclude_none=True, exclude_unset=True, by_alias=True
                    )
                ],
            },
            remote_map=remote_map,
        )

    def remote_option6_pool_del(
        self, pool: str, option_code: int, option_space: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes a DHCPv6 option from an address pool in the configuration database

        Args:
            pool:           Pool Range
            option_code:    Option Code
            option_space:   Option Space
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option6-pool-del
        """
        return self.api.send_command_remote(
            command="remote-option6-pool-del",
            service=self.service,
            arguments={
                "pools": [{"pool": pool}],
                "options": [{"code": option_code, "space": option_space}],
            },
            remote_map=remote_map,
        )

    def remote_option6_pool_set(
        self, pool: str, option_data: OptionData, remote_map: dict = {}
    ) -> KeaResponse:
        """Creates/Replaces a DHCPv6 option in an address pool in the configuration database

        Args:
            pool:           Pool Range
            option_data:    OptionData Object
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option6-pool-set
        """
        return self.api.send_command_remote(
            command="remote-option6-pool-set",
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

    def remote_option6_subnet_del(
        self, subnet_id: int, option_code: int, option_space: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes a DHCPv6 option from a subnet in the configuration database

        Args:
            subnet_id:      Subnet ID
            option_code:    Option Code
            option_space:   Option Space
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-option6-subnet-del
        """
        return self.api.send_command_remote(
            command="remote-option6-subnet-del",
            service=self.service,
            arguments={
                "subnets": [{"id": subnet_id}],
                "options": [{"code": option_code, "space": option_space}],
            },
            remote_map=remote_map,
        )

    def remote_option6_subnet_set(
        self, subnet_id: int, option_data: OptionData, remote_map: dict = {}
    ) -> KeaResponse:
        """Creates/Replaces a DHCPv6 option in a subnet in the configuration database

        Args:
            subnet_id:      Subnet ID
            option_data:    OptionData Object
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database
        """
        return self.api.send_command_remote(
            command="remote-option6-subnet-set",
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

    def remote_network6_del(
        self, name: str, keep_subnets: bool = True, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes an existing Shared Network from the configuration database

        Args:
            name:           Name of shared network
            keep_subnets:   Keeps any existing subnets if True
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-network6-del
        """
        return self.api.send_command_remote(
            command="remote-network6-del",
            service=self.service,
            arguments={
                "shared-networks": [{"name": name}],
                "subnets-action": "keep" if keep_subnets else "delete",
            },
            remote_map=remote_map,
        )

    def remote_network6_get(
        self, name: str, include_subnets: bool = True, remote_map: dict = {}
    ) -> SharedNetwork6:
        """Returns detailed information about a shared network, including subnets

        Args:
            name:               Name of shared network
            include_subnets:    Include detailed information about subnets
            remote_map:         (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-network6-get
        """
        data = self.api.send_command_remote(
            command="remote-network6-get",
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
        return SharedNetwork6.parse_obj(shared_network)

    def remote_network6_list(
        self, server_tags: List[str], remote_map: dict = {}
    ) -> List[SharedNetwork6]:
        """Gets all shared networks in the configuration database:

        Args:
            server_tags:        List of server tags (at least 1 one must be present)
            remote_map:         (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-network6-list
        """
        data = self.api.send_command_remote(
            command="remote-network6-list",
            service=self.service,
            arguments={"server-tags": server_tags},
            remote_map=remote_map,
        )

        shared_networks = [
            SharedNetwork6.parse_obj(shared_network)
            for shared_network in data.arguments["shared-networks"]
        ]
        return shared_networks

    def remote_network6_set(
        self,
        shared_networks: List[SharedNetwork6],
        server_tags: List[str],
        remote_map: dict = {},
    ) -> KeaResponse:
        """Adds or replaces shared-network configuration in the configuration database

        Args:
            shared_networks:    List of shared networks to add
            server_tags:        List of server tags (at least 1 one must be present)
            remote_map:         (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-network6-set
        """

        # Shared networks must not contain subnets in this API call
        for shared_network in shared_networks:
            if shared_network.subnet6:
                raise KeaException(
                    message=f"Shared Network {shared_network.name} contains a list of 1 or more subnets. Please refer to documentation on how to use this command."
                )

        return self.api.send_command_remote(
            command="remote-network6-set",
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

    def remote_server6_del(self, servers: List[str], remote_map: dict = {}):
        """Delete information about a selected DHCP server from the configuration database

        Args:
            servers:    List of servers to delete
            remote_map: (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-server6-del
        """
        servers = [RemoteServer(server_tag=server) for server in servers]

        return self.api.send_command_remote(
            command="remote-server6-del",
            service=self.service,
            arguments={
                "servers": [
                    server.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                ]
                for server in servers
            },
            remote_map=remote_map,
        )

    def remote_server6_get(self, server_tag: str, remote_map: dict = {}):
        """Get information about a specific DHCP server from the configuration database

        Args:
            server_tag:     Server tag to get
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-server6-get

        """
        server = RemoteServer(server_tag=server_tag)
        data = self.api.send_command_remote(
            command="remote-server6-get",
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

    def remote_server6_get_all(self, remote_map: dict = {}) -> KeaResponse:
        """Fetches all user-defined DHCPv6 servers from the database

        Args:
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-remote-server6-get-all
        """
        data = self.api.send_command_remote(
            command="remote-server6-get-all",
            service=self.service,
            remote_map=remote_map,
        )

        return [
            RemoteServer.parse_obj(server) for server in data.arguments.get("servers")
        ]

    def remote_server6_set(self, servers: List[RemoteServer], remote_map: dict = {}):
        """Creates or replaces information about a DHCP server in the database

        Args:
            servers:        List of Servers to set
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-server6-set

        """
        return self.api.send_command_remote(
            command="remote-server6-set",
            service=self.service,
            arguments={
                "servers": [
                    server.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                ]
                for server in servers
            },
            remote_map=remote_map,
        )

    def remote_subnet6_del_by_id(
        self, subnet_id: int, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes a subnet from the configuration database

        Args:
            subnet_id:      Subnet ID
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-subnet6-del-by-id
        """
        return self.api.send_command_remote(
            command="remote-subnet6-del-by-id",
            service=self.service,
            arguments={"subnets": [{"id": subnet_id}]},
            remote_map=remote_map,
        )

    def remote_subnet6_del_by_prefix(
        self, prefix: str, remote_map: dict = {}
    ) -> KeaResponse:
        """Deletes a subnet from the configuration database

        Args:
            prefix:         Subnet Prefix
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database
        """
        return self.api.send_command_remote(
            command="remote-subnet6-del-by-prefix",
            service=self.service,
            arguments={"subnets": [{"subnet": prefix}]},
            remote_map=remote_map,
        )

    def remote_subnet6_get_by_id(
        self, subnet_id: int, remote_map: dict = {}
    ) -> Subnet6:
        """Gets a Subnet based on id from the configuration database

        Args:
            subnet_id:      Subnet ID
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-subnet6-get-by-id
        """
        data = self.api.send_command_remote(
            command="remote-subnet6-get-by-id",
            service=self.service,
            arguments={"subnets": [{"id": subnet_id}]},
            remote_map=remote_map,
        )

        if data.result == 3:
            raise KeaSubnetNotFoundException(subnet_id)

        if not data.arguments.get("subnets"):
            return None

        subnet = data.arguments["subnets"][0]
        return Subnet6.parse_obj(subnet)

    def remote_subnet6_get_by_prefix(
        self, prefix: str, remote_map: dict = {}
    ) -> Subnet6:
        """Gets a Subnet based on subnet CIDR from the configuration database

        Args:
            prefix:         Subnet CIDR
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-subnet6-get-by-prefix
        """
        data = self.api.send_command_remote(
            command="remote-subnet6-get-by-prefix",
            service=self.service,
            arguments={"subnets": [{"subnet": prefix}]},
            remote_map=remote_map,
        )

        if data.result == 3:
            raise KeaSubnetNotFoundException(prefix)

        if not data.arguments.get("subnets"):
            return None

        subnet = data.arguments["subnets"][0]
        return Subnet6.parse_obj(subnet)

    def remote_subnet6_list(
        self, server_tags: List[str], remote_map: dict = {}
    ) -> List[Subnet6]:
        """List all currently configured subnets in the configuration database

        Args:
            server_tags:    List of server tags (at least 1 one must be present)
            remote_map:     (remote_type, remote_host or remote_port) to select a specific remote database

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-subnet6-list
        """
        data = self.api.send_command_remote(
            command="remote-subnet6-list",
            service=self.service,
            arguments={"server-tags": server_tags},
            remote_map=remote_map,
        )

        subnets = [Subnet6.parse_obj(subnet) for subnet in data.arguments["subnets"]]
        return subnets

    def remote_subnet6_set(
        self,
        subnet: Subnet6,
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
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#remote-subnet6-set

        """
        data = subnet.dict(
            exclude_none=True,
            exclude_unset=True,
            by_alias=True,
        )

        data["shared-network-name"] = shared_network_name

        return self.api.send_command_remote(
            command="remote-subnet6-set",
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
        reservation = Reservation6(ip_addresses=[ip_address], **kwargs)

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
            raise KeaUnknownHostReservationTypeException

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
    ) -> Reservation6:
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

        return Reservation6.parse_obj(data.arguments)

    def reservation_get_by_identifier(
        self,
        subnet_id: int,
        identifier_type: HostReservationIdentifierEnum,
        identifier: str,
    ) -> Reservation6:
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

        return Reservation6.parse_obj(data.arguments)

    def reservation_get_all(self, subnet_id: int) -> List[Reservation6]:
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
            Reservation6.parse_obj(reservation)
            for reservation in reservations.arguments.get("hosts")
        ]

    def reservation_get_by_hostname(
        self, hostname: str, subnet_id: int
    ) -> Reservation6:
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

        return Reservation6.parse_obj(data.arguments["hosts"][0])

    def reservation_get_page(
        self,
        subnet_id: int = None,
        limit: int = 1000,
        source_index: int = 0,
        from_host_id: int = 0,
    ) -> List[Reservation6]:
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
            Reservation6.parse_obj(reservation)
            for reservation in data.arguments["hosts"]
        ]

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
                "subnet6": [
                    subnet.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                    for subnet in subnets
                ]
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

    def subnet6_delta_add(self, subnets: List[Subnet6]) -> KeaResponse:
        """Updates (adds or overwrites) parts of a single subnet

        Args:
            subnets:        List of subnets to update/add

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet6-delta-add
        """
        return self.api.send_command_with_arguments(
            command="subnet6-delta-add",
            service=self.service,
            arguments={
                "subnet6": [
                    subnet.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                    for subnet in subnets
                ]
            },
            required_hook="subnet_cmds",
        )

    def subnet6_delta_del(self, subnets: List[Subnet6]) -> KeaResponse:
        """Updates (removes) parts of a single subnet

        Args:
            subnets:        List of subnets to update/delete

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet6-delta-del
        """
        return self.api.send_command_with_arguments(
            command="subnet6-delta-del",
            service=self.service,
            arguments={
                "subnet6": [
                    subnet.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                    for subnet in subnets
                ]
            },
            required_hook="subnet_cmds",
        )

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

        if not data.arguments["subnet6"]:
            return None

        subnet = data.arguments["subnet6"][0]
        return Subnet6.parse_obj(subnet)

    def subnet6_list(self) -> List[Subnet6]:
        """List all currently configured subnets

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet6-list
        """
        data = self.api.send_command(
            command="subnet6-list",
            service=self.service,
            required_hook="subnet_cmds",
        )

        subnets = [Subnet6.parse_obj(subnet) for subnet in data.arguments["subnets"]]
        return subnets

    def subnet6_update(self, subnets: List[Subnet6]) -> List[Subnet6]:
        """Updates (overwrites) a single subnet

        Args:
            subnets:        List of subnets to overwrite

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#subnet6-update
        """
        return self.api.send_command_with_arguments(
            command="subnet6-update",
            service=self.service,
            arguments={
                "subnet6": [
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
