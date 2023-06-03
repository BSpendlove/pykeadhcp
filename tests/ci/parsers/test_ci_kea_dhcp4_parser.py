from pykeadhcp.parsers.dhcp4 import Dhcp4Parser


def test_kea_dhcp4_parser_load(dhcp4_parser: Dhcp4Parser):
    assert dhcp4_parser


def test_kea_dhcp4_parser_get_shared_network(dhcp4_parser: Dhcp4Parser):
    for shared_network in dhcp4_parser.config.shared_networks:
        assert dhcp4_parser.get_shared_network(name=shared_network.name)


def test_kea_dhcp4_parser_get_subnet_by_id(dhcp4_parser: Dhcp4Parser):
    for shared_network in dhcp4_parser.config.shared_networks:
        for subnet in shared_network.subnet4:
            assert dhcp4_parser.get_subnet(id=subnet.id)

    for subnet in dhcp4_parser.config.subnet4:
        assert dhcp4_parser.get_subnet(id=subnet.id)
