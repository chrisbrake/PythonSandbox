import re


class Mac(object):
    MAC_PATTERN = re.compile(r'[0-9A-Fa-f]')

    @classmethod
    def sanitise_mac(cls, mac_raw):
        """
        Extract just the relevant characters from the provided string
        and store them as a 12 Tuple.
        :exception ValueError,
            Raised if a valid mac address cannot be extracted from mac_raw.
        :param mac_raw: String,
            A mac address and delimiter characters will be discarded.
        :return: 12 Tuple, representing the 12 characters of a Mac Address.
        """
        mac = tuple(cls.MAC_PATTERN.findall(mac_raw.upper()))
        if not len(mac) == 12:
            raise ValueError(
                'A valid MAC address could not be extracted from'
                '"%s".' % mac_raw)
        else:
            return mac

    def __init__(self, mac_raw):
        """
        Initialize the classes.
        :param mac_raw: String, should contain a mac address.
            Any delimiters will be discarded.
        """
        self.mac = self.sanitise_mac(mac_raw)
        self.__mac_string = str()
        self.__mac_repr = str()

    def __str__(self):
        """
        Construct and return a string representation of the stored mac address.
        :return: String, mac formatted as FF-FF-FF-FF-FF-FF
        """
        if not self.__mac_string:
            self.__mac_string = '-'.join([
                even + odd for even, odd in zip(self.mac[0::2], self.mac[1::2])
            ])
        return self.__mac_string

    def __repr__(self):
        """
        Construct and return a string representation of the stored mac address.
        :return: String, mac formatted as FFFFFFFFFFFF
        """
        if not self.__mac_repr:
            self.__mac_repr = ''.join(self.mac)
        return self.__mac_repr

    def __eq__(self, other):
        """
        Override the standard classes equality method to provide a more
        accurate comparison.
        :param other: The object to compare against.
        :return: Boolean, True if both are instances of the same classes and
            have the same content in their mac attributes. Otherwise False.
        """
        if isinstance(other, self.__class__):
            return self.mac == other.mac
        return False

    def __ne__(self, other):
        """
        Override the standard classes inequality method to provide a more
        accurate comparison.
        :param other: The object to compare against.
        :return: Boolean, False if both are instances of the same classes and
            have the same content in their mac attributes. Otherwise True.
        """
        return not self.__eq__(other)
