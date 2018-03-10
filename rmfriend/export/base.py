# -*- coding: utf-8 -*-
"""
"""
import math
from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Base(object):
    """
    """
    DEFAULT_WIDTH = 1404

    DEFAULT_HEIGHT = 1872

    @classmethod
    def page_to_filename(cls, base_name, total_pages, page_number, extension):
        """
        """
        # scale the padding to amount of pages 01 for total page < 10, 001 for
        # total pages < 100, etc.
        if total_pages == 1:
            pad = 1
        else:
            pad = int(round(math.log(total_pages, 10), 1))
        zero_pad = ':0{}d'.format(pad + 1)
        file_name_format = "{}-{" + zero_pad + "}.{}"
        file_name = file_name_format.format(base_name, page_number, extension)
        return file_name
