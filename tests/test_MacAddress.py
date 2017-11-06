from sys import path
from unittest import main, TestCase
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
        for mac_format in self.supported_formats:
            mac = Mac(mac_format)
            self.assertIsInstance(mac, Mac)

    def test_sanitise(self):
        for mac_format in self.supported_formats:
            self.assertEqual(self.mac, Mac.sanitise_mac(mac_format))

    def test_equality(self):
        for primary in self.supported_formats:
            for secondary in self.supported_formats:
                self.assertEqual(Mac(primary), Mac(secondary))

        for mac_format in self.supported_formats:
            self.assertNotEqual(Mac('AAAA.AAAA.AAAA'), Mac(mac_format))

    def test_string(self):
        for mac_format in self.supported_formats:
            self.assertEqual(self.mac_dash_delimited, str(Mac(mac_format)))


if __name__ == '__main__':
    main()

