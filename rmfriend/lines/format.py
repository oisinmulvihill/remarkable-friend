# -*- coding: utf-8 -*-
"""

Parse the lines format.


Using inspiration from

 - https://github.com/ax3l/lines-are-beautiful

 - https://plasma.ninja/blog/devices/remarkable/binary/format/2017/12/26/
    reMarkable-lines-file-format.html


"""
import io
import struct


class Base(object):
    """
    """
    def unpack(self, fmt, raw_bytes):
        """
        """
        fmt_size = struct.calcsize(fmt)

        data = struct.unpack_from(self.fmt, raw_bytes)

        return (data, fmt_size)


class Points(Base):
    """
    """
    fmt = '<I'

    def __init__(self):
        """
        """
        self.lines = []


class Segments(Base):
    """
    """
    fmt = '<I'

    def __init__(self):
        """
        """
        self.lines = []


class Lines(Base):
    """
    """
    fmt = '<I'

    def __init__(self):
        """
        """
        self.lines = []


class Layer(Base):
    """
    """
    fmt = '<I'

    def __init__(self):
        """
        """
        self.lines = []


class Page(Base):
    """
    """
    fmt = '<I'

    @classmethod
    def parse(cls, raw_bytes, offset):
        """
        """

    def __init__(self, layers):
        """
        """
        self.raw_bytes = raw_bytes

        self.layers = []

        self.layer_count =

        for layer in range(layers):
            print("Layer Number: {}".format(layer))
            lines = read_int32_t(fd)
            print("Number of lines: {}".format(lines))


class Notebook(Base):
    """
    """
    EXPECTED_HEADER = b'reMarkable lines with selections and layers'

    fmt = '<43s'

    @classmethod
    def parse(cls, raw_bytes):
        """
        """
        self.header, size = self.unpack(self.fmt, raw_bytes)
        self.header = self.header.decode('ascii')
        pages, size = self.unpack(Page.fmt, raw_bytes, offset=size)
        for page in range(pages):
            self.unpack(self.fmt, raw_bytes)


    def __init__(self, header, pages):
        """
        """
        self.header = header
        self.pages = []
        self.page_lookup = {}
        for page in range(pages):
            self.page_lookup[page] = Page()


def parse(raw_bytes):
    """
    """

    offset = struct.calcsize('<43s')


    # pages = struct.iter_unpack('<I', fd)

    print("\nheader: {}\npages: {}".format(header, pages))

    #pages = read_int32_t(fd)

    return



            for line in range(lines):
                brush_type = read_int32_t(fd)
                colour = read_int32_t(fd)
                unknown = read_int32_t(fd)
                brush_size = read_float(fd)
                print("line Number: {}".format(line))


    raise ValueError("*beep*")
