# -*- coding: utf-8 -*-
"""
"""
from rmfriend.lines.base import Int32
from rmfriend.lines.lines import Lines


class Layer(Int32):
    """
    """

    def __init__(self, lines):
        """
        """
        self.lines = lines

    @classmethod
    def load(cls, position):
        """
        """
        return Layer(Lines.load(position))

    def dump(self):
        """
        """
        return self.lines.dump()


class Layers(Int32):
    """
    """

    def __init__(self, count, layers):
        """
        """
        self.count = count
        self.layers = layers

    @classmethod
    def load(cls, position):
        """
        """
        count = position.send(cls)
        layers = [Layer.load(position) for layer in range(count)]
        return Layers(count, layers)

    def dump(self):
        """
        """
        raw_bytes = b''

        count = Int32(len(self.layers))
        raw_bytes += count.dump()
        for layer in self.layers:
            raw_bytes += layer.dump()

        return raw_bytes
