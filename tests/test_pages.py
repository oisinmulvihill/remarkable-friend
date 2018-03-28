# -*- coding: utf-8 -*-
"""
"""
from rmfriend.lines.base import recover
from rmfriend.lines.pages import Page
from rmfriend.lines.pages import Pages
from rmfriend.lines.layers import Layers


def test_page_and_pages_dump_and_load(logger):
    """Test the dump and loading of pages-page-empty layers instance.
    """
    page = Page(0, Layers(0, []))
    assert page.number == 0
    assert page.layers.count == 0
    pages = Pages(1, [page])
    assert pages.count == 1
    assert len(pages.pages) == 1
    assert pages.pages == [page]

    raw_bytes = pages.dump()
    position = recover(raw_bytes)
    next(position)

    result = Pages.load(position)
    assert result.count == 1
    assert len(result.pages) == 1
    page = result.pages[0]
    assert page.number == 0
    assert page.layers.count == 0
