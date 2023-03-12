from pykeadhcp import Kea
import pytest

"""lease4 process:
get (non-existent lease)
add
add (again to check duplicate lease)
get
get-page
update
del
wipe
reclaim
"""


def test_kea_dhcp4_lease4_get_non_exsistent(kea_server: Kea):
    response = kea_server.dhcp4.lease4_get(ip_address="192.0.2.32")
    assert response["result"] == 3


def test_kea_dhcp4_lease4_add(kea_server: Kea):
    subnet = kea_server.dhcp4.subnet4_add(
        subnets=[{"id": 40123, "subnet": "192.0.2.32/31"}]
    )
    assert subnet["result"] == 0
    response = kea_server.dhcp4.lease4_add(
        ip_address="192.0.2.32",
        identifier_key="hw-address",
        identifier_value="aa:bb:cc:11:22:33",
    )
    assert response["result"] == 0
