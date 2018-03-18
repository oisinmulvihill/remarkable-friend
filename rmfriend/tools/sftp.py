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
from terminaltables import AsciiTable


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
                },
                :
                etc
            }

        """
        results = collections.defaultdict(dict)

        for entry in dir_listing:
            file_name_parts = entry.split('.')
            document_id = file_name_parts[0].strip()
            if len(file_name_parts) > 1:
                extension = file_name_parts[-1].strip()

            found = results[document_id]
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
    def notebook_ls(cls, sftp, notebooks, show_id=False):
        """Recover the metadata and print a listing of the notebooks.

        :param sftp: See connect() for details.

        :param notebooks: See notebooks_from_listing().

        :param show_id: False or True

        If this is True the notebook's UUID will be displayed. This will be
        hidden by default.

        """
        listing = [
            ['Last Modified', 'Name']
        ]
        if show_id:
            listing[0].insert(0, 'ID')

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
            name = metadata['visibleName']
            if show_id:
                listing.append((document_id, last_modified, name))
            else:
                listing.append((last_modified, name))

        # print("\n\n{}\n".format(notebooks))
        table = AsciiTable(listing)
        print(table.table)