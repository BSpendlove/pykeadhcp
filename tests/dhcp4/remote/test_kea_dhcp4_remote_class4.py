from pykeadhcp import Kea
from pykeadhcp.models.dhcp4.client_class import ClientClass4
from pykeadhcp.exceptions import KeaClientClassNotFoundException
import pytest

"""remote-class4 process:

get (non existent)
set
get
get-all
del
"""


def test_kea_dhcp4_remote_class4_get_non_existent(kea_server: Kea):
    with pytest.raises(KeaClientClassNotFoundException):
        kea_server.dhcp4.remote_class4_get(name="ipxe_efi_x64")


def test_kea_dhcp4_remote_class4_set(kea_server: Kea):
    client_class = ClientClass4(
        name="ipxe_efi_x64",
        test="option[93].hex == 0x0009",
        next_server="192.0.2.254",
        server_hostname="hal9000",
        boot_file_name="/dev/null",
    )
    response = kea_server.dhcp4.remote_class4_set(client_class=client_class)
    assert response.result == 0
    assert len(response.arguments.get("client-classes", [])) > 0


def test_kea_dhcp4_remote_class4_get(kea_server: Kea):
    response = kea_server.dhcp4.remote_class4_get(name="ipxe_efi_x64")
    assert response
    assert response.name == "ipxe_efi_x64"


def test_kea_dhcp4_remote_class4_get_all(kea_server: Kea):
    response = kea_server.dhcp4.remote_class4_get_all()
    assert response
    assert len(response) > 0


def test_kea_dhcp4_remote_class4_del(kea_server: Kea):
    response = kea_server.dhcp4.remote_class4_del(name="ipxe_efi_x64")
    assert response.result == 0
    assert response.arguments.get("count") == 1
