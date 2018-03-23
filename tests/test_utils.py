# -*- coding: utf-8 -*-
"""
"""
from pathlib import Path

import pytest

from rmfriend.utils import filename_from
from rmfriend.utils import document_id_and_extension


@pytest.mark.parametrize(
    ('filename', 'doc_id', 'extension', 'path'),
    [
        (
            'adb42abd-44cd-4106-b40a-d716869a61d7.pagedata',
            'adb42abd-44cd-4106-b40a-d716869a61d7',
            'pagedata',
            None
        ),
        (
            'adb42abd-44cd-4106-b40a-d716869a61d7.metadata',
            'adb42abd-44cd-4106-b40a-d716869a61d7',
            'metadata',
            None
        ),
        (
            '17c49f76-a10c-4441-80aa-9123e22788d1.metadata',
            '17c49f76-a10c-4441-80aa-9123e22788d1',
            'metadata',
            None
        ),
        (
            '8fe35644-59a4-48df-961e-3f125ba304e4.lines',
            '8fe35644-59a4-48df-961e-3f125ba304e4',
            'lines',
            '/a/b/c'
        ),
        (
            '477b27a3-96e1-4d2b-9933-291b4e8db2d5.content',
            '477b27a3-96e1-4d2b-9933-291b4e8db2d5',
            'content',
            '/a/b/c'
        ),
        (
            'f53b409f-fe47-451a-a53a-733ddcefcc7c.lines.backup',
            'f53b409f-fe47-451a-a53a-733ddcefcc7c',
            'backup',
            None
        ),
        (
            'c2efcaa6-680a-423f-b743-a4c1053e9bde.thumbnails',
            'c2efcaa6-680a-423f-b743-a4c1053e9bde',
            'thumbnails',
            None
        ),
        (
            '25ba1ba4-e625-499e-80b7-ac99483f232e.cache',
            '25ba1ba4-e625-499e-80b7-ac99483f232e',
            'cache',
            None
        ),
        (
            'e73b813b-a1e8-4a24-8a4f-316b1b86c8c3.highlights',
            'e73b813b-a1e8-4a24-8a4f-316b1b86c8c3',
            'highlights',
            None
        ),
        (
            '25ba1ba4-e625-499e-80b7-ac99483f232e',
            '25ba1ba4-e625-499e-80b7-ac99483f232e',
            '',
            None
        ),
    ]
)
def test_document_id_and_extension(logger, filename, doc_id, extension, path):
    """Verify recover of the document id and extension from the raw filename.
    """
    result = document_id_and_extension(filename)
    assert result == (doc_id, extension)

    # test the file reconstruction with optional path:
    result = filename_from(doc_id, extension, path=path)
    if path:
        assert result == str(Path(path) / filename)

    else:
        assert result == filename
