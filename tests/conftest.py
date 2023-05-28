import pytest
import json
from pathlib import Path
from pytest import FixtureRequest
from pykeadhcp import Kea
from pykeadhcp.models.generic import KeaResponse


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
