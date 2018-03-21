# -*- coding: utf-8 -*-
"""
Manages the synchronisation of notebooks to local desktop to speed up
manipulation and to backup.

"""
import collections
from pathlib import Path

from rmfriend import userconfig
from rmfriend.utils import document_id_and_extension


class Sync(object):
    """
    """
    @classmethod
    def notebooks_cache_status(cls):
        """
        """
        notebooks = collections.defaultdict(dict)

        config = userconfig.recover_or_create()
        cache_dir = Path(config['rmfriend']['cache_dir'])

        for item in cache_dir.iterdir():
            doc_id, ext = document_id_and_extension(item.name)
            # if ext == 'cache':
            #     # not handled yet.
            #     print('Cache found: is_dir? {}'.format(item.is_dir()))
            #     print([i for i in item.iterdir()])

            status = item.lstat()
            notebooks[doc_id][ext] = {
                'last_access': int(status.st_atime),
                'last_modification': int(status.st_mtime),
                'size': status.st_size,
            }

        return dict(notebooks)
