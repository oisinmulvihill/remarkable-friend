# -*- coding: utf-8 -*-
"""
"""
import pytest

from rmfriend import exceptions
from rmfriend.notebook import Notebook
from rmfriend.notebookops import NotebookOPS


def test_new_notebook_from_pages(logger, triangle_notebook):
    """
    """
    document_id = '0e7143f2-e82d-4402-8eb5-39811ddbb936'
    triangle = Notebook.parse(
        document_id=triangle_notebook['document_id'],
        page_data=triangle_notebook['pagedata'],
        lines=triangle_notebook['lines'],
        meta_data=triangle_notebook['metadata'],
        content=triangle_notebook['content'],
        thumbnails=triangle_notebook['thumbnails'],
        cache=triangle_notebook['cache'],
    )
    assert triangle.document_id == document_id
    assert triangle.name == 'triangle'
    assert triangle.last_modified == '2018-03-10 13:50:22+Z'

    # Attempting to copy pages that don't exist in the source should be caught:
    with pytest.raises(exceptions.PageNotFoundError):
        NotebookOPS.new_from_pages(triangle, pages=[1])

    with pytest.raises(exceptions.PageNotFoundError):
        NotebookOPS.new_from_pages(triangle, pages=[0, 1])

    # Create a new book from the only page in triangle
    new_book = NotebookOPS.new_from_pages(triangle, pages=[0])
    assert new_book.document_id != triangle.document_id
    assert len(new_book.page_data.pages) == 0
    assert len(new_book.lines.pages) == 1
    assert new_book.name == '<No Name>'
    assert new_book.last_modified == ''
    assert new_book.last_opened_page == 0
