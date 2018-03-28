# -*- coding: utf-8 -*-
"""
"""
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
        if isinstance(header, bytes):
            self.header = header.decode('ascii')

        else:
            self.header = header

    def dump(self):
        """
        """
        return struct.pack(self.fmt, bytes(self.header.encode('ascii')))


class NotebookLines(Base):
    """This represents the drawing data which resides in the notebook file with
    the .lines extension.

    From what I can see the drawing data is a bit like a binary SVG. Every
    stroke and tool used is recorded in the order it happened. This means
    rendering it would need to take account of the eraser tools for example.

    """

    def __init__(self, header, pages):
        """
        """
        # A FileHeader instance
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
    def new(cls, pages=[]):
        """Returns and empty NotebookLines instance."""
        return cls(
            header=FileHeader(FileHeader.EXPECTED),
            pages=Pages.new(pages=pages)
        )

    @classmethod
    def load(cls, raw_bytes):
        """Convert the raw bytes in a NotebookLines instance.

        :param raw_bytes: A bytes string.

        The raw_bytes will usually have come from the <document_id>.lines file.

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
        """Convert this NotebookLines instance into raw_bytes.

        This could then be written to the <document_id>.lines file.

        :returns: A bytes string.

        """
        raw_bytes = b''

        # Add standard header
        raw_bytes += self.file_header.dump()

        # Dump out the rest of the notebook lines
        raw_bytes += self.pages_.dump()

        return raw_bytes
