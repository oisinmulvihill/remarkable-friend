# -*- coding: utf-8 -*-
"""
"""
import uuid
import json

from rmfriend.notebook import Content
from rmfriend.notebook import PageData
from rmfriend.notebook import MetaData
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


def test_new_empty_MetaData(logger):
    """Test empty MetaData creation.
    """
    empty = MetaData.new()
    assert empty.data_['deleted'] is False
    assert empty.data_['lastModified'] == ''
    assert empty.data_['metadatamodified'] is False
    assert empty.data_['modified'] is False
    assert empty.data_['parent'] == ""
    assert empty.data_['pinned'] is False
    assert empty.data_['synced'] is False
    assert empty.data_['version'] == 1
    assert empty.data_['visibleName'] == '<No Name>'

    # Tue, 27 Mar 2018 20:32:08 UTC
    # https://www.epochconverter.com/
    # epoch time in milliseconds
    empty.data_['lastModified'] = '1522182728000'

    # Special attributes:
    assert empty.name == '<No Name>'
    assert empty.version == 1
    assert empty.last_modified == '2018-03-27 20:32:08+Z'


def test_MetaData_parse(logger):
    """Test empty MetaData creation.
    """
    json_d = json.dumps({
        "deleted": False,
        "lastModified": "1520689822972",
        "metadatamodified": False,
        "modified": False,
        "parent": "",
        "pinned": False,
        "synced": True,
        "type": "DocumentType",
        "version": 3,
        "visibleName": "Om1"
    })
    meta_data = MetaData.parse(json_d)
    assert meta_data.data_['deleted'] is False
    # Saturday, March 10, 2018 1:50:22.972 PM
    # https://www.epochconverter.com/
    assert meta_data.data_['lastModified'] == '1520689822972'
    assert meta_data.data_['metadatamodified'] is False
    assert meta_data.data_['modified'] is False
    assert meta_data.data_['parent'] == ""
    assert meta_data.data_['pinned'] is False
    assert meta_data.data_['synced'] is True
    assert meta_data.data_['version'] == 3
    assert meta_data.data_['visibleName'] == 'Om1'

    # Special attributes:
    assert meta_data.name == 'Om1'
    assert meta_data.version == 3
    assert meta_data.last_modified == '2018-03-10 13:50:22+Z'


def test_new_empty_Content(logger):
    """Test empty Content creation.
    """
    empty = Content.new()
    assert empty.data_['lastOpenedPage'] == 0

    empty.data_['lastOpenedPage'] = 2

    # Special attributes:
    assert empty.last_opened_page == 2


def test_Content_parse(logger, content):
    """Test empty MetaData creation.
    """
    content_ = Content.parse(content)
    assert content_.data_['lastOpenedPage'] == 0
    # Special attributes:
    assert content_.last_opened_page == 0


def test_Notebook(logger, pagedata, lines, metadata, content):
    """Test the parsing and creation of the Notebook instance.
    """
    document_id = str(uuid.uuid4())

    notebook = Notebook.parse(
        document_id=document_id,
        page_data=pagedata,
        lines=lines,
        meta_data=metadata,
        content=content,
    )
    assert notebook.document_id == document_id

    assert len(notebook.page_data.pages) == 1
    assert notebook.page_data.pages[0] == 'Blank'

    assert len(notebook.lines.pages) == 1

    assert notebook.name == 'Om1'
    assert notebook.last_modified == '2018-03-10 13:50:22+Z'

    assert notebook.last_opened_page == 0


def test_Notebook_thumnails_and_cache(logger, triangle_notebook):
    """Test the parsing and creation of the Notebook instance.
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

    # This is empty in my example
    assert len(triangle.page_data.pages) == 0

    # There should be one page in the lines file:
    assert triangle.lines.page_count == 1
    assert len(triangle.lines.pages) == 1

    assert triangle.last_opened_page == 0
