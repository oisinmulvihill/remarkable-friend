# -*- coding: utf-8 -*-
"""
"""
import svgwrite

from rmfriend.export.base import Base
from rmfriend.export.base import grouper


class Export(Base):
    """
    """
    @classmethod
    def convert(cls, lines, output_prefix='test-svg'):
        """Convert the notebook lines into SVG images
        """
        drawings = []

        for page in lines.pages:
            file_name = cls.page_to_filename(
                output_prefix, lines.page_count, page.number, 'svg'
            )

            dwg = svgwrite.Drawing(
                file_name, (cls.DEFAULT_WIDTH, cls.DEFAULT_HEIGHT)
            )
            for layer in page.layers.layers:
                for line in layer.lines.lines:
                    width = line.brush_base_size.value
                    last_point = None
                    # Create polylines with blocks of points inside to reduce
                    # down the size of the SVG file.
                    for points in grouper(line.points.points, 10, 'X'):
                        # I will need to work out the tool properties here in
                        # a similar fashion to Maxio's rM2SVG tool.
                        segment_width = width
                        segment_opacity = 1
                        extra = {
                            "style": (
                                "fill:none;"
                                "stroke:{};"
                                "stroke-width:{:.3f};"
                                "opacity:{}"
                            ).format("black", segment_width, segment_opacity)
                        }
                        line_points = [p.x_y for p in points if p != 'X']
                        end_point = line_points[-1]
                        if last_point is not None:
                            # Connect this to the last polyline to avoid gaps.
                            line_points.insert(0, last_point)
                        dwg.add(dwg.polyline(line_points, **extra))
                        last_point = end_point

            drawings.append({'filename': file_name, 'image': dwg})

        return drawings
