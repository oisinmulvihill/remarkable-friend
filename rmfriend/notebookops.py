# -*- coding: utf-8 -*-
"""
"""
import uuid

from rmfriend import exceptions
from rmfriend.content import Content
from rmfriend.pagedata import PageData
from rmfriend.metadata import MetaData
from rmfriend.notebook import Notebook
from rmfriend.lines.notebooklines import NotebookLines


class NotebookOPS(object):
    """
    """
    @classmethod
    def new_from_pages(cls, source, pages):
        """Return a new Notebook from the selected pages of another

        :param source: The source notebook.Notebook instance.

        :param pages: A list of page indicies to export from the source.

        If a page number is not found then exceptions.PageNotFoundError will be
        raised.

        :returns: A new notebook.Notebook with the copied pages.

        """
        found_pages = []

        # verify the pages exist in the source notebook and recover the
        # individual Page instances we can put into a new book.
        for page_number in pages:
            try:
                page = source.lines.pages[page_number]
            except IndexError:
                raise exceptions.PageNotFoundError(
                    "Page not found '{}'".format(page_number)
                )
            else:
                found_pages.append(page)

        document_id = str(uuid.uuid4())
        metadata = MetaData.new()
        pagedata = PageData.new()
        content = Content.new()
        lines = NotebookLines.new(pages=found_pages)

        return Notebook(
            document_id=document_id,
            metadata=metadata,
            pagedata=pagedata,
            content=content,
            lines=lines,
        )
