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

    def __init__(self, pages):
        """
        """
        self.pages = pages

    @classmethod
    def parse(cls, page_data=None):
        """Return a Pagedata instance for the given data.

        :param page_data: A string of page data lines.

        E.g.::

            Blank
            P Lines medium
            LS Grid margin large
            P Grid large

        If page_data is not given or is empty the the Pagedata instance will
        not contain any pages. Is this actually possible? I'm not sure.

        """
        if page_data and page_data.strip():
            pages = [page for page in page_data.split('\n') if page.strip()]

        else:
            pages = []

        return cls(pages)
