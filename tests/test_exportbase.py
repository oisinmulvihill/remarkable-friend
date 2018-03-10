# -*- coding: utf-8 -*-
"""
"""
import pytest

from rmfriend.export.base import Base


@pytest.mark.parametrize(
    ('base_name', 'total_pages', 'page_number', 'extension', 'expected'),
    [
        ('output', 10, 1, 'svg', 'output-01.svg'),
        ('output', 100, 1, 'png', 'output-001.png'),
        ('output', 1000, 1, 'tiff', 'output-0001.tiff'),
        ('output', 1, 1, 'jpg', 'output-01.jpg'),
    ]
)
def test_page_number_to_filename(
    base_name, total_pages, page_number, extension, expected
):
    """Verify the filename generation for pages
    """
    result = Base.page_to_filename(
        base_name, total_pages, page_number, extension
    )
    assert result == expected
