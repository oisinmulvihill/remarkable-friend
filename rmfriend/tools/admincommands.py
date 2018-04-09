# -*- coding: utf-8 -*-
"""
Handy command line tool working with the reMarkable tablet and manipulating
notebooks.

Oisin Mulvihill
2018-03-10

"""
import sys
import getpass
import logging

import cmdln
from terminaltables import AsciiTable

from rmfriend import userconfig
from rmfriend.tools.sftp import SFTP
from rmfriend.tools.sync import Sync
from rmfriend.notebook import Notebook
from rmfriend.lines.notebooklines import NotebookLines


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
        data = NotebookLines.read(lines_file)

        log.debug("Parsing file '{}'".format(lines_file))
        notebook = NotebookLines.load(data)

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
        data = NotebookLines.read(lines_file)

        log.debug("Parsing file '{}'".format(lines_file))
        notebook = NotebookLines.load(data)

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
            ['Last Modified', 'Name', 'reMarkable Version', 'Local Version']
        ]
        if opts.show_id:
            table_listing[0].insert(0, 'ID')

        for e in listing:
            if opts.show_id:
                table_listing.append((
                    e['id'],
                    e['last_modified'],
                    e['name'],
                    e['version'],
                    e['local_version'] or '-'
                )
                )
            else:
                table_listing.append((
                    e['last_modified'],
                    e['name'],
                    e['version'],
                    e['local_version'] or '-'
                ))

        table = AsciiTable(table_listing)
        print(table.table)

    def do_rsync(self, subcmd, opts, *args, **kwargs):
        """${cmd_name}: Update the local cache with new & changed notebooks.

        ${cmd_usage}
        ${cmd_option_list}

        """
        Sync.rsync()

    def do_generate_previews(self, subcmd, opts, *args, **kwargs):
        """${cmd_name}: Generate the notebook file previews.

        ${cmd_usage}
        ${cmd_option_list}

        """
        Sync.generate_previews()

    def do_cache_status(self, subcmd, opts, *args, **kwargs):
        """${cmd_name}: Update the local cache with new & changed notebooks.

        ${cmd_usage}
        ${cmd_option_list}

        """
        notebooks = Sync.notebook_cache()

        listing = [
            ('Name', 'Version', 'URI')
        ]
        for doc_id in notebooks:
            for ext in notebooks[doc_id]:
                nb = notebooks[doc_id][ext]
                listing.append(
                    (
                        nb['name'],
                        nb['version'],
                        nb['uri'],
                    )
                )

        table = AsciiTable(listing)
        print(table.table)

    def do_notebook_previews(self, subcmd, opts, *args, **kwargs):
        """${cmd_name}: Show the notebook preview listing.

        The generate_previews create an index we can use to reference a
        notebook and its pages. This will be used in the UI.

        ${cmd_usage}
        ${cmd_option_list}

        """
        notebooks = Sync.notebook_previews()

        listing = [
            ('Name', 'Pages')
        ]
        for notebook in notebooks:
            listing.append(
                (
                    notebook['name'],
                    len(notebook['pages']),
                )
            )

        table = AsciiTable(listing)
        print(table.table)

    def do_recover(self, subcmd, opts, document_id):
        """${cmd_name}: Recover a specific notebook to the local cache.

        The given document will be recovered regardless of whether the same
        files already exist.

        ${cmd_usage}
        ${cmd_option_list}

        """
        config = userconfig.recover_or_create()
        auth = dict(
            hostname=config['rmfriend']['address'],
            username=config['rmfriend']['username'],
        )
        with SFTP.connect(**auth) as sftp:
            Notebook.recover(sftp, document_id)
