# -*- coding: utf-8 -*-
"""
"""
import struct

from rmfriend.lines.base import Base
from rmfriend.lines.base import Int32
from rmfriend.lines.base import Float
from rmfriend.lines.base import recover


def test_recover_generator(logger):
    """Verify the behaviour of the raw bytes parsing generator.
    """
    class Char(object):
        fmt = 'c'

    raw_bytes = b'0123456789'

    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)

    # Start the generator ready for reading in and converting bytes:
    data = next(position)
    assert data == ''

    # Parse out the characters
    for i in range(10):
        # recorver the next character
        data = position.send(Char)
        # verify it is correct:
        assert int(data) == i


def test_recover_base(logger):
    """Verify the behaviour Int32 class used in parsing.
    """
    class AnotherInt32(Base):
        fmt = '<I'

        def __init__(self, value):
            self.value = value

    raw_bytes = struct.pack(AnotherInt32.fmt, 9009)

    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    assert AnotherInt32.parse(position).value == 9009


def test_recover_int32(logger):
    """Verify the behaviour Int32 class used in parsing.
    """
    raw_bytes = struct.pack('<I', 1001)

    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    assert Int32.parse(position).value == 1001


def test_recover_float(logger):
    """Verify the behaviour Float class used in parsing.
    """
    raw_bytes = struct.pack('<f', 3.141)

    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    assert round(Float.parse(position).value, 3) == 3.141
