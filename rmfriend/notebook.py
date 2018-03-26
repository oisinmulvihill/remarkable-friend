# -*- coding: utf-8 -*-
"""
"""
import uuid

from rmfriend.pagedata import PageData
from rmfriend.metadata import MetaData
from rmfriend.lines.notebooklines import NotebookLines


class Notebook(object):
    """This repesents a 'Notebook' on the reMarkable device.

    On reMarkable a notebook is actually a collections of files. Each file that
    makes up a notebook uses the same UUID (Universally Unique Identifer). The
    extension then determines what it does.

    From observation I've discovered a notebook will have the following file
    extensions and meanings:

      - 'pagedata' this contains the template used on each page in the
    notebook. This is handled by the PageData class.

      - 'lines' this contains the binary drawing information. It represents
    the notebooks content. The NotebookLines class handles this content.

      - 'lines.backup' I don't do anything with this at the moment.

      - 'metadata' this contains extra information about the lines file. For
    example its visible name. The MetaData class handles this content.

      - 'content' this contains information to aid the UI relating. For example
    its the last opened page and pen type used. The Content class handles this.

      - 'content' this contains information to aid the UI relating. For example
      its the last opened page and pen type used. The Content class handles
      this.

    Along with these files there are also two directories which have the same
    UUID with the 'extension':

      - 'thumbnails' this directory contains a small jpeg image of each page.
      For example: '0.jpg, 1.jpg,  3.jpg, etc'

      - 'cache' this directory contains a a full sized  each page. For example:
      '0.jpg, 1.jpg,  3.jpg, etc'

    """

    def __init__(self, document_id, page_data, lines, meta_data):
        """
        """
        self.document_id = document_id
        # A PageData instance:
        self.page_data = page_data
        # A NotebookLines instance:
        self.lines = lines
        # A MetaData instance:
        self.meta_data = meta_data

    @classmethod
    def parse(cls, document_id, page_data, lines, meta_data):
        """Return a Notebook for the given sections.

        :param document_id: The UUID string for this notebook.

        :param page_data: The raw page data for this notebook.

        :param meta_data: The raw meta JSON for this notebook.

        """
        return cls(
            # verify this is actually a UUID formatted string.
            document_id=str(uuid.UUID(document_id)),
            page_data=PageData.parse(page_data),
            lines=NotebookLines.parse(lines),
            meta_data=MetaData.parse(meta_data),
        )
