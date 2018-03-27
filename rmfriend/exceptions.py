# -*- coding: utf-8 -*-
"""
"""


class RMFriendError(Exception):
    """
    """


class PageNotFoundError(RMFriendError):
    """An operation with a page that could not be found was attempted."""
