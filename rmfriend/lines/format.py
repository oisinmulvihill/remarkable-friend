# -*- coding: utf-8 -*-
"""

Parse the lines format.


Using inspiration from

 - https://github.com/ax3l/lines-are-beautiful

 - https://plasma.ninja/blog/devices/remarkable/binary/format/2017/12/26/
    reMarkable-lines-file-format.html


"""
import logging

from struct import pack


def get_log(e=None):
    return logging.getLogger("{0}.{1}".format(__name__, e) if e else __name__)


def parse(lines):
    """
    """
    log = get_log('parse')

    # The first 43 bytes should be:
    #
    #   b'reMarkable lines with selections and layers'
    #
    header_line = lines[:43]

    raise ValueError("*beep*")
