# -*- coding: utf-8 -*-
"""
"""
import pytest

from rmfriend.export.svg import Export
from rmfriend.lines.notebook import Notebook


def test_export_lines_to_svg(logger, example_lines_file):
    """
    """
    notebook = Notebook.parse(example_lines_file)
    assert notebook.pages.count == 1

    # for svg_file in Export.convert(notebook):
    #     svg_file.save()
