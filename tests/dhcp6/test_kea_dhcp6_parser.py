import json
from pykeadhcp import Kea
from pykeadhcp.parsers.dhcp6 import Dhcp6Parser


def test_kea_dhcp6_parser_parse_config(kea_server: Kea):
    cached_config = kea_server.dhcp6.cached_config
    parsed = Dhcp6Parser(config=cached_config)

    assert parsed.config.interfaces_config
    assert parsed.config.control_socket
    assert json.dumps(
        parsed.config.dict(exclude_none=True, by_alias=True),
        indent=4,
        sort_keys=True,
    )


def test_kea_dhcp6_parser_config_test(kea_server: Kea):
    cached_config = kea_server.dhcp6.cached_config
    parsed = Dhcp6Parser(config=cached_config)
    config_to_test = {"Dhcp6": parsed.config.dict(exclude_none=True, by_alias=True)}

    test_results = kea_server.dhcp6.config_test(config=config_to_test)
    assert test_results.result == 0

    cached_config_json = json.dumps(cached_config, indent=4)
    parsed_config_json = json.dumps(config_to_test, indent=4, sort_keys=True)
    assert cached_config_json == parsed_config_json
