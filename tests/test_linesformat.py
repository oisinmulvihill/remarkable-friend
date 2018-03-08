# -*- coding: utf-8 -*-
"""
"""
from rmfriend.lines.notebook import Notebook


def test_format_parsing(logger, example_lines_file):
    """
    """
    notebook = Notebook.parse(example_lines_file)

    print (notebook)

    raise ValueError('*beep*')
