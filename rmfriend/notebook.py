# -*- coding: utf-8 -*-
"""
"""
import os
import uuid
from pathlib import Path

from rmfriend import userconfig
from rmfriend.content import Content
from rmfriend.tools.sftp import SFTP
from rmfriend.pagedata import PageData
from rmfriend.metadata import MetaData
from rmfriend.utils import filename_from
from rmfriend.lines.notebooklines import NotebookLines


class Notebook(object):
    """This repesents a 'Notebook' on the reMarkable device.

    On reMarkable a notebook is actually a collections of files. Each file that
    makes up a notebook uses the same UUID (Universally Unique Identifer). The
    extension then determines what it does.

    From observation I've discovered a notebook will have the following file
    extensions and meanings:

      - 'pagedata' this contains the template used on each page in the
    notebook. This is handled by the PageData class.

      - 'lines' this contains the binary drawing information. It represents
    the notebooks content. The NotebookLines class handles this content.

      - 'lines.backup' I don't do anything with this at the moment.

      - 'metadata' this contains extra information about the lines file. For
    example its visible name. The MetaData class handles this content.

      - 'content' this contains information to aid the UI relating. For example
    its the last opened page and pen type used. The Content class handles this.

      - 'content' this contains information to aid the UI relating. For example
      its the last opened page and pen type used. The Content class handles
      this.

    Along with these files there are also two directories which have the same
    UUID with the 'extension':

      - 'thumbnails' this directory contains a small jpeg image of each page.
      For example: '0.jpg, 1.jpg,  3.jpg, etc'

      - 'cache' this directory contains a a full sized  each page. For example:
      '0.jpg, 1.jpg,  3.jpg, etc'

      - 'highlights': I don't know what to do with this just yet.

    """

    def __init__(
        self, document_id, pagedata, lines, metadata, content, thumbnails=[],
        cache=[]
    ):
        """
        """
        self.document_id = document_id
        # A PageData instance:
        self.pagedata = pagedata
        # A NotebookLines instance:
        self.lines = lines
        # A MetaData instance:
        self.metadata = metadata
        # A Content instance:
        self.content = content
        # Directories
        self.thumbnails = thumbnails
        self.cache = cache

    @property
    def name(self):
        """Return the meta data's name property."""
        return self.metadata.name

    @property
    def last_modified(self):
        """Return the meta data's last modified property."""
        return self.metadata.last_modified

    @property
    def last_opened_page(self):
        """Return the content's last opened page property."""
        return self.content.last_opened_page

    @property
    def page_count(self):
        """Return the lines's file count of pages."""
        return self.lines.page_count()

    @property
    def version(self):
        """Return the metadata's version."""
        return self.metadata.version

    @classmethod
    def load(
        cls, document_id, pagedata, lines, metadata, content, thumbnails=[],
        cache=[]
    ):
        """Return a Notebook for the given sections.

        :param document_id: The UUID string for this notebook.

        :param pagedata: The raw page data for this notebook.

        :param metadata: The raw meta JSON for this notebook.

        :param content: The raw content JSON for this notebook.

        :param thumbnails: A list of file present in the thumbnails directory.

        :param cache: A list of files present in the cache directory.

        """
        return cls(
            # verify this is actually a UUID formatted string.
            document_id=str(uuid.UUID(document_id)),
            pagedata=PageData.load(pagedata),
            lines=NotebookLines.load(lines),
            metadata=MetaData.load(metadata),
            content=Content.load(content),
            thumbnails=thumbnails,
            cache=cache,
        )

    def dump(self):
        """Return a dict of and the raw versions of each extension part."""
        return dict(
            document_id=self.document_id,
            pagedata=self.pagedata.dump(),
            lines=self.lines.dump(),
            metadata=self.metadata.dump(),
            content=self.content.dump(),
            thumbnails=self.thumbnails,
            cache=self.cache,
        )

    def write(self, destination_path):
        """Write out the notebook to disk.

        :param destination_path: Where to write the notebook to.

        The destination_path will contain the notebook files:

            <document_id>.(lines|metadata|content|pagedata)

        """
        destination = Path(destination_path)

        data = self.dump()

        document_id = data['document_id']

        for key in data:
            if key in ('document_id', 'thumbnails', 'cache'):
                # Ignore these. Thumnails and cache will be generated by
                # reMarkable. Let it do the work.
                continue

            filename = destination / "{}.{}".format(document_id, key)
            if key == 'lines':
                filename.write_bytes(data[key])
            else:
                filename.write_bytes(data[key].encode('utf-8'))

    @classmethod
    def read(cls, document_path, document_id):
        """Read a notebook from disk.

        :param document_path: The folder containing the notebook files.

        :param document_id: The UUID string for the notebook.

        This will attempt to read the files

            <document_id>.(lines|metadata|content|pagedata)

        The notebook directories (thumbnails and cache) will also be read.

        :returns: A Notebook instance.

        """
        data = {}
        document_path = Path(document_path)

        for key in ('lines', 'metadata', 'content', 'pagedata'):
            filename = document_path / "{}.{}".format(document_id, key)
            if key == 'lines':
                data[key] = filename.read_bytes()
            else:
                data[key] = filename.read_bytes().decode('utf-8')

        for key in ('thumbnails', 'cache'):
            dirname = document_path / "{}.{}".format(document_id, key)
            if dirname.is_dir():
                data[key] = [item.name for item in dirname.iterdir()]

        data['document_id'] = document_id

        return cls.load(**data)

    @classmethod
    def recover(cls, sftp, document_id):
        """Recover a remote notebook from reMarkable.

        :param sftp: A connected paramiko SFTP instance.

        This should have changed directory to the one containing the notebooks.

        :param document_id: The UUID string for the notebook.

        This will attempt to recover the files

            <document_id>.(lines|metadata|content|pagedata)

        The notebook directories (thumbnails and cache) will also be recovered.

        :returns: A Notebook instance.

        """
        config = userconfig.recover_or_create()
        cache_dir = Path(config['rmfriend']['cache_dir'])
        address = config['rmfriend']['address']
        username = config['rmfriend']['username']
        auth = dict(
            hostname=address,
            username=username,
        )

        for extension in ('lines', 'metadata', 'content', 'pagedata'):
            # Recover to the cache:
            local_file = filename_from(document_id, extension, cache_dir)
            remote_file = filename_from(document_id, extension)
            try:
                sftp.get(remote_file, localpath=local_file)
            except IOError as error:
                print('Error recovering {} to {}: {}'.format(
                    remote_file,
                    local_file,
                    error
                ))

        def get_(remote_dir, remote_file, local_file):
            with SFTP.connect(**auth) as sftp:
                sftp.chdir(remote_dir)
                sftp.get(
                    remote_file,
                    localpath=local_file,
                )

        for extension in ('thumbnails', 'cache'):
            with SFTP.connect(**auth) as sftp:
                name = filename_from(document_id, extension)
                local_dir = Path(
                    filename_from(document_id, extension, cache_dir)
                )
                dirname = cache_dir / name
                if not dirname.is_dir():
                    os.makedirs(dirname)
                # Iterate through each image and recover it:
                sftp.chdir(name)
                for item in sftp.listdir_iter():
                    local_file = str(local_dir / item.filename)
                    remote_file = item.filename
                    get_(name, remote_file, local_file)
