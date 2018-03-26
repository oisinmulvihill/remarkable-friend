# -*- coding: utf-8 -*-
"""
"""
from rmfriend.export.svg import Export
from rmfriend.lines.notebooklines import NotebookLines


def test_export_lines_to_svg(logger, example_lines_file):
    """
    """
    notebook = NotebookLines.parse(example_lines_file)
    assert notebook.pages.count == 1

    for svg_file in Export.convert(notebook):
        pass
        # svg_file.save()
