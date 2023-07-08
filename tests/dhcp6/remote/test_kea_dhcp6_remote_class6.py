from pykeadhcp import Kea
from pykeadhcp.models.dhcp6.client_class import ClientClass6
from pykeadhcp.exceptions import KeaClientClassNotFoundException
import pytest

"""remote-class6 process:

get (non existent)
set
get
get-all
del
"""


def test_kea_dhcp6_remote_class6_get_non_existent(kea_server: Kea):
    with pytest.raises(KeaClientClassNotFoundException):
        kea_server.dhcp6.remote_class6_get(name="ipxe_efi_x64")


def test_kea_dhcp6_remote_class6_set(kea_server: Kea):
    client_class = ClientClass6(
        name="ipxe_efi_x64",
        test="option[93].hex == 0x0009",
        next_server="2001:db8::111",
        server_hostname="hal9000",
        boot_file_name="/dev/null",
    )
    response = kea_server.dhcp6.remote_class6_set(client_class=client_class)
    assert response.result == 0
    assert len(response.arguments.get("client-classes", [])) > 0


def test_kea_dhcp6_remote_class6_get(kea_server: Kea):
    response = kea_server.dhcp6.remote_class6_get(name="ipxe_efi_x64")
    assert response
    assert response.name == "ipxe_efi_x64"


def test_kea_dhcp6_remote_class6_get_all(kea_server: Kea):
    response = kea_server.dhcp6.remote_class6_get_all()
    assert response
    assert len(response) > 0


def test_kea_dhcp6_remote_class6_del(kea_server: Kea):
    response = kea_server.dhcp6.remote_class6_del(name="ipxe_efi_x64")
    assert response.result == 0
    assert response.arguments.get("count") == 1
