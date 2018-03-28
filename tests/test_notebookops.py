# -*- coding: utf-8 -*-
"""
"""
import pytest

from rmfriend import exceptions
from rmfriend.notebook import Notebook
from rmfriend.notebookops import NotebookOPS


def test_new_notebook_from_pages(logger, triangle_notebook):
    """Verify the creation of a new notebook from pages of another notebook.

    This will also dump out and load back in the new notebook to see it was
    generated correctly and could be uploaded to the reMarkable.

    """
    document_id = '0e7143f2-e82d-4402-8eb5-39811ddbb936'
    triangle = Notebook.load(
        document_id=triangle_notebook['document_id'],
        pagedata=triangle_notebook['pagedata'],
        lines=triangle_notebook['lines'],
        metadata=triangle_notebook['metadata'],
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
    assert len(new_book.pagedata.pages) == 0
    assert len(new_book.lines.pages) == 1
    assert new_book.name == 'No Name'
    assert new_book.last_modified == ''
    assert new_book.last_opened_page == 0

    data = new_book.dump()

    triangle2 = Notebook.load(
        document_id=data['document_id'],
        pagedata=data['pagedata'],
        lines=data['lines'],
        metadata=data['metadata'],
        content=data['content'],
        thumbnails=data['thumbnails'],
        cache=data['cache'],
    )
    assert len(triangle2.pagedata.pages) == 0
    assert len(triangle2.lines.pages) == 1
    assert triangle2.name == 'No Name'
    assert triangle2.last_modified == ''
    assert triangle2.last_opened_page == 0
