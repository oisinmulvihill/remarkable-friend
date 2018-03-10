# -*- coding: utf-8 -*-
"""
Handy command line tool working with the reMarkable tablet and manipulating
notebooks.

Oisin Mulvihill
2018-03-10

"""
import sys
import logging

import cmdln

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
