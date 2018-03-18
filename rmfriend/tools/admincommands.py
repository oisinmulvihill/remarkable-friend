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
from rmfriend.tools.sftp import SFTP
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
        "-a", "--address", action="store", dest="address",
        default='10.11.99.1',
        help="The address to connect to. The default is %default"
    )
    @cmdln.option(
        "-u", "--username", action="store", dest="username",
        default='root',
        help="The username to use. The default is %default"
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
        if opts.ask:
            password = getpass.getpass(
                "Please enter password for {}@{}: ".
                format(opts.username, opts.address)
            )
        else:
            password = opts.password

        auth = dict(
            hostname=opts.address,
            username=opts.username,
            password=password,
        )
        with SFTP.connect(**auth) as sftp:
            results = SFTP.notebooks_from_listing(sftp.listdir())
            SFTP.notebook_ls(sftp, results, show_id=opts.show_id)
