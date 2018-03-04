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


binary_format = [
    {"name": "header", "bytes": 43},
    {"name": "pages", "bytes": 4},
]


def read_int32_t(stream):
    return int.from_bytes(stream.read(4), byteorder='little')

def read_int32_t(stream):
    return int.from_bytes(stream.read(4), byteorder='little')


def parse(lines):
    """
    """
    fd = io.BytesIO(lines)
    #header = fd.read(43).decode('ascii')

    expected = b'reMarkable lines with selections and layers'
    header, pages = struct.unpack_from('<{}sI'.format(len(expected)), lines)

    # pages = struct.iter_unpack('<I', fd)

    print("\nheader: {}\npages: {}".format(header, pages))

    #pages = read_int32_t(fd)

    return

    for page in range(pages):
        print("Page Number: {}".format(page))
        layers = read_int32_t(fd)
        print("Number of layers: {}".format(layers))

        for layer in range(layers):
            print("Layer Number: {}".format(layer))
            lines = read_int32_t(fd)
            print("Number of lines: {}".format(lines))

            for line in range(lines):
                brush_type = read_int32_t(fd)
                colour = read_int32_t(fd)
                unknown = read_int32_t(fd)
                brush_size = read_float(fd)
                print("line Number: {}".format(line))


    raise ValueError("*beep*")
