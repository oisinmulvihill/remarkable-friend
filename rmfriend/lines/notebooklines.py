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

    def dump_to(self, raw_bytes):
        """
        """
        raw_bytes += struct.pack(self.fmt, self.header.encode())


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
    def parse(cls, raw_bytes):
        """
        """
        position = recover(raw_bytes)

        # Start the generator off at position 0 ready to extract the file
        # header.
        next(position)

        # recover the header
        file_header = FileHeader.parse(position)
        assert file_header.header == FileHeader.EXPECTED

        # Now recover all the pages contained content:
        pages = Pages.parse(position)

        notebook = NotebookLines(file_header, pages)

        position.close()

        return notebook

    def dump(self):
        """
        """
        raw_bytes = b''

        self.header.dump_to(raw_bytes)
        self.pages_.dump_to(raw_bytes)

        return raw_bytes
