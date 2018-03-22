# -*- coding: utf-8 -*-
"""
Handy command line tool working with the reMarkable tablet and manipulating
notebooks.

Oisin Mulvihill
2018-03-10

"""
import os
import sys
import getpass
import logging

import cmdln
from terminaltables import AsciiTable

from rmfriend import userconfig
from rmfriend.tools.sftp import SFTP
from rmfriend.tools.sync import Sync
from rmfriend.lines.notebook import Notebook


def get_log(e=None):
    return logging.getLogger("{0}.{1}".format(__name__, e) if e else __name__)


class AdminCommands(cmdln.Cmdln):
    """Usage:
        rmfriend --help

    ${command_list}
    ${help_list}

    """
    name = "rmfriend"

    def do_notebook_to_svg(
        self, subcmd, opts, lines_file, output_file, *args, **kwargs
    ):
        """${cmd_name}: Convert a raw lines file into SVG documents.

        ${cmd_usage}
        ${cmd_option_list}

        """
        from rmfriend.export.svg import Export

        log = get_log('do_notebook_to_svg')

        return_code = 0

        log.debug("Reading file '{}'".format(lines_file))
        data = Notebook.read(lines_file)

        log.debug("Parsing file '{}'".format(lines_file))
        notebook = Notebook.parse(data)

        log.debug("{} has '{}' pages.".format(
            lines_file, notebook.pages.count
        ))
        for file_ in Export.convert(notebook, output_file):
            log.debug("Writing file '{}'.".format(file_['filename']))
            file_['image'].save()

        sys.exit(return_code)

    def do_notebook_to_png(
        self, subcmd, opts, lines_file, output_file, *args, **kwargs
    ):
        """${cmd_name}: Convert a raw lines file into a PNG documents.

        ${cmd_usage}
        ${cmd_option_list}

        """
        from rmfriend.export.png import Export

        log = get_log('do_notebook_to_png')

        return_code = 0

        log.debug("Reading file '{}'".format(lines_file))
        data = Notebook.read(lines_file)

        log.debug("Parsing file '{}'".format(lines_file))
        notebook = Notebook.parse(data)

        log.debug("{} has '{}' pages.".format(
            lines_file, notebook.pages.count
        ))
        for file_ in Export.convert(notebook, output_file):
            log.debug("Writing file '{}'.".format(file_['filename']))
            with open(file_['filename'], 'wb') as fd:
                file_['image'].save(fd, "PNG")

        sys.exit(return_code)

    @cmdln.alias("ls")
    @cmdln.option(
        "-i", "--show-id", action="store_true", dest="show_id", default=False,
        help="Show the document ID in the listing."
    )
    @cmdln.option(
        "--password", action="store", dest="password",
        default=None,
        help="The password to use when connecting."
    )
    @cmdln.option(
        "-p", action="store_true", dest="ask", default=False,
        help="Ask for password to be entered."
    )
    def do_notebook_ls(self, subcmd, opts, *args, **kwargs):
        """${cmd_name}: Show a list of notebooks on reMarkable.

        ${cmd_usage}
        ${cmd_option_list}

        """
        config = userconfig.recover_or_create()
        address = config['rmfriend']['address']
        username = config['rmfriend']['username']

        if opts.ask:
            password = getpass.getpass(
                "Please enter password for {}@{}: ".format(username, address)
            )
        else:
            password = opts.password

        auth = dict(
            hostname=config['rmfriend']['address'],
            username=config['rmfriend']['username'],
            password=password,
        )
        with SFTP.connect(**auth) as sftp:
            results = SFTP.notebooks_from_listing(sftp.listdir())
            listing = SFTP.notebook_ls(sftp, results)

        table_listing = [
            ['Last Modified', 'Name']
        ]
        if opts.show_id:
            table_listing[0].insert(0, 'ID')

        for e in listing:
            if opts.show_id:
                table_listing.append((
                    e['id'], e['last_modified'], e['name'])
                )
            else:
                table_listing.append((
                    e['last_modified'], e['name'])
                )

        table = AsciiTable(table_listing)
        print(table.table)

    def do_sync_ls(self, subcmd, opts, *args, **kwargs):
        """${cmd_name}: Show a list of notebooks on reMarkable.

        ${cmd_usage}
        ${cmd_option_list}

        """
        config = userconfig.recover_or_create()
        address = config['rmfriend']['address']
        username = config['rmfriend']['username']
        cache_dir = config['rmfriend']['cache_dir']

        auth = dict(
            hostname=address,
            username=username,
        )
        with SFTP.connect(**auth) as sftp:
            remote_notebooks = SFTP.notebooks_from_listing(sftp.listdir())
            SFTP.notebook_remote_status(sftp, remote_notebooks)

            local_notebooks = Sync.notebooks_cache_status()

            remote = set(remote_notebooks.keys())
            local = set(local_notebooks.keys())

            present_on_both = local.union(remote)
            for doc_id in present_on_both:
                for extension in remote_notebooks[doc_id]:
                    if extension in (
                        'thumbnails', 'cache', 'backup', 'highlights'
                    ):
                        # ignore for the moment
                        continue

                    auth['ssh_only'] = True
                    with SFTP.connect(**auth) as ssh:
                        filename = '{}.{}'.format(doc_id, extension)
                        stdin, stdout, stderr = ssh.exec_command(
                        'cd {} ; md5sum {}'.format(
                            '/home/root/.local/share/remarkable/xochitl',
                            filename
                        ))
                        print(stdout.read())

                        import hashlib
                        import binascii
                        local_file = os.path.join(cache_dir, filename)
                        with open(local_file, 'rb') as lfd:
                            print(binascii.hexlify(
                                hashlib.md5(lfd.read()).digest()
                            ))

                        import ipdb; ipdb.set_trace()
                        pass

                    filename = '{}.{}'.format(doc_id, extension)
                    local_file = os.path.join(cache_dir, filename)
                    sftp.get(filename, localpath=local_file)

            only_local = local.difference(remote)
            print("Files only present locally: ")
            print(only_local)

            # Recover the file present on reMarkable and store them locally
            only_remote = remote.difference(local)
            for doc_id in only_remote:
                for extension in remote_notebooks[doc_id]:
                    if extension in (
                        'thumbnails', 'cache', 'backup', 'highlights'
                    ):
                        # ignore for the moment
                        continue

                    print('doc_id: {} extension: {}'.format(doc_id, extension))
                    filename = '{}.{}'.format(doc_id, extension)
                    local_file = os.path.join(cache_dir, filename)
                    sftp.get(filename, localpath=local_file)




