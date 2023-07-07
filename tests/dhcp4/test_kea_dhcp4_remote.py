from pykeadhcp import Kea
from pykeadhcp.models.generic.remote_server import RemoteServer

# remote-server4-get-all (0 servers)
# remote-server4-set
# remote-server4-get
# remote-server4-get (non existent)
# remote-server4-get-all
# remote-server4-del


def test_kea_dhcp4_remote_server4_get_all_none(kea_server: Kea):
    servers = kea_server.dhcp4.remote_server4_get_all(remote_map={"host": "db"})
    assert len(servers) == 0


def test_kea_dhcp4_remote_server4_set(kea_server: Kea):
    response = kea_server.dhcp4.remote_server4_set(
        servers=[RemoteServer(server_tag="pykeadhcp", description="pykeadhcp-test")]
    )
    assert response.result == 0


def test_kea_dhcp4_remote_server4_get(kea_server: Kea):
    server = kea_server.dhcp4.remote_server4_get(server_tag="pykeadhcp")
    assert server
    assert server.server_tag == "pykeadhcp"
    assert server.description == "pykeadhcp-test"


def test_kea_dhcp4_remote_server4_del(kea_server: Kea):
    response = kea_server.dhcp4.remote_server4_del(servers=["pykeadhcp"])
    assert response.result == 0
    assert "deleted" in response.text
