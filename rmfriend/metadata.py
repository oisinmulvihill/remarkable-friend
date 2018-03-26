# -*- coding: utf-8 -*-
"""
"""
import time
import json


class MetaData(object):
    """This file contains information about the notebook.

    From what I have observed this is information such as the visible name
    then end user types in when creating a notebook.

    """

    def __init__(self, data):
        """
        """
        self.data_ = data

    @property
    def name(self):
        """Attempt to return the notebooks visibleName field."""
        self.data_.get('visibleName', '')

    @property
    def last_modified(self):
        """Attempt to an ISO8601 string for the lastModified field."""
        last_modified = self.data_.get('lastModified', '0')
        # Time in gmt hack really as its and epoch timestamp with timezone
        last_modified = int(last_modified[:-3])
        last_modified = time.strftime(
            '%Y-%m-%d %H:%M:%S+Z', time.gmtime(last_modified)
        )
        return last_modified

    @classmethod
    def new_meta_data(cls):
        """Returns a default meta data dict for create meta data instances."""
        return {
            "deleted": False,
            "lastModified": "0",
            "metadatamodified": False,
            "modified": False,
            "parent": "",
            "pinned": False,
            "synced": False,
            "type": "DocumentType",
            "version": 1,
            "visibleName": "<No Name>"
        }

    @classmethod
    def parse(cls, meta_data=None):
        """Return a MetaData instance for the given data.

        :param page_data: A string of JSON data.

        E.g.::

            '{
                "deleted": false,
                "lastModified": "1520689822972",
                "metadatamodified": false,
                "modified": false,
                "parent": "",
                "pinned": false,
                "synced": true,
                "type": "DocumentType",
                "version": 3,
                "visibleName": "Om1"
            }'

        """
        if meta_data:
            meta_ = json.loads(meta_data)

        else:
            meta_ = cls.new_meta_data()

        return cls(meta_)
