import re


class Mac(object):
    MAC_PATTERN = re.compile(r'[0-9A-Fa-f]')

    @classmethod
    def sanitise_mac(cls, mac_raw):
        return tuple(cls.MAC_PATTERN.findall(mac_raw.upper()))

    def __init__(self, mac_raw=str()):
        self.mac = self.sanitise_mac(mac_raw)
        self.delimiter = '-'
        self.group_len = 2
        self.__mac_as_string = str()

    def __str__(self):
        if not self.__mac_as_string:
            self.__mac_as_string = self.delimiter.join(
                [even + odd for even, odd in zip(self.mac[0::self.group_len],
                                                 self.mac[1::self.group_len])]
            )
        return self.__mac_as_string

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.mac == other.mac
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


if __name__ == '__main__':
    mac = Mac('94:61:24:00:0d:f9')
    print(mac)
