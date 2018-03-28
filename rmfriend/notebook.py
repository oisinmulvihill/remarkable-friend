# -*- coding: utf-8 -*-
"""
"""
import uuid
import pathlib

from rmfriend.content import Content
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

      - 'highlights': I don't know what to do with this just yet.

    """

    def __init__(
        self, document_id, pagedata, lines, metadata, content, thumbnails=[],
        cache=[]
    ):
        """
        """
        self.document_id = document_id
        # A PageData instance:
        self.pagedata = pagedata
        # A NotebookLines instance:
        self.lines = lines
        # A MetaData instance:
        self.metadata = metadata
        # A Content instance:
        self.content = content
        # Directories
        self.thumbnails = thumbnails
        self.cache = cache

    @property
    def name(self):
        """Return the meta data's name property."""
        return self.metadata.name

    @property
    def last_modified(self):
        """Return the meta data's last modified property."""
        return self.metadata.last_modified

    @property
    def last_opened_page(self):
        """Return the content's last opened page property."""
        return self.content.last_opened_page

    @property
    def page_count(self):
        """Return the lines's file count of pages."""
        return self.lines.page_count()

    @property
    def version(self):
        """Return the metadata's version."""
        return self.metadata.version

    @classmethod
    def load(
        cls, document_id, pagedata, lines, metadata, content, thumbnails=[],
        cache=[]
    ):
        """Return a Notebook for the given sections.

        :param document_id: The UUID string for this notebook.

        :param pagedata: The raw page data for this notebook.

        :param metadata: The raw meta JSON for this notebook.

        :param content: The raw content JSON for this notebook.

        :param thumbnails: A list of file present in the thumbnails directory.

        :param cache: A list of files present in the cache directory.

        """
        return cls(
            # verify this is actually a UUID formatted string.
            document_id=str(uuid.UUID(document_id)),
            pagedata=PageData.load(pagedata),
            lines=NotebookLines.load(lines),
            metadata=MetaData.load(metadata),
            content=Content.load(content),
            thumbnails=thumbnails,
            cache=cache,
        )

    def dump(self):
        """Return a dict of and the raw versions of each extension part."""
        return dict(
            document_id=self.document_id,
            pagedata=self.pagedata.dump(),
            lines=self.lines.dump(),
            metadata=self.metadata.dump(),
            content=self.content.dump(),
            thumbnails=self.thumbnails,
            cache=self.cache,
        )

    def write(self, destination_path):
        """Write out the notebook to disk.

        :param destination_path: Where to write the notebook to.

        The destination_path will contain the notebook files:

            <document_id>.(lines|metadata|content|pagedata)

        """
        destination = pathlib.Path(destination_path)

        data = self.dump()

        document_id = data['document_id']

        for key in data:
            if key in ('document_id', 'thumbnails', 'cache'):
                # Ignore these. Thumnails and cache will be generated by
                # reMarkable. Let it do the work.
                continue

            filename = destination / "{}.{}".format(document_id, key)
            if key == 'lines':
                filename.write_bytes(data[key])
            else:
                filename.write_bytes(data[key].encode('utf-8'))
