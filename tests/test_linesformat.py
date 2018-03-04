# -*- coding: utf-8 -*-
"""
"""
from rmfriend.lines.format import parse


def test_format_parsing(logger, example_lines_file):
    """
    """
    lines = parse(example_lines_file)
