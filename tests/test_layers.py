# -*- coding: utf-8 -*-
"""
"""
from rmfriend.lines.base import recover
from rmfriend.lines.lines import Lines
from rmfriend.lines.layers import Layer
from rmfriend.lines.layers import Layers


def test_layers_dump_and_load(logger):
    """Test the dump and loading of layers-layer-empty lines instance.
    """
    layer = Layer(Lines(0, []))
    assert layer.lines.count == 0
    layers = Layers(1, [layer])
    assert layers.count == 1
    assert len(layers.layers) == 1
    assert layers.layers == [layer]

    raw_bytes = layers.dump()
    position = recover(raw_bytes)
    next(position)

    result = Layers.load(position)
    assert result.count == 1
    assert len(result.layers) == 1
    layer = result.layers[0]
    assert layer.lines.count == 0
