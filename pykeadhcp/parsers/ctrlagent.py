from pykeadhcp.parsers.generic import GenericParser
from pykeadhcp.models.ctrlagent.config import CtrlAgentDaemonConfig


class CtrlAgentParser(GenericParser):
    """Parser for the ISC Kea CtrlAgent configuration file. This should ideally
    be used with the cached config stored in the Daemon class like this:

    parser = CtrlAgentParser(config=server.ctrlagent.cached_config)
    """

    def __init__(self, config: dict):
        self.config = CtrlAgentDaemonConfig.parse_obj(config["Control-agent"])
