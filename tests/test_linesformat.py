# -*- coding: utf-8 -*-
"""
"""
from rmfriend.lines import format


def test_format_parsing(logger, example_lines_file):
    """
    """
    lines = format.parse(example_lines_file)
