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
    def parse(cls, number, position):
        """
        """
        return Page(number, Layers.parse(position))

    def dump_to(self, raw_bytes):
        """
        """
        # write out the total layers:
        raw_bytes += struct.pack(self.fmt, len(self.layers))

        # Now start writing the layers themselves after this:
        for layer in self.layers:
            layer.dump_to(raw_bytes)


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
    def parse(cls, position):
        """
        """
        count = position.send(cls)
        pages = [Page.parse(number, position) for number in range(count)]
        return Pages(count, pages)

    def dump_to(self, raw_bytes):
        """
        """
        # write out the total pages:
        raw_bytes += struct.pack(self.fmt, len(self.pages))

        # Now start writing the pages themselves after this:
        for page in self.pages:
            page.dump_to(raw_bytes)

