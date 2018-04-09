# -*- coding: utf-8 -*-
"""
Manages the synchronisation of notebooks to local desktop to speed up
manipulation and to backup.

"""
import sys
import json
import collections
from pathlib import Path

from natsort import natsorted, ns

from rmfriend import utils
from rmfriend import userconfig
from rmfriend.tools.sftp import SFTP
from rmfriend.notebook import Notebook
from rmfriend.utils import filename_from
from rmfriend.utils import document_id_and_extension


class Sync(object):
    """
    """
    @classmethod
    def notebook_cache(cls):
        """
        """
        notebooks = collections.defaultdict(dict)

        config = userconfig.recover_or_create()
        cache_dir = Path(config['rmfriend']['cache_dir'])

        for item in cache_dir.iterdir():
            if item.is_dir():
                # Skip for the moment
                continue
            doc_id, ext = document_id_and_extension(item.name)
            uri = item.as_uri()
            version = '-'
            name = '-'
            if ext == 'metadata':
                metadata = json.loads(item.read_bytes())
                name = metadata['visibleName']
                version = metadata['version']

            notebooks[doc_id][ext] = {
                'uri': uri,
                'version': version,
                'name': name,
            }

        return dict(notebooks)

    @classmethod
    def notebook_previews(cls):
        """
        """
        config = userconfig.recover_or_create()
        cache_dir = Path(config['rmfriend']['cache_dir'])

        found = []
        for item in cache_dir.iterdir():
            document_id, ext = document_id_and_extension(item.name)
            listing = {
                "id": document_id,
                "name": '',
                "version": '',
                "last_modified": '',
                "last_opened": '',
                "images": [],
            }
            if ext == 'thumbnails':
                # recover metadata details:
                name = filename_from(document_id, 'metadata')
                metadata = cache_dir / name
                metadata = json.loads(metadata.read_bytes())
                listing['name'] = metadata['visibleName']
                listing['version'] = metadata['version']
                listing['last_modified'] = metadata['lastModified']

                # Is the last opened page present?
                name = filename_from(document_id, 'content')
                content = cache_dir / name
                if content.is_file():
                    content = json.loads(content.read_bytes())
                    if 'lastOpenedPage' in content:
                        listing['last_opened'] = content['lastOpenedPage']

                # find the thumbnail images:
                name = filename_from(document_id, 'thumbnails')
                thumbnails = cache_dir / name
                for item in thumbnails.iterdir():
                    listing['images'].append(item.name)
                listing['images'] = natsorted(
                    listing['images'], alg=ns.IGNORECASE
                )
                found.append(listing)

        # Sort by last modified decending emulating reMarkable / Notebooks UI
        found = sorted(
            found,
            key=lambda doc: doc['last_modified'],
            reverse=True
        )

        return found

    @classmethod
    def rsync(cls):
        """
        """
        config = userconfig.recover_or_create()
        address = config['rmfriend']['address']
        username = config['rmfriend']['username']

        local_notebooks = Sync.notebook_cache()
        local = set(local_notebooks.keys())

        def progress_factory(message):
            def action_ticker(total, position):
                done = int((position / total) * 100)
                sys.stdout.write(
                    '\r{}: {:2d}%'.format(message, done)
                )
                sys.stdout.flush()

            return action_ticker

        auth = dict(
            hostname=address,
            username=username,
        )
        with SFTP.connect(**auth) as sftp:
            notebook_listing = SFTP.notebooks_from_listing(sftp.listdir())
            remote_notebooks = {
                nb['id']: nb
                for nb in SFTP.notebook_ls(sftp, notebook_listing)
            }

        remote = set(remote_notebooks.keys())
        print("All notebooks on reMarkable: {}".format(len(remote)))

        only_local = local.difference(remote)
        print("Notebooks only present locally: {}".format(len(only_local)))

        present_on_both = local.union(remote)
        print("Notebooks on both: {}".format(len(present_on_both)))

        only_remote = remote.difference(local)
        print("Notebooks only on reMarkable: {}".format(len(only_remote)))

        change_progress = utils.progress_factory('Working out changes')
        changed_notebooks = []
        with SFTP.connect(**auth) as sftp:
            progress = 1
            total = len(list(present_on_both))
            for doc_id in present_on_both:
                change_progress(progress, total)
                progress += 1

                if doc_id not in remote_notebooks:
                    # only local, ignore.
                    continue

                local_version = remote_notebooks[doc_id]['local_version']
                remarkable_version = remote_notebooks[doc_id]['version']
                if remarkable_version > local_version:
                    Notebook.recover(sftp, doc_id)

        recover_progress = utils.progress_factory('Recovering new notebooks')
        auth['ssh_only'] = False
        with SFTP.connect(**auth) as sftp:
            # clear change progress update.
            print('\n')
            progress = 1
            total = len(only_remote)
            for document_id in only_remote:
                Notebook.recover(sftp, document_id)
                recover_progress(progress, total)
                progress += 1

        returned = {
            'new': list(only_remote),
            'deleted': list(only_local),
            'changed': list(changed_notebooks),
        }

        return returned
