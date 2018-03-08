# -*- coding: utf-8 -*-
"""

I'm inspired by the hard work of the following projects which worked out the
format.

 - https://github.com/reHackable/maxio

 - https://github.com/ax3l/lines-are-beautiful

 - https://plasma.ninja/blog/devices/remarkable/binary/format/2017/12/26/
    reMarkable-lines-file-format.html

"""
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


class Notebook(Base):
    """
    """
    def __init__(self, header, pages):
        """
        """
        self.file_header = header
        self.pages = pages

    @classmethod
    def parse(cls, raw_bytes):
        """
        """
        position = recover(raw_bytes)

        # Start the generator off at position 0 ready to extract the file
        # header.
        print(next(position))

        # recover the header
        file_header = FileHeader.parse(position)
        assert file_header.header == FileHeader.EXPECTED

        # Now recover all the pages contained content:
        pages = Pages.parse(position)

        notebook = Notebook(file_header, pages)

        position.close()

        return notebook
