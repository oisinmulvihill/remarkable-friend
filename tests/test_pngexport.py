# -*- coding: utf-8 -*-
"""
"""
from rmfriend.export.png import Export
from rmfriend.lines.notebooklines import NotebookLines


def test_export_lines_to_png(logger, lines):
    """
    """
    notebook_lines = NotebookLines.load(lines)
    assert notebook_lines.page_count == 1
    for png_file in Export.convert(notebook_lines):
        pass
        # png_file.save()
