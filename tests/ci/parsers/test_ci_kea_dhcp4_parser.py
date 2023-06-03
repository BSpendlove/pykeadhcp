import pytest
from pykeadhcp.parsers.dhcp4 import Dhcp4Parser
from pykeadhcp.parsers.exceptions import (
    ParserSubnetIDAlreadyExistError,
    ParserSubnetCIDRAlreadyExistError,
    ParserReservationAlreadyExistError,
    ParserSubnetPoolAlreadyExistError,
    ParserPoolAddressNotInSubnetError,
)


def test_kea_dhcp4_parser_load(dhcp4_parser: Dhcp4Parser):
    assert dhcp4_parser


def test_kea_dhcp4_parser_add_shared_network(dhcp4_parser: Dhcp4Parser):
    dhcp4_parser.add_shared_network(name="pykeadhcp-dhcp4-parser")
    assert len(dhcp4_parser.config.shared_networks) > 0


def test_kea_dhcp4_parser_get_shared_network(dhcp4_parser: Dhcp4Parser):
    shared_network = dhcp4_parser.get_shared_network(name="pykeadhcp-dhcp4-parser")
    assert shared_network


def test_kea_dhcp4_parser_add_shared_network_option(dhcp4_parser: Dhcp4Parser):
    shared_network = dhcp4_parser.add_dhcp_option_to_shared_network(
        name="pykeadhcp-dhcp4-parser", code=15, data="pykeadhcp.local"
    )
    assert len(shared_network.option_data) > 0


def test_kea_dhcp4_parser_add_subnet(dhcp4_parser: Dhcp4Parser):
    dhcp4_parser.add_subnet(
        id=40123, subnet="192.0.2.0/24", option_data=[{"code": 3, "data": "192.0.2.1"}]
    )
    assert len(dhcp4_parser.config.subnet4) > 0


def test_kea_dhcp4_parser_add_existing_subnet_id(dhcp4_parser: Dhcp4Parser):
    with pytest.raises(ParserSubnetIDAlreadyExistError):
        dhcp4_parser.add_subnet(id=40123, subnet="192.0.2.0/24")


def test_kea_dhcp4_parser_add_existing_subnet_cidr(dhcp4_parser: Dhcp4Parser):
    with pytest.raises(ParserSubnetCIDRAlreadyExistError):
        dhcp4_parser.add_subnet(id=40124, subnet="192.0.2.0/24")


def test_kea_dhcp4_parser_add_subnet_reservation(dhcp4_parser: Dhcp4Parser):
    dhcp4_parser.add_reservation_to_subnet(
        id=40123,
        ip_address="192.0.2.1",
        hw_address="aa:bb:cc:dd:ee:ff",
        client_id="pykeadhcp-client-id",
        circuit_id="pykeadhcp-circuit-id",
        flex_id="pykeadhcp-flex-id",
    )

    subnet = dhcp4_parser.get_subnet(id=40123)
    assert len(subnet.reservations) > 0


def test_kea_dhcp4_parser_add_subnet_reservation_existing(dhcp4_parser: Dhcp4Parser):
    with pytest.raises(ParserReservationAlreadyExistError):
        dhcp4_parser.add_reservation_to_subnet(
            id=40123,
            ip_address="192.0.2.1",
            hw_address="aa:bb:cc:dd:ee:ff",
        )


def test_kea_dhcp4_parser_get_reservation_ip(dhcp4_parser: Dhcp4Parser):
    reservation = dhcp4_parser.get_reservation_by_ip(ip_address="192.0.2.1")
    assert reservation


def test_kea_dhcp4_parser_get_reservation_not_exist(dhcp4_parser: Dhcp4Parser):
    no_reservation = dhcp4_parser.get_reservation_by_ip(ip_address="192.0.2.2")
    assert no_reservation == None


def test_kea_dhcp4_parser_get_reservation_by_hw_address(dhcp4_parser: Dhcp4Parser):
    reservation = dhcp4_parser.get_reservation_by_hw_address(
        hw_address="aa:bb:cc:dd:ee:ff"
    )
    assert reservation
    assert reservation.ip_address == "192.0.2.1"


def test_kea_dhcp4_parser_get_reservation_by_client_id(dhcp4_parser: Dhcp4Parser):
    reservation = dhcp4_parser.get_reservation_by_client_id(
        client_id="pykeadhcp-client-id"
    )
    assert reservation
    assert reservation.ip_address == "192.0.2.1"


def test_kea_dhcp4_parser_get_reservation_by_circuit_id(dhcp4_parser: Dhcp4Parser):
    reservation = dhcp4_parser.get_reservation_by_circuit_id(
        circuit_id="pykeadhcp-circuit-id"
    )
    assert reservation
    assert reservation.ip_address == "192.0.2.1"


def test_kea_dhcp4_parser_get_reservation_by_flex_id(dhcp4_parser: Dhcp4Parser):
    reservation = dhcp4_parser.get_reservation_by_flex_id(flex_id="pykeadhcp-flex-id")
    assert reservation
    assert reservation.ip_address == "192.0.2.1"


def test_kea_dhcp4_parser_change_reservation(dhcp4_parser: Dhcp4Parser):
    reservation = dhcp4_parser.get_reservation_by_ip(ip_address="192.0.2.1")
    reservation.circuit_id = "new-circuit-id"
    reservation.flex_id = "new-flex-id"

    assert dhcp4_parser.get_reservation_by_circuit_id(circuit_id="new-circuit-id")
    assert dhcp4_parser.get_reservation_by_flex_id(flex_id="new-flex-id")


def test_kea_dhcp4_parser_get_subnet_by_reservation(dhcp4_parser: Dhcp4Parser):
    subnet = dhcp4_parser.get_subnet_by_reservation(ip_address="192.0.2.1")
    assert subnet.id == 40123


def test_kea_dhcp4_parser_remove_reservation(dhcp4_parser: Dhcp4Parser):
    dhcp4_parser.remove_reservation(id=40123, ip_address="192.0.2.1")

    no_reservation = dhcp4_parser.get_reservation_by_ip(ip_address="192.0.2.1")
    assert no_reservation == None

    subnet = dhcp4_parser.get_subnet(id=40123)
    assert len(subnet.reservations) == 0


def test_kea_dhcp4_parser_remove_reservation_not_exist(dhcp4_parser: Dhcp4Parser):
    no_reservation = dhcp4_parser.remove_reservation(id=40123, ip_address="192.0.2.1")
    assert no_reservation == None


def test_kea_dhcp4_parser_subnet_add_pool(dhcp4_parser: Dhcp4Parser):
    subnet = dhcp4_parser.add_pool_to_subnet(
        id=40123, start="192.0.2.100", end="192.0.2.200"
    )
    assert len(subnet.pools) > 0


def test_kea_dhcp4_parser_subnet_add_pool_existing(dhcp4_parser: Dhcp4Parser):
    with pytest.raises(ParserSubnetPoolAlreadyExistError):
        dhcp4_parser.add_pool_to_subnet(
            id=40123, start="192.0.2.100", end="192.0.2.200"
        )


def test_kea_dhcp4_parser_subnet_add_pool_bad_ip(dhcp4_parser: Dhcp4Parser):
    with pytest.raises(ParserPoolAddressNotInSubnetError):
        dhcp4_parser.add_pool_to_subnet(
            id=40123, start="198.51.100.100", end="192.0.2.200"
        )


def test_kea_dhcp4_parser_subnet_remove_pool(dhcp4_parser: Dhcp4Parser):
    dhcp4_parser.remove_subnet_pool(id=40123, pool="192.0.2.100-192.0.2.200")
    subnet = dhcp4_parser.get_subnet(id=40123)
    assert len(subnet.pools) == 0


def test_kea_dhcp4_parser_get_subnet_by_default_gateway(dhcp4_parser: Dhcp4Parser):
    subnet = dhcp4_parser.get_subnet_by_default_gateway(ip_address="192.0.2.1")
    assert subnet
    assert subnet.id == 40123


def test_kea_dhcp4_parser_add_subnet_to_shared_network(dhcp4_parser: Dhcp4Parser):
    shared_network = dhcp4_parser.add_subnet_to_shared_network(
        id=40123, name="pykeadhcp-dhcp4-parser"
    )

    assert len(shared_network.subnet) > 0


def test_kea_dhcp4_parser_remove_subnet_from_shared_network(dhcp4_parser: Dhcp4Parser):
    dhcp4_parser.remove_subnet_from_shared_network(
        id=40123, name="pykeadhcp-dhcp4-parser"
    )
    shared_network = dhcp4_parser.get_shared_network(name="pykeadhcp-dhcp4-parser")
    assert len(shared_network.subnet4) == 0


def test_kea_dhcp4_parser_remove_shared_network(dhcp4_parser: Dhcp4Parser):
    dhcp4_parser.remove_shared_network(name="pykeadhcp-dhcp4-parser")
    shared_network = dhcp4_parser.get_shared_network(name="pykeadhcp-dhcp4-parser")
    assert shared_network == None
