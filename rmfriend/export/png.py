# -*- coding: utf-8 -*-
"""
"""
from rmfriend.export.base import Base
from rmfriend.export.base import grouper


class Export(Base):
    """
    """
    BLACK = (50, 50, 50)

    @classmethod
    def convert(cls, notebook, output_prefix='test-png'):
        """Convert the notebook into SVG images
        """
        from PIL import Image, ImageDraw

        drawings = []

        for page in notebook.pages:
            file_name = cls.page_to_filename(
                output_prefix, notebook.page_count, page.number, 'png'
            )
            image = Image.new(
                'RGBA',
                (cls.DEFAULT_WIDTH, cls.DEFAULT_HEIGHT),
                (255, 255, 255, 255)
            )
            draw = ImageDraw.Draw(image)

            for layer in page.layers.layers:
                for line in layer.lines.lines:
                    if line.brush_type.name in ('eraser', 'erase_area'):
                        continue

                    last_point = None
                    for (p1, p2) in grouper(line.points.points, 2, 'X'):
                        if p1 == 'X' or p2 == 'X':
                            # end of data
                            continue

                        if last_point is not None:
                            # Connect this to the last line to avoid gaps.
                            draw.line([last_point.x_y, p2.x_y], fill=cls.BLACK)

                        draw.line([p1.x_y, p2.x_y], fill=cls.BLACK)

                        last_point = p2

            drawings.append({'filename': file_name, 'image': image})

        return drawings
