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
    def parse(cls, position):
        """
        """
        return Layer(Lines.parse(position))


class Layers(Int32):
    """
    """
    def __init__(self, count, layers):
        """
        """
        self.count = count
        self.layers = layers

    @classmethod
    def parse(cls, position):
        """
        """
        count = position.send(cls)
        layers = [Layer.parse(position) for layer in range(count)]
        return Layers(count, layers)
