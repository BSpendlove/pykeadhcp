from pykeadhcp import Kea
from pykeadhcp.exceptions import KeaClientClassNotFoundException
from pykeadhcp.models.dhcp4.client_class import ClientClass4
import pytest

"""class process:
get (non-existent client-class)
add
add (again to check duplicate client-class)
get
list
update
del
del (non-existent client-class)
"""


def test_kea_dhcp4_class_get_non_existent(kea_server: Kea):
    with pytest.raises(KeaClientClassNotFoundException):
        kea_server.dhcp4.class_get(name="ipxe_efi_x64")


def test_kea_dhcp4_class_add(kea_server: Kea):
    client_class = ClientClass4(
        name="ipxe_efi_x64",
        test="option[93].hex == 0x0009",
        next_server="192.0.2.254",
        server_hostname="hal9000",
        boot_file_name="/dev/null",
    )
    response = kea_server.dhcp4.class_add(client_class=client_class)
    assert response.result == 0


def test_kea_dhcp4_class_get(kea_server: Kea):
    response = kea_server.dhcp4.class_get(name="ipxe_efi_x64")
    assert response
    assert response.name == "ipxe_efi_x64"


def test_kea_dhcp4_class_list(kea_server: Kea):
    response = kea_server.dhcp4.class_list()
    assert len(response) > 0


def test_kea_dhcp4_class_del(kea_server: Kea):
    response = kea_server.dhcp4.class_del(name="ipxe_efi_x64")
    assert response.result == 0


def test_kea_dhcp4_class_del_non_existent(kea_server: Kea):
    response = kea_server.dhcp4.class_del(name="ipxe_efi_x64")
    assert response.result == 3
