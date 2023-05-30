from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pykeadhcp import Kea

from pykeadhcp.models.generic import KeaResponse, StatusGet


class CtrlAgent:
    def __init__(self, api: "Kea"):
        self.service = None  # Control Agent expects service: [] in payload
        self.api = api

        # Cache config and hooks
        try:
            self.cached_config = None
            self.refresh_cached_config()
            self.hook_libraries = self.api.get_active_hooks(
                hooks=self.cached_config["Control-agent"]["hooks-libraries"]
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

    def shutdown(self) -> KeaResponse:
        """Instructs the server daemon to initiate its shutdown procedure

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-shutdown
        """
        return self.api.send_command_with_arguments(
            command="shutdown", service=self.service, arguments={"exit-value": 123}
        )

    def status_get(self) -> StatusGet:
        """Returns servers runtime information

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-status-get
        """
        data = self.api.send_command(command="status-get", service=self.service)
        return StatusGet.parse_obj(data.arguments)
