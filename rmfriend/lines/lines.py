# -*- coding: utf-8 -*-
"""
"""
from rmfriend.lines.base import Int32
from rmfriend.lines.base import Float


class X(Float):
    """
    """


class Y(Float):
    """
    """


class Pressure(Float):
    """
    """


class RotX(Float):
    """
    """


class RotY(Float):
    """
    """


class Point(Float):
    """An individual point on a line.
    """
    def __init__(self, x, y, pressure, rot_x, rot_y):
        """
        """
        self.x = x
        self.y = y
        self.pressure = pressure
        self.rot_x = rot_x
        self.rot_y = rot_y

    @classmethod
    def parse(cls, position):
        """
        """
        x = X.parse(position).value
        y = Y.parse(position).value
        pressure = Pressure.parse(position).value
        rot_x = RotX.parse(position).value
        rot_y = RotY.parse(position).value

        return Point(x, y, pressure, rot_x, rot_y)


class Points(Int32):
    """
    """
    def __init__(self, count, points):
        """
        """
        self.count = count
        self.points = points

    @classmethod
    def parse(cls, position):
        """
        """
        count = position.send(cls)
        points = [Point.parse(position) for point in range(count)]
        return Points(count, points)


class BrushBaseSize(Float):
    """Handle the parsing of the base brush sizes and handy string
    representation conversion.

    """
    BASE_SIZE = {
        1.875: 'small',
        2.0: 'medium',
        2.125: 'large',
    }

    REVERSE = {value: key for key, value in BASE_SIZE.items()}

    def __init__(self, value):
        """
        """
        self.value = value
        self.name = self.BASE_SIZE.get(value, 'unknown')

    def __str__(self):
        return u"{}: {}".format(self.name, self.value)


class LineAttribute1(Int32):
    """Don't know what this is used for."""
    def __init__(self, value):
        """
        """
        self.value = value


class Colour(Int32):
    """Represents the colours on the reMarkable being grayscale there aren't
    that many.

    """
    COLOURS = {0: 'black', 1: 'grey', 2: 'white'}

    REVERSE = {value: key for key, value in COLOURS.items()}

    def __init__(self, value):
        """
        """
        self.value = value
        self.name = self.COLOURS.get(value, 'unknown')

    def __str__(self):
        return u"{}: {}".format(self.name, self.value)


class BrushType(Int32):
    """Represents the differnt brush tools present on the reMarkable.
    """
    BRUSH_TYPES = {
        0: 'pen',
        1: 'pen2',
        2: 'fine_liner',
        3: 'marker',
        4: 'fine_liner2',
        5: 'highlighter',
        6: 'eraser',
        7: 'pencil',
        8: 'erase_area',
    }

    REVERSE = {value: key for key, value in BRUSH_TYPES.items()}

    def __init__(self, brush_type):
        """
        """
        self.value = brush_type
        self.name = self.BRUSH_TYPES.get(brush_type, 'unknown')

    def __str__(self):
        return u"{}: {}".format(self.name, self.value)


class Line(Int32):
    """
    """
    def __init__(
        self, brush_type, colour, line_attribute1, brush_base_size, points
    ):
        """
        """
        self.brush_type = brush_type
        self.colour = colour
        self.line_attribute1 = line_attribute1
        self.brush_base_size = brush_base_size
        self.points = points

    @classmethod
    def parse(cls, position):
        """
        """
        brush_type = BrushType.parse(position)
        colour = Colour.parse(position)
        line_attribute1 = LineAttribute1.parse(position)
        brush_base_size = BrushBaseSize.parse(position)
        points = Points.parse(position)
        return Line(
            brush_type, colour, line_attribute1, brush_base_size, points
        )


class Lines(Int32):
    """
    """
    def __init__(self, count, lines):
        """
        """
        self.count = count
        self.lines = lines

    @classmethod
    def parse(cls, position):
        """
        """
        count = position.send(cls)
        lines = [Line.parse(position) for line in range(count)]
        return Lines(count, lines)
