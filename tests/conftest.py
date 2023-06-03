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


@pytest.fixture(scope="module")
def kea_server(request: FixtureRequest):
    host = request.config.getoption("host")
    port = request.config.getoption("port", default=8000)

    return Kea(host=host, port=port)


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
