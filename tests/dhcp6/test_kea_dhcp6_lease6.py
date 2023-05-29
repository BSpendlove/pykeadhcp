from pykeadhcp import Kea
from pykeadhcp.exceptions import KeaLeaseNotFoundException
from pykeadhcp.models.dhcp6.subnet import Subnet6
import pytest

"""lease6 process:
get (non-existent lease)
add
add (again to check duplicate lease)
get
get-all
get-page
get-by-client-id
get-by-hw-address
update
del
wipe
reclaim
"""


def test_kea_dhcp6_lease6_get_non_exsistent(kea_server: Kea):
    with pytest.raises(KeaLeaseNotFoundException):
        kea_server.dhcp6.lease6_get(ip_address="2001:db8::32")
