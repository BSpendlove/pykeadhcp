import json
from pykeadhcp import Kea
from pykeadhcp.parsers.ctrlagent import CtrlAgentParser


def test_kea_ctrlagent_parser_parse_config(kea_server: Kea):
    cached_config = kea_server.ctrlagent.cached_config
    parsed = CtrlAgentParser(config=cached_config)

    assert parsed.config.http_host
    assert parsed.config.http_port
    assert json.dumps(
        parsed.config.dict(exclude_none=True, by_alias=True),
        indent=4,
        sort_keys=True,
    )


def test_kea_ctrlagent_parser_config_test(kea_server: Kea):
    cached_config = kea_server.ctrlagent.cached_config
    parsed = CtrlAgentParser(config=cached_config)
    config_to_test = {
        "Control-agent": parsed.config.dict(
            exclude_none=True, exclude_unset=True, by_alias=True
        )
    }

    test_results = kea_server.ctrlagent.config_test(config=config_to_test)
    assert test_results.result == 0

    # Remove hash if exist for now until tests are created to take that into account
    if cached_config.get("hash"):
        del cached_config["hash"]

    cached_config_json = json.dumps(cached_config, indent=4)
    parsed_config_json = json.dumps(config_to_test, indent=4, sort_keys=True)
    assert cached_config_json == parsed_config_json
