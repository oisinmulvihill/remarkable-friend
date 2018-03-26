# -*- coding: utf-8 -*-
"""
"""
import struct

from rmfriend.lines.base import recover
from rmfriend.lines.notebooklines import FileHeader
from rmfriend.lines.notebooklines import NotebookLines


def test_file_header_parsing(logger):
    """
    """
    expected = 'reMarkable lines with selections and layers'
    raw_bytes = struct.pack('<43s', expected.encode('ascii'))

    position = recover(raw_bytes)
    next(position)

    file_header = FileHeader.parse(position)

    assert file_header.header == expected


def test_format_parsing(logger, example_lines_file):
    """
    """
    notebook = NotebookLines.parse(example_lines_file)

    assert notebook.pages.count == 1