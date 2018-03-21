# -*- coding: utf-8 -*-
"""
"""
import io
import json
import time
import logging
import collections
from contextlib import contextmanager

import paramiko

from rmfriend.utils import document_id_and_extension


def get_log(e=None):
    return logging.getLogger("{0}.{1}".format(__name__, e) if e else __name__)


class SFTP(object):
    """
    """
    @classmethod
    def notebooks_from_listing(cls, dir_listing):
        """Recover the listing of notebooks from the raw directory listing.

        :param dir_listing: A list of of file names with extensions.

        :returns: A dict of notebook document ids.

        E.g.::

            {
                '04b68eba-86f5-41fc-aa5d-e38f948ea109': {
                    'metadata': {},
                    'content': {},
                    'lines': {},
                    'pagedata': {},
                    'cache': {},
                },
                :
                etc
            }

        """
        results = collections.defaultdict(dict)

        for entry in dir_listing:
            document_id, extension = document_id_and_extension(entry)
            found = results[document_id]
            if extension:
                found[extension] = {}
            results[document_id] = found

        # filter out anything that doesn't have the 'lines' extension as this
        # is not a notebook. It could be a PDF for example.
        results = {
            doc_id: parts
            for (doc_id, parts) in results.items()
            if 'lines' in parts
        }

        return dict(results)

    @classmethod
    @contextmanager
    def connect(
        cls, hostname, username='root', password=None,
        default_path="/home/root/.local/share/remarkable/xochitl"
    ):
        """A context manager that sets up a connection to the device.

        :param host: The Address/IP Address of the device.

        :param username: The user which defaults to root.

        :param password: The user's password.

        :param default_path:

        This yields a connected open sftp client in the default path.

        When control returns the connection is closed.

        """
        log = get_log('SFTP.connect')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        log.info(
            "Connecting to device hostname '{}' username '{}'".
            format(hostname, username)
        )
        ssh.connect(hostname=hostname, username=username, password=password)
        sftp = ssh.open_sftp()
        log.info(
            "Connected to device '{}' changing to remote path '{}'".
            format(hostname, default_path)
        )
        sftp.chdir(default_path)
        log.debug("yielding sftp client")
        yield sftp
        ssh.close()
        log.info("Connection to device '{}' closed.".format(hostname))

    @classmethod
    def get(cls, sftp, filename):
        """Recover the given file's contents from the remote side.

        :param sftp: See connect() for details.

        :param filename: E.g. 12d97066-9881-44b6-9abc-2284855f43a1.lines

        :returns: The raw bytes recovered.

        """
        fd = io.BytesIO(b'')
        sftp.getfo(filename, fd)
        fd.seek(0)
        return fd.read()

    @classmethod
    def notebook_remote_status(cls, sftp, notebooks):
        """Update the notebooks give with filesystem information.

        :param sftp: See connect() for details.

        :param notebooks: See notebooks_from_listing().

        The classmethod is used to recover the current filesystem status of
        notebooks on the device. This will update each of the entries in the
        notebooks dict with a status dict in the form::

                {
                    'last_access': <remote st_atime>,
                    'last_modification': <remote st_mtime>,
                    'size': <remote st_size>,
                }

        """
        for item in sftp.listdir_attr():
            (document_id, extension) = document_id_and_extension(
                item.filename
            )
            if document_id in notebooks:
                notebooks[document_id][extension] = {
                    'last_access': item.st_atime,
                    'last_modification': item.st_mtime,
                    'size': item.st_size,
                }

    @classmethod
    def notebook_ls(cls, sftp, notebooks):
        """Recover the metadata and print a listing of the notebooks.

        :param sftp: See connect() for details.

        :param notebooks: See notebooks_from_listing().

        :returns: A list of notebook information or an empty list.

        E.g.::

            [
                {
                    'id': 'UUID',
                    'name': 'notebook name',
                    'last_modified': 'iso8601 formatted string'
                },
                :
                etc
            ]

        This only contains the information and not the actual notebook lines
        data.

        """
        listing = []

        for document_id in notebooks:
            # for extension in ('metadata', 'content'):
            for extension in ('metadata',):
                file_ = "{}.{}".format(document_id, extension)
                data = cls.get(sftp, file_)
                notebooks[document_id][extension] = json.loads(data)

            metadata = notebooks[document_id]['metadata']
            # Time in gmt hack really as its and epoch timestamp with timezone
            last_modified = int(metadata['lastModified'][:-3])
            last_modified = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.gmtime(last_modified)
            )
            listing.append({
                'id': document_id,
                'last_modified': last_modified,
                'name': metadata['visibleName']
            })

        return listing
