# -*- coding: utf-8 -*-
"""
"""
import struct

from rmfriend.lines import base
from rmfriend.lines.lines import X
from rmfriend.lines.lines import Y
from rmfriend.lines.lines import Pressure
from rmfriend.lines.lines import RotX
from rmfriend.lines.lines import RotY
from rmfriend.lines.lines import Line
from rmfriend.lines.lines import Point
from rmfriend.lines.lines import Points
from rmfriend.lines.base import recover
from rmfriend.lines.lines import Colour
from rmfriend.lines.lines import BrushType
from rmfriend.lines.lines import BrushBaseSize
from rmfriend.lines.lines import LineAttribute1
from rmfriend.lines.notebooklines import FileHeader
from rmfriend.lines.notebooklines import NotebookLines


def test_file_header_parsing(logger):
    """
    """
    expected = 'reMarkable lines with selections and layers'
    raw_bytes = struct.pack('<43s', expected.encode('ascii'))

    position = recover(raw_bytes)
    next(position)

    file_header = FileHeader.load(position)

    assert file_header.header == expected


def test_format_parsing(logger, lines):
    """
    """
    notebook = NotebookLines.load(lines)
    assert notebook.page_count == 1


def test_dump_fields(logger):
    """Test the raw binary packing of the primitive fields Int32 & Float.
    """
    number = base.Int32(1234)
    assert number.value == 1234
    raw_bytes = number.dump()
    assert struct.pack('<I', 1234) == raw_bytes

    number = base.Float(3.141)
    assert number.value == 3.141
    raw_bytes = number.dump()
    assert struct.pack('<f', 3.141) == raw_bytes


def test_dump_Point(logger):
    """Test the dump and load of the Point structure.
    """
    point = Point(
        x=12.341,
        y=107.301,
        pressure=0.351,
        rot_x=0.03,
        rot_y=0.216,
    )

    raw_bytes = point.dump()
    position = recover(raw_bytes)
    next(position)

    result = Point.load(position)
    assert round(result.x, 3) == 12.341
    assert round(result.y, 3) == 107.301
    assert round(result.pressure, 3) == 0.351
    assert round(result.rot_x, 3) == 0.03
    assert round(result.rot_y, 3) == 0.216


def test_dump_Points_and_Point(logger):
    """Test the dump and load of the Points which contains Point instances.
    """
    point = Point(
        x=12.341,
        y=107.301,
        pressure=0.351,
        rot_x=0.03,
        rot_y=0.216,
    )
    points = Points(1, [point])
    raw_bytes = points.dump()
    position = recover(raw_bytes)
    next(position)

    result = Points.load(position)
    assert result.count == 1
    assert len(result.points) == 1
    result = result.points[0]
    assert round(result.x, 3) == 12.341
    assert round(result.y, 3) == 107.301
    assert round(result.pressure, 3) == 0.351
    assert round(result.rot_x, 3) == 0.03
    assert round(result.rot_y, 3) == 0.216


def test_dump_lines(logger):
    """
    """
    raw_bytes = b''
    point_data_fragment = [
        # line:
        #
        # brush type
        (
            struct.pack(BrushType.fmt, BrushType.REVERSE['pen']),
            BrushType.REVERSE['pen'],
        ),
        # colour
        (
            struct.pack(Colour.fmt, Colour.REVERSE['black']),
            Colour.REVERSE['black']
        ),
        # magical unknown line attribute 1
        (
            struct.pack(LineAttribute1.fmt, 0),
            0
        ),
        # base brush size
        (
            struct.pack(
                BrushBaseSize.fmt, BrushBaseSize.REVERSE['small']
            ),
            BrushBaseSize.REVERSE['small']
        ),
        # one point:
        (struct.pack(Points.fmt, 1), 1),
        # the single point's data:
        (struct.pack(X.fmt, 12.341), 12.341),
        (struct.pack(Y.fmt, 107.301), 107.301),
        (struct.pack(Pressure.fmt, 0.351), 0.351),
        (struct.pack(RotX.fmt, 0.03), 0.03),
        (struct.pack(RotY.fmt, 0.216), 0.216),
    ]
    for data in point_data_fragment:
        raw_bytes += data[0]

    # Set up the generator with the raw bytes:
    position = recover(raw_bytes)
    data = next(position)
    assert data == ''

    raw_bytes = Line.load(position).dump()
    position = recover(raw_bytes)
    next(position)

    the_line = Line.load(position)
    assert the_line.brush_type.name == 'pen'
    assert the_line.colour.name == 'black'
    assert the_line.line_attribute1.value == 0
    assert the_line.brush_base_size.name == 'small'
    assert the_line.points.count == 1
    result = the_line.points.points[0]
    assert round(result.x, 3) == 12.341
    assert round(result.y, 3) == 107.301
    assert round(result.pressure, 3) == 0.351
    assert round(result.rot_x, 3) == 0.03
    assert round(result.rot_y, 3) == 0.216
