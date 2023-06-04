import pytest
from pykeadhcp.parsers.dhcp6 import Dhcp6Parser
from pykeadhcp.parsers.exceptions import (
    ParserSharedNetworkAlreadyExistError,
    ParserSubnetIDAlreadyExistError,
    ParserSubnetCIDRAlreadyExistError,
    ParserPDPoolAlreadyExistError,
    ParserPDPoolNotFoundError,
    ParserReservationAlreadyExistError,
    ParserSubnetPoolAlreadyExistError,
    ParserPoolAddressNotInSubnetError,
)


def test_kea_dhcp6_parser_load(dhcp6_parser: Dhcp6Parser):
    assert dhcp6_parser


def test_kea_dhcp6_parser_add_shared_network(dhcp6_parser: Dhcp6Parser):
    dhcp6_parser.add_shared_network(name="pykeadhcp-dhcp6-parser")
    assert len(dhcp6_parser.config.shared_networks) > 0


def test_kea_dhcp6_parser_add_shared_network_existing(dhcp6_parser: Dhcp6Parser):
    with pytest.raises(ParserSharedNetworkAlreadyExistError):
        dhcp6_parser.add_shared_network(name="pykeadhcp-dhcp6-parser")


def test_kea_dhcp6_parser_get_shared_network(dhcp6_parser: Dhcp6Parser):
    shared_network = dhcp6_parser.get_shared_network(name="pykeadhcp-dhcp6-parser")
    assert shared_network


def test_kea_dhcp6_parser_add_shared_network_option(dhcp6_parser: Dhcp6Parser):
    shared_network = dhcp6_parser.add_dhcp_option_to_shared_network(
        name="pykeadhcp-dhcp6-parser", code=15, data="pykeadhcp.local"
    )
    assert len(shared_network.option_data) > 0


def test_kea_dhcp6_parser_add_subnet(dhcp6_parser: Dhcp6Parser):
    dhcp6_parser.add_subnet(
        id=40123,
        subnet="2001:db8::/64",
        option_data=[{"code": 3, "data": "2001:db8::1"}],
    )
    assert len(dhcp6_parser.config.subnet6) > 0


def test_kea_dhcp6_parser_add_existing_subnet_id(dhcp6_parser: Dhcp6Parser):
    with pytest.raises(ParserSubnetIDAlreadyExistError):
        dhcp6_parser.add_subnet(id=40123, subnet="2001:db8::/64")


def test_kea_dhcp6_parser_add_existing_subnet_cidr(dhcp6_parser: Dhcp6Parser):
    with pytest.raises(ParserSubnetCIDRAlreadyExistError):
        dhcp6_parser.add_subnet(id=40124, subnet="2001:db8::/64")


def test_kea_dhcp6_parser_add_pd_pool(dhcp6_parser: Dhcp6Parser):
    dhcp6_parser.add_pd_pool(
        id=40123, prefix="2001:db8::", prefix_len=52, delegated_len=56
    )
    existing_subnet = dhcp6_parser.get_subnet(id=40123)
    assert len(existing_subnet.pd_pools) > 0


def test_kea_dhcp6_parser_add_pd_pool_existing(dhcp6_parser: Dhcp6Parser):
    with pytest.raises(ParserPDPoolAlreadyExistError):
        existing_subnet = dhcp6_parser.get_subnet(id=40123)
        assert len(existing_subnet.pd_pools) > 0
        for pd_pool in existing_subnet.pd_pools:
            dhcp6_parser.add_pd_pool(
                id=existing_subnet.id,
                prefix=pd_pool.prefix,
                prefix_len=pd_pool.prefix_len,
                delegated_len=pd_pool.delegated_len,
            )
            break


def test_kea_dhcp6_parser_remove_pd_pool(dhcp6_parser: Dhcp6Parser):
    pd_pool = dhcp6_parser.remove_pd_pool(id=40123, prefix="2001:db8::", prefix_len=52)
    assert pd_pool
    existing_subnet = dhcp6_parser.get_subnet(id=40123)
    assert len(existing_subnet.pd_pools) == 0


def test_kea_dhcp6_parser_remove_pd_pool_not_exist(dhcp6_parser: Dhcp6Parser):
    with pytest.raises(ParserPDPoolNotFoundError):
        dhcp6_parser.remove_pd_pool(id=40123, prefix="2001:db8::", prefix_len=52)


def test_kea_dhcp6_parser_add_subnet_reservation(dhcp6_parser: Dhcp6Parser):
    dhcp6_parser.add_reservation_to_subnet(
        id=40123,
        ip_address="2001:db8::123",
        hw_address="aa:bb:cc:dd:ee:ff",
        client_id="pykeadhcp-client-id",
        circuit_id="pykeadhcp-circuit-id",
        flex_id="pykeadhcp-flex-id",
        duid="pykeadhcp-duid",
    )

    subnet = dhcp6_parser.get_subnet(id=40123)
    assert len(subnet.reservations) > 0


def test_kea_dhcp6_parser_add_subnet_reservation_existing(dhcp6_parser: Dhcp6Parser):
    with pytest.raises(ParserReservationAlreadyExistError):
        dhcp6_parser.add_reservation_to_subnet(id=40123, ip_address="2001:db8::123")


def test_kea_dhcp6_parser_get_reservation_ip(dhcp6_parser: Dhcp6Parser):
    reservation = dhcp6_parser.get_reservation_by_ip(ip_address="2001:db8::123")
    assert reservation
    assert len(reservation.ip_addresses) > 0
    assert "2001:db8::123" in reservation.ip_addresses


def test_kea_dhcp6_parser_get_reservation_not_exist(dhcp6_parser: Dhcp6Parser):
    no_reservation = dhcp6_parser.get_reservation_by_ip(ip_address="2001:db8::124")
    assert no_reservation == None


def test_kea_dhcp6_parser_get_resrvation_by_hw_address(dhcp6_parser: Dhcp6Parser):
    reservation = dhcp6_parser.get_reservation_by_hw_address(
        hw_address="aa:bb:cc:dd:ee:ff"
    )
    assert reservation
    assert "2001:db8::123" in reservation.ip_addresses


def test_kea_dhcp6_parser_get_reservation_by_flex_id(dhcp6_parser: Dhcp6Parser):
    reservation = dhcp6_parser.get_reservation_by_flex_id(flex_id="pykeadhcp-flex-id")
    assert reservation
    assert "2001:db8::123" in reservation.ip_addresses


def test_kea_dhcp6_parser_change_reservation(dhcp6_parser: Dhcp6Parser):
    reservation = dhcp6_parser.get_reservation_by_ip(ip_address="2001:db8::123")
    reservation.duid = "new-duid-id"
    reservation.flex_id = "new-flex-id"

    assert dhcp6_parser.get_reservation_by_duid(duid="new-duid-id")
    assert dhcp6_parser.get_reservation_by_flex_id(flex_id="new-flex-id")


def test_kea_dhcp6_parser_get_subnet_by_reservation(dhcp6_parser: Dhcp6Parser):
    subnet = dhcp6_parser.get_subnet_by_reservation(ip_address="2001:db8::123")
    assert subnet.id == 40123


def test_kea_dhcp6_parser_remove_reservation(dhcp6_parser: Dhcp6Parser):
    dhcp6_parser.remove_reservation(id=40123, ip_address="2001:db8::123")

    no_reservation = dhcp6_parser.get_reservation_by_ip(ip_address="2001:db8::123")
    assert no_reservation == None

    subnet = dhcp6_parser.get_subnet(id=40123)
    assert len(subnet.reservations) == 0


def test_kea_dhcp6_parser_remove_reservation_not_exist(dhcp6_parser: Dhcp6Parser):
    no_reservation = dhcp6_parser.remove_reservation(
        id=40123, ip_address="2001:db8::123"
    )
    assert no_reservation == None


def test_kea_dhcp6_parser_subnet_add_pool(dhcp6_parser: Dhcp6Parser):
    subnet = dhcp6_parser.add_pool_to_subnet(
        id=40123, start="2001:db8::100", end="2001:db8::200"
    )
    assert len(subnet.pools) > 0


def test_kea_dhcp6_parser_subnet_add_pool_existing(dhcp6_parser: Dhcp6Parser):
    with pytest.raises(ParserSubnetPoolAlreadyExistError):
        dhcp6_parser.add_pool_to_subnet(
            id=40123, start="2001:db8::100", end="2001:db8::200"
        )


def test_kea_dhcp6_parser_subnet_add_pool_bad_ip(dhcp6_parser: Dhcp6Parser):
    with pytest.raises(ParserPoolAddressNotInSubnetError):
        dhcp6_parser.add_pool_to_subnet(
            id=40123, start="2001:db8:FFFF:FFFF::100", end="2001:db8::200"
        )


def test_kea_dhcp6_parser_subnet_remove_pool(dhcp6_parser: Dhcp6Parser):
    dhcp6_parser.remove_subnet_pool(id=40123, pool="2001:db8::100-2001:db8::200")
    subnet = dhcp6_parser.get_subnet(id=40123)
    assert len(subnet.pools) == 0


def test_kea_dhcp6_parser_subnet_get_subnet_from_default_gateway(
    dhcp6_parser: Dhcp6Parser,
):
    subnet = dhcp6_parser.get_subnet_by_default_gateway(ip_address="2001:db8::1")
    assert subnet
    assert subnet.id == 40123


def test_kea_dhcp6_parser_add_subnet_to_shared_network(dhcp6_parser: Dhcp6Parser):
    shared_network = dhcp6_parser.add_subnet_to_shared_network(
        id=40123, name="pykeadhcp-dhcp6-parser"
    )

    assert len(shared_network.subnet) > 0


def test_kea_dhcp6_parser_remove_subnet_from_shared_network(dhcp6_parser: Dhcp6Parser):
    dhcp6_parser.remove_subnet_from_shared_network(
        id=40123, name="pykeadhcp-dhcp6-parser"
    )
    shared_network = dhcp6_parser.get_shared_network(name="pykeadhcp-dhcp6-parser")
    assert len(shared_network.subnet6) == 0


def test_kea_dhcp6_parser_remove_shared_network(dhcp6_parser: Dhcp6Parser):
    dhcp6_parser.remove_shared_network(name="pykeadhcp-dhcp6-parser")
    shared_network = dhcp6_parser.get_shared_network(name="pykeadhcp-dhcp6-parser")
    assert shared_network == None
