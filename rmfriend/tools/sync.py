# -*- coding: utf-8 -*-
"""
Manages the synchronisation of notebooks to local desktop to speed up
manipulation and to backup.

"""
import os
import sys
import json
import collections
from pathlib import Path

from rmfriend import utils
from rmfriend import userconfig
from rmfriend.export import svg
from rmfriend.tools.sftp import SFTP
from rmfriend.notebook import Notebook
from rmfriend.utils import document_id_and_extension
from rmfriend.lines.notebooklines import NotebookLines


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
            notebook = NotebookLines.parse(item.read_bytes())
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
