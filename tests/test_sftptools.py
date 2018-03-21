# -*- coding: utf-8 -*-
"""
"""
import pytest

from rmfriend.tools.sftp import SFTP


def test_raw_listing_to_notebook_listing(logger, sftp_listing):
    """Verify how the notebook detection is done.

    Not a great test, more a place holder to come back to. It doesn't always
    just show only notebooks.

    """
    results = SFTP.notebooks_from_listing(sftp_listing)
    # There are 7 notebooks in the fixture listing. The non-notebooks should
    # be ignored in the output.
    assert len(results) == 7

    expected_document_ids = [
        '04b68eba-86f5-41fc-aa5d-e38f948ea109',
        '12d97066-9881-44b6-9abc-2284855f43a1',
        '153932e3-1918-4b6c-975e-52d5395adb59',
        '15c5db23-740a-4c09-b7e0-6e30b4ae5433',
        '164a8827-755c-4fdb-adaa-55c76f873263',
        '1bcc746d-c68f-4762-b990-8b0e2a4555cc',
        '25ba1ba4-e625-499e-80b7-ac99483f232e',
    ]
    for document_id in expected_document_ids:
        assert document_id in results
        assert 'metadata' in results[document_id]
        assert 'content' in results[document_id]
