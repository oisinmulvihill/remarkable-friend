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

from rmfriend.utils import filename_from
from rmfriend.utils import document_id_and_extension


def get_log(e=None):
    return logging.getLogger("{0}.{1}".format(__name__, e) if e else __name__)


class SFTP(object):
    """
    """
    @classmethod
    @contextmanager
    def connect(
        cls, hostname, username='root', password=None,
        default_path="/home/root/.local/share/remarkable/xochitl",
        ssh_only=False
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
        if ssh_only:
            log.info(
                "Connected to device '{}' changing to remote path '{}'".
                format(hostname, default_path)
            )
            log.debug("yielding ssh client")
            yield ssh

        else:
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

        # filter out the non notebooks based on the collection we have
        # recovered.
        returned = {}
        for document_id in results:
            extensions = list(results[document_id].keys())
            if 'pdf' in extensions or 'epub' in extensions:
                print("Ignoring '{}' as its not to be a notebook: {}".format(
                    document_id, extensions,
                ))
            else:
                returned[document_id] = results[document_id]

        return returned

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
    def recover_notebooks(
        cls, sftp, cache_dir, notebooks, document_ids, progress_callback
    ):
        """
        """
        progress = 1
        total = len(document_ids)

        for doc_id in document_ids:
            for extension in notebooks[doc_id]:
                progress += 1

                if extension not in ('lines', 'metadata', 'content'):
                    # ignore for the moment
                    continue

                # Recover to the cache:
                local_file = filename_from(
                    doc_id, extension, cache_dir
                )
                remote_file = filename_from(doc_id, extension)
                sftp.get(remote_file, localpath=local_file)

                progress_callback(total, progress)

    @classmethod
    def remote_md5sum(cls, ssh, remote_dir, filename):
        """
        """
        remote_file = '{}/{}'.format(remote_dir, filename)
        command = 'md5sum {}'.format(remote_file)
        stdin, stdout, stderr = ssh.exec_command(command)
        # split the md5sum line into sum and filename
        #   2decad2252e3cd09fb2cfa19118b250b  \
        #       93861cf6-dffc-45cd-ae02-25283e71c4db.content
        # returning just 2decad2252e3cd09fb2cfa19118b250b
        remote_md5 = stdout.read().decode().strip().split(' ')[0]
        return remote_md5

    @classmethod
    def notebook_remote_status(
        cls, sftp, ssh, remote_dir, notebooks, progress_callback
    ):
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
        progress = 1
        total = len(sftp.listdir_attr())
        for item in sftp.listdir_attr():
            (document_id, extension) = document_id_and_extension(
                item.filename
            )

            progress += 1

            if document_id not in notebooks:
                continue

            if extension not in ('lines', 'metadata', 'content'):
                continue

            md5sum = '' #cls.remote_md5sum(ssh, remote_dir, item.filename)
            progress_callback(total, progress)
            notebooks[document_id][extension] = {
                'last_access': item.st_atime,
                'last_modification': item.st_mtime,
                'size': item.st_size,
                'md5sum': md5sum,
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
            file_ = "{}.{}".format(document_id, 'metadata')
            try:
                data = cls.get(sftp, file_)

            except IOError as error:
                # print('Error reading {}: {}'.format(file_, error))
                pass

            else:
                notebooks[document_id]['metadata'] = json.loads(data)

                metadata = notebooks[document_id]['metadata']
                last_modified = int(metadata['lastModified']) / 100
                last_modified = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(last_modified)
                )
                listing.append({
                    'id': document_id,
                    'last_modified': last_modified,
                    'name': metadata['visibleName']
                })

        return listing
