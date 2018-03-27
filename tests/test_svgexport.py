# -*- coding: utf-8 -*-
"""
"""
from rmfriend.export.svg import Export
from rmfriend.lines.notebooklines import NotebookLines


def test_export_lines_to_svg(logger, lines):
    """
    """
    notebook_lines = NotebookLines.parse(lines)
    assert notebook_lines.page_count == 1
    for svg_file in Export.convert(notebook_lines):
        pass
        # svg_file.save()
