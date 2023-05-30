from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pykeadhcp import Kea

from pykeadhcp.models.generic import KeaResponse


class Ddns:
    def __init__(self, api: "Kea"):
        self.service = "Ddns"
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
        eg. config-set, commands like config-test won't need a config refresh to keep the cached config up to date
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

    def list_commands(self) -> KeaResponse:
        """List all commands supported by the server/service

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-list-commands
        """
        return self.api.send_command_with_arguments(
            command="list-commands", service=self.service, arguments={}
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
