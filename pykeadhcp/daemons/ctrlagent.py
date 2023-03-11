from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pykeadhcp import Kea


class CtrlAgent:
    def __init__(self, api: "Kea"):
        self.service = None
        self.api = api

    def build_report(self) -> dict:
        """Returns list of compilation options that this particular binary was built with

        Kea API Reference:
            https://kea.readthedocs.io/en/kea-2.2.0/api.html#ref-build-report
        """
        return self.api.send_command(command="build-report", service=self.service)
