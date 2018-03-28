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

    def __init__(self, data={}):
        """
        """
        self.data_ = data

    @property
    def name(self):
        """Attempt to return the notebooks visibleName field."""
        return self.data_.get('visibleName', '<No Name>')

    @property
    def version(self):
        """Attempt to return the version field."""
        return self.data_.get('version', 1)

    @property
    def last_modified(self):
        """Attempt to an ISO8601 string for the lastModified field."""
        last_modified = self.data_.get('lastModified', '')
        if last_modified:
            # Time in UTC, convert from epoch timestamp in milliseconds to
            # seconds:
            last_modified = int(last_modified) / 1000
            last_modified = time.strftime(
                '%Y-%m-%d %H:%M:%S+Z', time.gmtime(last_modified)
            )
        return last_modified

    @classmethod
    def new(cls):
        """Returns a default meta data dict for create meta data instances."""
        return cls(data={
            "deleted": False,
            "lastModified": "",
            "metadatamodified": False,
            "modified": False,
            "parent": "",
            "pinned": False,
            "synced": False,
            "type": "DocumentType",
            "version": 1,
            "visibleName": "No Name"
        })

    @classmethod
    def load(cls, metadata):
        """Return a MetaData instance for the given data.

        :param metadata: A string of JSON data.

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
        return cls(data=json.loads(metadata))

    def dump(self):
        """Return JSON string of the internal data we could write to disk."""
        return json.dumps(self.data_, indent=4)
