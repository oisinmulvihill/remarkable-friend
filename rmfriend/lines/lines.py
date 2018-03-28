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
    def load(cls, position):
        """
        """
        x = X.load(position).value
        y = Y.load(position).value
        pressure = Pressure.load(position).value
        rot_x = RotX.load(position).value
        rot_y = RotY.load(position).value

        return Point(x, y, pressure, rot_x, rot_y)

    def dump(self):
        """
        """
        raw_bytes = b''

        x = X(self.x)
        raw_bytes += x.dump()
        y = Y(self.y)
        raw_bytes += y.dump()
        pressure = Pressure(self.pressure)
        raw_bytes += pressure.dump()
        rot_x = RotX(self.rot_x)
        raw_bytes += rot_x.dump()
        rot_y = RotX(self.rot_y)
        raw_bytes += rot_y.dump()

        return raw_bytes

    @property
    def x_y(self):
        """Return a tuple of the (x, y) for convience."""
        return (self.x, self.y)

    def __str__(self):
        return u"{}: pressure={} rot_x={} rot_y={}".format(
            self.x_y, self.pressure, self.rot_x, self.rot_y
        )

    def __repr__(self):
        return str({
            "name": "Point",
            "x": self.x,
            "y": self.y,
            "pressure": self.pressure,
            "rot_x": self.rot_x,
            "rot_y": self.rot_y,
        })


class Points(Int32):
    """
    """

    def __init__(self, count, points):
        """
        """
        self.count = count
        self.points = points

    @classmethod
    def load(cls, position):
        """
        """
        count = position.send(cls)
        points = [Point.load(position) for point in range(count)]
        return Points(count, points)

    def dump(self):
        """
        """
        raw_bytes = b''

        count = Int32(len(self.points))
        raw_bytes += count.dump()
        for point in self.points:
            raw_bytes += point.dump()

        return raw_bytes


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
    """Don't know what this is used for.
    """

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
    def load(cls, position):
        """
        """
        brush_type = BrushType.load(position)
        colour = Colour.load(position)
        line_attribute1 = LineAttribute1.load(position)
        brush_base_size = BrushBaseSize.load(position)
        points = Points.load(position)
        return Line(
            brush_type, colour, line_attribute1, brush_base_size, points
        )

    def dump(self):
        """
        """
        raw_bytes = b''

        raw_bytes += self.brush_type.dump()
        raw_bytes += self.colour.dump()
        raw_bytes += self.line_attribute1.dump()
        raw_bytes += self.brush_base_size.dump()
        raw_bytes += self.points.dump()

        return raw_bytes

    def __str__(self):
        return u"brush={} colour={} base_size={} points={}".format(
            self.brush_type.name,
            self.colour.name,
            self.brush_base_size.name,
            self.points.count,
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
    def load(cls, position):
        """
        """
        count = position.send(cls)
        lines = [Line.load(position) for line in range(count)]
        return Lines(count, lines)

    def dump(self):
        """
        """
        raw_bytes = b''

        count = Int32(len(self.lines))
        raw_bytes += count.dump()
        for line in self.lines:
            raw_bytes += line.dump()

        return raw_bytes
