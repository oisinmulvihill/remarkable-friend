# -*- coding: utf-8 -*-
"""
"""
import os
import logging
import pathlib

import pytest


@pytest.fixture(scope='session')
def logger(request):
    """Set up a root logger showing all entries in the console.
    """
    log = logging.getLogger()
    hdlr = logging.StreamHandler()
    fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt)
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)
    log.propagate = False

    return log


def example_file(extension, open_as):
    """Recover the data the example files dependingon the extension.

    examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.(
        lines|content|pagedata|metadata
    )


    """
    tests_dir = os.path.split(__file__)[0]
    lines_file = os.path.join(
        tests_dir,
        'examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.{}'.format(extension)
    )
    with open(lines_file, open_as) as fd:
        raw_binary = fd.read()
    return raw_binary


@pytest.fixture(scope='function')
def lines(request):
    return example_file('lines', 'rb')


example_lines_file = lines


@pytest.fixture(scope='function')
def metadata(request):
    return example_file('metadata', 'r')


@pytest.fixture(scope='function')
def pagedata(request):
    return example_file('pagedata', 'r')


@pytest.fixture(scope='function')
def content(request):
    return example_file('content', 'r')


@pytest.fixture(scope='function')
def triangle_notebook():
    """Recover all the parts from the 'triangle' notebook.

    examples/0e7143f2-e82d-4402-8eb5-39811ddbb936.(
        lines|content|pagedata|metadata|thumbnails|cache
    )

    :returns: A dict with all the parts.

    """
    document_id = '0e7143f2-e82d-4402-8eb5-39811ddbb936'

    tests_dir = pathlib.Path(os.path.split(__file__)[0])
    examples_dir = tests_dir / 'examples'

    def get_(extension):
        filename = str(examples_dir / '{}.{}'.format(document_id, extension))
        open_as = 'r'
        if extension == 'lines':
            open_as = 'rb'

        if extension in ('thumbnails', 'cache'):
            dirname = pathlib.Path(filename)
            if dirname.is_dir():
                data = [item.name for item in dirname.iterdir()]
            else:
                data = []

        else:
            with open(filename, open_as) as fd:
                data = fd.read()

        return data

    return {
        'document_id': document_id,
        'lines': get_('lines'),
        'metadata': get_('metadata'),
        'pagedata': get_('pagedata'),
        'content': get_('content'),
        'thumbnails': get_('thumbnails'),
        'cache': get_('cache'),
    }


@pytest.fixture(scope='function')
def sftp_listing(request):
    """
    """
    tests_dir = os.path.split(__file__)[0]
    lines_file = os.path.join(
        tests_dir, u'examples/sftp_listing.txt'
    )
    with open(lines_file, 'r') as fd:
        sftp_listing = fd.readlines()
    return sftp_listing
