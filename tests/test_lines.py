# -*- coding: utf-8 -*-
"""
"""
import struct

import pytest

from rmfriend.lines import lines
from rmfriend.lines.base import Int32
from rmfriend.lines.base import Float
from rmfriend.lines.base import recover


@pytest.mark.parametrize(
    ('class_', 'raw_bytes', 'expected'),
    [
        (lines.X, struct.pack(lines.X.fmt, 12.341), 12.341),
        (lines.Y, struct.pack(lines.Y.fmt, 107.3), 107.3),
        (lines.Pressure, struct.pack(lines.Pressure.fmt, 0.351), 0.351),
        (lines.RotX, struct.pack(lines.RotX.fmt, 0.03), 0.03),
        (lines.RotY, struct.pack(lines.RotY.fmt, 0.216), 0.216),
    ]
)
def test_primitives(logger, class_, raw_bytes, expected):
    """Verify basic conversion of the classes used by lines.Point
    """
    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    result = class_.load(position)

    if issubclass(class_, Float):
        assert round(result.value, 3) == expected

    else:
        assert result.value == expected


def test_point_parse(logger):
    """Verify Point.load from raw bytes.
    """
    raw_bytes = b''
    point_data_fragment = [
        (struct.pack(lines.X.fmt, 12.341), 12.341),
        (struct.pack(lines.Y.fmt, 107.301), 107.301),
        (struct.pack(lines.Pressure.fmt, 0.351), 0.351),
        (struct.pack(lines.RotX.fmt, 0.03), 0.03),
        (struct.pack(lines.RotY.fmt, 0.216), 0.216),
    ]
    for data in point_data_fragment:
        raw_bytes += data[0]

    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    result = lines.Point.load(position)
    assert round(result.x, 3) == 12.341
    assert round(result.y, 3) == 107.301
    assert round(result.pressure, 3) == 0.351
    assert round(result.rot_x, 3) == 0.03
    assert round(result.rot_y, 3) == 0.216


def test_points_class_parse(logger):
    """Verify Points class.load which creates individual Point instances from
    raw bytes.

    """
    raw_bytes = b''
    point_data_fragment = [
        # one point:
        (struct.pack(lines.Points.fmt, 1), 1),
        # the single point's data:
        (struct.pack(lines.X.fmt, 12.341), 12.341),
        (struct.pack(lines.Y.fmt, 107.301), 107.301),
        (struct.pack(lines.Pressure.fmt, 0.351), 0.351),
        (struct.pack(lines.RotX.fmt, 0.03), 0.03),
        (struct.pack(lines.RotY.fmt, 0.216), 0.216),
    ]
    for data in point_data_fragment:
        raw_bytes += data[0]

    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    result = lines.Points.load(position)
    assert result.count == 1
    assert len(result.points) == 1
    result = result.points[0]
    assert round(result.x, 3) == 12.341
    assert round(result.y, 3) == 107.301
    assert round(result.pressure, 3) == 0.351
    assert round(result.rot_x, 3) == 0.03
    assert round(result.rot_y, 3) == 0.216


@pytest.mark.parametrize(
    ('raw_bytes', 'value', 'name'),
    [
        (struct.pack(Float.fmt, 1.875), 1.875, 'small'),
        (struct.pack(Float.fmt, 2.0), 2.0, 'medium'),
        (struct.pack(Float.fmt, 2.125), 2.125, 'large'),
    ]
)
def test_line_attribute_brush_base_size(logger, raw_bytes, value, name):
    """Verify how lines.BrushBaseSize handles parsing.
    """
    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    result = lines.BrushBaseSize.load(position)
    assert result.value == value
    assert result.name == name


@pytest.mark.parametrize(
    ('raw_bytes', 'value', 'name'),
    [
        (struct.pack(Int32.fmt, 0), 0, 'black'),
        (struct.pack(Int32.fmt, 1), 1, 'grey'),
        (struct.pack(Int32.fmt, 2), 2, 'white'),
        (struct.pack(Int32.fmt, 12), 12, 'unknown'),
    ]
)
def test_line_attribute_colour(logger, raw_bytes, value, name):
    """Verify how lines.BrushBaseSize handles parsing.
    """
    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    result = lines.Colour.load(position)
    assert result.value == value
    assert result.name == name


def test_line_attribute_lineattribute1(logger):
    """Verify how lines.LineAttribute1 handles parsing.
    """
    raw_bytes = struct.pack(Int32.fmt, 0)

    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    result = lines.LineAttribute1.load(position)
    assert result.value == 0


@pytest.mark.parametrize(
    ('raw_bytes', 'value', 'name'),
    [
        (struct.pack(Int32.fmt, 0), 0, 'pen'),
        (struct.pack(Int32.fmt, 1), 1, 'pen2'),
        (struct.pack(Int32.fmt, 2), 2, 'fine_liner'),
        (struct.pack(Int32.fmt, 3), 3, 'marker'),
        (struct.pack(Int32.fmt, 4), 4, 'fine_liner2'),
        (struct.pack(Int32.fmt, 5), 5, 'highlighter'),
        (struct.pack(Int32.fmt, 6), 6, 'eraser'),
        (struct.pack(Int32.fmt, 7), 7, 'pencil'),
        (struct.pack(Int32.fmt, 8), 8, 'erase_area'),
        (struct.pack(Int32.fmt, 12), 12, 'unknown'),
    ]
)
def test_line_attribute_brush_type(logger, raw_bytes, value, name):
    """Verify how lines.BrushBaseSize handles parsing.
    """
    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    result = lines.BrushType.load(position)
    assert result.value == value
    assert result.name == name


def test_line_class_parse(logger):
    """Verify Line class.load from raw bytes.

    """
    raw_bytes = b''
    point_data_fragment = [
        # line:
        #
        # brush type
        (
            struct.pack(lines.BrushType.fmt, lines.BrushType.REVERSE['pen']),
            lines.BrushType.REVERSE['pen'],
        ),
        # colour
        (
            struct.pack(lines.Colour.fmt, lines.Colour.REVERSE['black']),
            lines.Colour.REVERSE['black']
        ),
        # magical unknown line attribute 1
        (
            struct.pack(lines.LineAttribute1.fmt, 0),
            0
        ),
        # base brush size
        (
            struct.pack(
                lines.BrushBaseSize.fmt, lines.BrushBaseSize.REVERSE['small']
            ),
            lines.BrushBaseSize.REVERSE['small']
        ),
        # one point:
        (struct.pack(lines.Points.fmt, 1), 1),
        # the single point's data:
        (struct.pack(lines.X.fmt, 12.341), 12.341),
        (struct.pack(lines.Y.fmt, 107.301), 107.301),
        (struct.pack(lines.Pressure.fmt, 0.351), 0.351),
        (struct.pack(lines.RotX.fmt, 0.03), 0.03),
        (struct.pack(lines.RotY.fmt, 0.216), 0.216),
    ]
    for data in point_data_fragment:
        raw_bytes += data[0]

    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    result = lines.Line.load(position)
    assert result.brush_type.name == 'pen'
    assert result.colour.name == 'black'
    assert result.line_attribute1.value == 0
    assert result.brush_base_size.name == 'small'
    assert result.points.count == 1
    result = result.points.points[0]
    assert round(result.x, 3) == 12.341
    assert round(result.y, 3) == 107.301
    assert round(result.pressure, 3) == 0.351
    assert round(result.rot_x, 3) == 0.03
    assert round(result.rot_y, 3) == 0.216


def test_lines_class_parse(logger):
    """Verify Lines class.load which creates an individual line instances from
    raw bytes.

    """
    raw_bytes = b''
    point_data_fragment = [
        # Only 1 line in this "data"
        (
            struct.pack(lines.Lines.fmt, 1),
            1,
        ),
        # line:
        #
        # brush type
        (
            struct.pack(lines.BrushType.fmt, lines.BrushType.REVERSE['pen']),
            lines.BrushType.REVERSE['pen'],
        ),
        # colour
        (
            struct.pack(lines.Colour.fmt, lines.Colour.REVERSE['black']),
            lines.Colour.REVERSE['black']
        ),
        # magical unknown line attribute 1
        (
            struct.pack(lines.LineAttribute1.fmt, 0),
            0
        ),
        # base brush size
        (
            struct.pack(
                lines.BrushBaseSize.fmt, lines.BrushBaseSize.REVERSE['small']
            ),
            lines.BrushBaseSize.REVERSE['small']
        ),
        # one point:
        (struct.pack(lines.Points.fmt, 1), 1),
        # the single point's data:
        (struct.pack(lines.X.fmt, 12.341), 12.341),
        (struct.pack(lines.Y.fmt, 107.301), 107.301),
        (struct.pack(lines.Pressure.fmt, 0.351), 0.351),
        (struct.pack(lines.RotX.fmt, 0.03), 0.03),
        (struct.pack(lines.RotY.fmt, 0.216), 0.216),
    ]
    for data in point_data_fragment:
        raw_bytes += data[0]

    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    result = lines.Lines.load(position)
    assert result.count == 1
    assert len(result.lines) == 1
    result = result.lines[0]
    assert result.brush_type.name == 'pen'
    assert result.colour.name == 'black'
    assert result.line_attribute1.value == 0
    assert result.brush_base_size.name == 'small'
    assert result.points.count == 1
    result = result.points.points[0]
    assert round(result.x, 3) == 12.341
    assert round(result.y, 3) == 107.301
    assert round(result.pressure, 3) == 0.351
    assert round(result.rot_x, 3) == 0.03
    assert round(result.rot_y, 3) == 0.216
