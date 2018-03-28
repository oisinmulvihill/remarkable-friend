# -*- coding: utf-8 -*-
"""
"""
import struct

from rmfriend.lines.base import Int32
from rmfriend.lines.layers import Layers


class Page(Int32):
    """
    """

    def __init__(self, number, layers):
        """
        """
        self.number = number
        self.layers = layers

    @classmethod
    def load(cls, number, position):
        """
        """
        return Page(number, Layers.load(position))

    def dump(self):
        """
        """
        raw_bytes = b''

        # Now layers will take care of dump individual layer instances:
        raw_bytes += self.layers.dump()

        return raw_bytes


class Pages(Int32):
    """
    """

    def __init__(self, count, pages):
        """
        """
        self.count = count
        self.pages = pages

    @classmethod
    def new(cls, pages=[]):
        """Return a new instance with the given Page instances."""
        return Pages(len(pages), pages)

    @classmethod
    def load(cls, position):
        """
        """
        count = position.send(cls)
        pages = [Page.load(number, position) for number in range(count)]
        return Pages(count, pages)

    def dump(self):
        """
        """
        raw_bytes = b''

        # write out the total pages:
        raw_bytes += struct.pack(self.fmt, len(self.pages))

        # Now start writing the pages themselves after this:
        for page in self.pages:
            raw_bytes += page.dump()

        return raw_bytes
