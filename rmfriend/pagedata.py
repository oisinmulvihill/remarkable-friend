# -*- coding: utf-8 -*-
"""
"""


class PageData(object):
    """This file contains a list of templates used on each page of a notebook.

    On the reMarkable device a notebook will have a '<UUID>.pagedata' file.
    The first page i.e. element 0 of the pages member represents the template
    for page 0 in the NotebookLines pages.

    This behaviour comes from my observing the notebooks on my device.

    """

    def __init__(self, pages=[]):
        """
        """
        self.pages = pages

    @classmethod
    def new(cls):
        print("new")
        return cls()

    @classmethod
    def load(cls, pagedata):
        """Return a Pagedata instance for the given data.

        :param pagedata: A string of page data lines.

        E.g.::

            Blank
            P Lines medium
            LS Grid margin large
            P Grid large

        If pagedata is not given or is empty the the Pagedata instance will
        not contain any pages. Is this actually possible? I'm not sure.

        """
        if pagedata and pagedata.strip():
            pages = [page for page in pagedata.split('\n') if page.strip()]

        else:
            pages = []

        return cls(pages)

    def dump(self):
        """A list of page templates one per line ready to write to disk."""
        return "\n".join(self.pages) if self.pages else ""
