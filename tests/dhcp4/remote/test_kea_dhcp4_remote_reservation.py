"""The reason why I have created 'remote_reservation' although the API commands are 'reservation-<action>
is because you need a database to use these commands, they don't work with a mem file... Host reservations
must be configured in the global dhcp configuration files as per the documentation:

https://kea.readthedocs.io/en/kea-2.2.0/arm/hooks.html#hooks-host-cmds

"To use the commands that change reservation information (i.e. reservation-add and reservation-del), the hosts database
must be specified and it must not operate in read-only mode
(for details, see the hosts-databases descriptions in DHCPv4 Hosts Database Configuration and DHCPv6 Hosts Database Configuration)."
"""

from pykeadhcp import Kea
import pytest

"""reservation process:
reservation-get non existent
reservation-add
reservation-add existing
reservation-get
reservation-get-by-hostname
reservation-get-by-id
reservation-get-page
reservation-del
reservation-del non existent
"""


def test_kea_dhcp4_remote_reservation_get_non_existent(kea_server: Kea):
    test = None
