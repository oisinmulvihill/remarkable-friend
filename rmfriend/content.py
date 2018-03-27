# -*- coding: utf-8 -*-
"""
"""
import json


class Content(object):
    """This file information the aids the User Interface when displaying the
    notebook.

    From what I have observed this is information such as the last page opened,
    total pages and things like the last used pen.

    """

    def __init__(self, data={}):
        """
        """
        self.data_ = data

    @property
    def last_opened_page(self):
        """Attempt to return the notebooks lastOpenedPage field."""
        return self.data_.get('lastOpenedPage', 0)

    @classmethod
    def new(cls):
        """Returns a default content dict for create Content instance."""
        return cls(data={
            "extraMetadata": {
                "LastColor": "Black",
                "LastTool": "Fineliner",
                "ThicknessScale": "2"
            },
            "fileType": "",
            "fontName": "",
            "lastOpenedPage": 0,
            "lineHeight": -1,
            "margins": 100,
            "pageCount": 1,
            "textScale": 1,
            "transform": {
                "m11": 1,
                "m12": 0,
                "m13": 0,
                "m21": 0,
                "m22": 1,
                "m23": 0,
                "m31": 0,
                "m32": 0,
                "m33": 1
            }
        })

    @classmethod
    def parse(cls, content):
        """Return a Content instance for the given data.

        :param content: A string of JSON data.

        E.g.::

            '{
                "extraMetadata": {
                    "LastColor": "Black",
                    "LastTool": "Fineliner",
                    "ThicknessScale": "2"
                },
                "fileType": "",
                "fontName": "",
                "lastOpenedPage": 0,
                "lineHeight": -1,
                "margins": 100,
                "pageCount": 1,
                "textScale": 1,
                "transform": {
                    "m11": 1,
                    "m12": 0,
                    "m13": 0,
                    "m21": 0,
                    "m22": 1,
                    "m23": 0,
                    "m31": 0,
                    "m32": 0,
                    "m33": 1
                }
            }'

        """
        return cls(data=json.loads(content))

    def dump(self):
        """Return JSON string of the internal data we could write to disk."""
        return json.dumps(self.data_)
