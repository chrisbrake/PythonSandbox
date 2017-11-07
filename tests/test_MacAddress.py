from sys import path
from unittest import TestCase
path.append('../')
from MacAddress import Mac


class TestMacAddress(TestCase):
    def setUp(self):
        self.mac_no_delimiter = 'FFFFFFFFFFFF'
        self.mac_dash_delimited = 'FF-FF-FF-FF-FF-FF'
        self.mac_colon_delimited = 'FF:FF:FF:FF:FF:FF'
        self.mac_dot_delimited = 'FFFF.FFFF.FFFF'

        self.mac = tuple(f for f in self.mac_no_delimiter)
        self.supported_formats = [
            self.mac_no_delimiter,
            self.mac_dash_delimited,
            self.mac_colon_delimited,
            self.mac_dot_delimited,
        ]

    def test_basic_init(self):
        """Confirm the class can be initialised."""
        for mac_format in self.supported_formats:
            mac = Mac(mac_format)
            self.assertIsInstance(mac, Mac)

    def test_sanitise(self):
        """Confirm we can extract a valid tuple from all supported formats."""
        for mac_format in self.supported_formats:
            self.assertEqual(self.mac, Mac.sanitise_mac(mac_format))

    def test_sanitise_exception(self):
        """Confirm throw a ValueError for invalid input."""
        with self.assertRaises(ValueError):
            Mac('Not a MAC address.')

    def test_equality(self):
        """Confirm the equality method is functioning as expected."""
        for primary in self.supported_formats:
            for secondary in self.supported_formats:
                self.assertEqual(Mac(primary), Mac(secondary))

        for mac_format in self.supported_formats:
            self.assertNotEqual(Mac('AAAA.AAAA.AAAA'), Mac(mac_format))

    def test_string(self):
        """Confirm that the __str__ method is functioning as expected."""
        for mac_format in self.supported_formats:
            self.assertEqual(self.mac_dash_delimited, str(Mac(mac_format)))

    def test_representation(self):
        """Confirm that the __repr__ method is functioning as expected."""
        for mac_format in self.supported_formats:
            self.assertEqual(self.mac_no_delimiter, repr(Mac(mac_format)))
