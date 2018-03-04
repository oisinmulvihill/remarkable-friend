# -*- coding: utf-8 -*-
"""
"""
import os
import logging

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


@pytest.fixture(scope='function')
def example_lines_file(request):
    """
    """
    tests_dir = os.path.split(__file__)[0]
    lines_file = os.path.join(
        tests_dir, u'examples/aa90b0e7-5c1a-42fe-930f-dad9cf3363cc.lines'
    )
    with open(lines_file, 'rb', buffering=0) as fd:
        raw_binary = fd.read()
    return raw_binary
