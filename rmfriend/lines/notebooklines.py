# -*- coding: utf-8 -*-
"""
"""
import os
import struct

from rmfriend.lines.base import Base
from rmfriend.lines.pages import Pages
from rmfriend.lines.base import recover


class FileHeader(Base):
    """
    """
    EXPECTED = 'reMarkable lines with selections and layers'

    fmt = '<43s'

    def __init__(self, header):
        """
        """
        self.header = header.decode('ascii')

    def dump(self):
        """
        """
        return struct.pack(self.fmt, bytes(self.header.encode()))


class NotebookLines(Base):
    """
    """

    def __init__(self, header, pages):
        """
        """
        self.file_header = header
        # A Pages instance
        self.pages_ = pages

    @property
    def pages(self):
        """Return the pages from the self.pages_ (Pages instance).
        """
        return self.pages_.pages

    @property
    def page_count(self):
        """Return the pages from the self.pages_.count (Pages instance).
        """
        return self.pages_.count

    @classmethod
    def read(cls, filename):
        """
        """
        filename = os.path.expanduser(filename)
        filename = os.path.abspath(filename)

        with open(filename, 'rb') as fd:
            raw_binary = fd.read()

        return raw_binary

    @classmethod
    def new(cls, pages=[]):
        """Returns and empty NotebookLines instance."""
        return cls(
            header=FileHeader.EXPECTED,
            pages=Pages.new(pages=pages)
        )

    @classmethod
    def load(cls, raw_bytes):
        """
        """
        position = recover(raw_bytes)

        # Start the generator off at position 0 ready to extract the file
        # header.
        next(position)

        # recover the header
        file_header = FileHeader.load(position)
        assert file_header.header == FileHeader.EXPECTED

        # Now recover all the pages contained content:
        pages = Pages.load(position)

        notebook = NotebookLines(file_header, pages)

        position.close()

        return notebook

    def dump(self):
        """
        """
        raw_bytes = b''

        # Add standard header
        raw_bytes += FileHeader(self.file_header.encode('ascii')).dump()

        # Dump out the rest of the notebook lines
        raw_bytes += self.pages_.dump()

        return raw_bytes
