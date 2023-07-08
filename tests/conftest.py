import pytest
import json
from pathlib import Path
from pytest import FixtureRequest
from pykeadhcp import Kea
from pykeadhcp.models.ctrlagent.config import CtrlAgentDaemonConfig
from pykeadhcp.models.dhcp4.config import Dhcp4DaemonConfig
from pykeadhcp.models.dhcp6.config import Dhcp6DaemonConfig
from pykeadhcp.parsers import CtrlAgentParser, Dhcp4Parser, Dhcp6Parser


def pytest_addoption(parser):
    parser.addoption(
        "--host",
        action="store",
        dest="host",
        type=str,
        help="Host URL for Kea Server API",
        default="http://127.0.0.1",
    )
    parser.addoption(
        "--port",
        action="store",
        dest="port",
        type=int,
        help="Port for Kea Server API",
        default=8000,
    )
    parser.addoption(
        "--disable-ssl-verify",
        action="store_true",
        dest="disable_ssl_verify",
        default=False,
        help="Disable SSL Verification when calling Kea class",
    )
    parser.addoption(
        "--ssl-ca-bundle",
        action="store",
        dest="ssl_ca_bundle",
        type=str,
        help="CA Bundle if required to pass into requests module",
        default=None,
    )
    parser.addoption(
        "--db-type",
        action="store",
        dest="db_type",
        type=str,
        help="Database Type to set in the remote_map to all API calls starting with 'remote'",
        default="mysql",
    )
    parser.addoption(
        "--db-host",
        action="store",
        dest="db_host",
        type=str,
        help="Database Host to set in the remote_map to all API calls starting with 'remote'",
        default="db",
    )


@pytest.fixture(scope="module")
def kea_server(request: FixtureRequest):
    host = request.config.getoption("host")
    port = request.config.getoption("port", default=8000)
    disable_ssl_verify = request.config.getoption("disable_ssl_verify", default=False)
    ssl_ca_bundle = request.config.getoption("ssl_ca_bundle", default=None)

    return Kea(
        host=host,
        port=port,
        verify=False
        if disable_ssl_verify
        else True
        if not ssl_ca_bundle
        else ssl_ca_bundle,
    )


def read_local_config(filename: str):
    json_file = Path(filename)
    if not json_file.exists():
        raise FileNotFoundError

    with json_file.open() as config:
        return json.load(config)


@pytest.fixture(scope="module")
def ctrlagent_model(request: FixtureRequest):
    data = read_local_config(filename="tests/configs/ctrlagent_api_config.json")
    assert data["Control-agent"]
    return CtrlAgentDaemonConfig.parse_obj(data["Control-agent"])


@pytest.fixture(scope="module")
def dhcp4_model(request: FixtureRequest):
    data = read_local_config(filename="tests/configs/dhcp4_api_config.json")
    assert data["Dhcp4"]
    return Dhcp4DaemonConfig.parse_obj(data["Dhcp4"])


@pytest.fixture(scope="module")
def dhcp6_model(request: FixtureRequest):
    data = read_local_config(filename="tests/configs/dhcp6_api_config.json")
    assert data["Dhcp6"]
    return Dhcp6DaemonConfig.parse_obj(data["Dhcp6"])


@pytest.fixture(scope="module")
def dhcp4_parser(request: FixtureRequest):
    data = read_local_config(filename="tests/configs/dhcp4_api_config.json")
    assert data["Dhcp4"]
    return Dhcp4Parser(config=data)


@pytest.fixture(scope="module")
def dhcp6_parser(request: FixtureRequest):
    data = read_local_config(filename="tests/configs/dhcp6_api_config.json")
    assert data["Dhcp6"]
    return Dhcp6Parser(config=data)


@pytest.fixture(scope="module")
def ctrlagent_parser(request: FixtureRequest):
    data = read_local_config(filename="tests/configs/ctrlagent_api_config.json")
    assert data["Control-agent"]
    return CtrlAgentParser(config=data)


@pytest.fixture(scope="module")
def db_remote_map(request: FixtureRequest):
    return {
        "type": request.config.getoption("db_type"),
        "host": request.config.getoption("db_host"),
    }
