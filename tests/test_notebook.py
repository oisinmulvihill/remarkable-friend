# -*- coding: utf-8 -*-
"""
"""
import uuid

from rmfriend.notebook import PageData
# from rmfriend.notebook import Content
# from rmfriend.notebook import Metadata
from rmfriend.notebook import Notebook


def test_PageData(logger, pagedata):
    """Test the Pagedata class.
    """
    example_page_data = """Blank
P Lines medium
LS Grid margin large
P Grid large
    """
    page_data = PageData.parse(example_page_data)
    assert len(page_data.pages) == 4
    assert page_data.pages[0] == 'Blank'
    assert page_data.pages[1] == 'P Lines medium'
    assert page_data.pages[2] == 'LS Grid margin large'
    assert page_data.pages[3] == 'P Grid large'

    page_data = PageData.parse(pagedata)
    assert len(page_data.pages) == 1
    assert page_data.pages[0] == 'Blank'

    # Check no page data is handled OK
    page_data = PageData.parse("")
    assert page_data.pages == []
    assert len(page_data.pages) == 0

    page_data = PageData.parse(None)
    assert page_data.pages == []
    assert len(page_data.pages) == 0

    page_data = PageData.parse("\n\n\n")
    assert page_data.pages == []
    assert len(page_data.pages) == 0


def test_Pagedata(logger, pagedata):
    """Test the Pagedata class.
    """
    example_page_data = """Blank
P Lines medium
LS Grid margin large
P Grid large
    """
    page_data = PageData.parse(example_page_data)
    assert len(page_data.pages) == 4
    assert page_data.pages[0] == 'Blank'
    assert page_data.pages[1] == 'P Lines medium'
    assert page_data.pages[2] == 'LS Grid margin large'
    assert page_data.pages[3] == 'P Grid large'

    page_data = PageData.parse(pagedata)
    assert len(page_data.pages) == 1
    assert page_data.pages[0] == 'Blank'

    # Check no page data is handled OK
    page_data = PageData.parse("")
    assert page_data.pages == []
    assert len(page_data.pages) == 0

    page_data = PageData.parse(None)
    assert page_data.pages == []
    assert len(page_data.pages) == 0

    page_data = PageData.parse("\n\n\n")
    assert page_data.pages == []
    assert len(page_data.pages) == 0


def test_Notebook(logger, pagedata, lines, metadata):
    """Test the parsing and creation of the Notebook instance.
    """
    document_id = str(uuid.uuid4())

    notebook = Notebook.parse(
        document_id=document_id,
        page_data=pagedata,
        lines=lines,
        metadata=metadata,
    )
    assert notebook.document_id == document_id
    assert notebook.name == 'Om1'

    assert len(notebook.page_data.pages) == 1
    assert notebook.page_data.pages[0] == 'Blank'

    assert len(notebook.lines.pages) == 1

