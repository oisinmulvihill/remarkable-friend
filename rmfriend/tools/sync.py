# -*- coding: utf-8 -*-
"""
Manages the synchronisation of notebooks to local desktop to speed up
manipulation and to backup.

"""
import os
import sys
import json
import hashlib
import binascii
import collections
from pathlib import Path

from rmfriend import userconfig
from rmfriend.export import svg
from rmfriend.tools.sftp import SFTP
from rmfriend.lines.notebook import Notebook
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
            doc_id, ext = document_id_and_extension(item.name)
            md5sum = binascii.hexlify(
                hashlib.md5(item.read_bytes()).digest()
            )
            status = item.lstat()
            notebooks[doc_id][ext] = {
                'last_access': int(status.st_atime),
                'last_modification': int(status.st_mtime),
                'size': status.st_size,
                'md5sum': md5sum.decode(),
            }

        return dict(notebooks)

    @classmethod
    def generate_previews(cls):
        """
        """
        config = userconfig.recover_or_create()
        cache_dir = Path(config['rmfriend']['cache_dir'])
        preview_dir = cache_dir / 'preview'
        if not os.path.isdir(preview_dir):
            os.makedirs(preview_dir)

        def action_ticker(total, position):
            done = int((position / total) * 100)
            sys.stdout.write(
                '\r{}: {:2d}%'.format('Preview generation', done)
            )
            sys.stdout.flush()

        total = len(list(cache_dir.iterdir()))
        progress = 0
        for item in cache_dir.iterdir():
            progress += 1
            action_ticker(total, progress)
            doc_id, ext = document_id_and_extension(item.name)
            if ext != 'lines':
                # Only generate previews for notebooks
                continue

            metadata = {}
            metadata_file = cache_dir / "{}.metadata".format(doc_id)
            if metadata_file.is_file():
                try:
                    metadata = json.loads(metadata_file.read_bytes())
                except ValueError:
                    pass
            name = metadata.get('visibleName')
            notebook = Notebook.parse(item.read_bytes())
            image_filename = "{}-page".format(doc_id)
            image_index = {'id': doc_id, 'name': name, 'pages': []}
            index_filename = str(preview_dir / "{}.page_index".format(doc_id))
            for file_ in svg.Export.convert(notebook, image_filename):
                # index to easily get all notebook preview pages:
                preview = str(preview_dir / file_['filename'])
                with open(preview, 'wb') as fd:
                    os.chdir(str(preview_dir))
                    file_['image'].save()
                image_index['pages'].append(preview)
            with open(index_filename, 'wb') as fd:
                fd.write(json.dumps(image_index).encode())

    @classmethod
    def notebook_previews(cls):
        """
        """
        config = userconfig.recover_or_create()
        cache_dir = Path(config['rmfriend']['cache_dir'])
        preview_dir = cache_dir / 'preview'

        found = []
        for item in cache_dir.iterdir():
            doc_id, ext = document_id_and_extension(item.name)
            if ext == 'lines':
                # Is there a generated index?
                index_filename = preview_dir / "{}.page_index".format(doc_id)
                if index_filename.is_file():
                    try:
                        notebook = json.loads(index_filename.read_bytes())
                    except ValueError:
                        pass

                    else:
                        found.append(notebook)

        return found

    @classmethod
    def rsync(cls):
        """
        """
        config = userconfig.recover_or_create()
        address = config['rmfriend']['address']
        username = config['rmfriend']['username']
        cache_dir = config['rmfriend']['cache_dir']
        remote_dir = config['rmfriend']['remote_dir']

        local_notebooks = Sync.notebook_cache()
        local = set(local_notebooks.keys())
        print("Local notebooks '{}'".format(len(local)))

        def progress_factory(message):
            def action_ticker(total, position):
                done = int((position / total) * 100)
                sys.stdout.write(
                    '\r{}: {:2d}%'.format(message, done)
                )
                sys.stdout.flush()

            return action_ticker

        calculation_progress = progress_factory('Calculating remote changes')

        auth = dict(
            hostname=address,
            username=username,
        )
        with SFTP.connect(**auth) as sftp:
            remote_notebooks = SFTP.notebooks_from_listing(sftp.listdir())
            auth['ssh_only'] = True
            with SFTP.connect(**auth) as ssh:
                SFTP.notebook_remote_status(
                    sftp, ssh, remote_dir, remote_notebooks,
                    calculation_progress
                )

        remote = set(remote_notebooks.keys())
        print("Notebooks present remotely: {}".format(len(remote)))

        only_local = local.difference(remote)
        print("Notebooks only present locally: {}".format(len(only_local)))

        present_on_both = local.union(remote)
        changed_notebooks = []
        for doc_id in present_on_both:
            if doc_id not in remote_notebooks:
                # only local, ignore.
                continue

            for extension in remote_notebooks[doc_id]:
                if extension not in ('lines', 'metadata', 'content'):
                    # ignore for the moment
                    continue
                remote_md5 = remote_notebooks[doc_id][extension]['md5sum']
                if doc_id not in local_notebooks:
                    # a new notebook skip, it will be handled later.
                    continue
                local_md5 = local_notebooks[doc_id][extension]['md5sum']
                if local_md5 != remote_md5:
                    changed_notebooks.append(doc_id)

        recover_progress = progress_factory('Recovering changes')
        auth['ssh_only'] = False
        with SFTP.connect(**auth) as sftp:
            SFTP.recover_notebooks(
                sftp, cache_dir, remote_notebooks, changed_notebooks,
                recover_progress
            )

        recover_progress = progress_factory('Recovering new notebooks')
        only_remote = remote.difference(local)
        auth['ssh_only'] = False
        with SFTP.connect(**auth) as sftp:
            SFTP.recover_notebooks(
                sftp, cache_dir, remote_notebooks, list(only_remote),
                recover_progress
            )

        returned = {
            'new': list(only_remote),
            'deleted': list(only_local),
            'changed': list(changed_notebooks),
        }

        return returned
