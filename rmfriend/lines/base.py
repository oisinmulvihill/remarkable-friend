# -*- coding: utf-8 -*-
"""
"""
import struct


def recover(raw_bytes, class_=None, offset=0):
    """A generator to iterate through the raw bytes
    """
    data = ''
    size = 0

    while True:
        if class_ is not None:
            size = struct.calcsize(class_.fmt)
            data = struct.unpack_from(class_.fmt, raw_bytes, offset=offset)
            data = data[0]
            offset += size
            print(
                "position:{} fmt:{} offset:{} size:{} data:{}".
                format(class_.__name__, class_.fmt, offset, size, data)
            )

        # get the next format to read:
        class_ = (yield data)


class Base(object):
    """
    """
    @classmethod
    def parse(cls, position):
        """Using the classes fmt recover that amount of data next from the
        current position. This will then return the data and the byte size  of
        the data recovered.

        :param position: The generator managing the binary file.

        :returns: An instance of this class given the data and size.

        """
        return cls(position.send(cls))


class Int32(Base):
    """Convert raw bytes to an integer number.
    """
    fmt = '<I'

    def __init__(self, value):
        """
        """
        self.value = value


class Float(Base):
    """Convert raw bytes to an floating point number.
    """
    fmt = '<f'

    def __init__(self, value):
        """
        """
        self.value = value
