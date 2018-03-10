# -*- coding: utf-8 -*-
"""
"""
import sys
import logging
import logging.config

from rmfriend.tools.admincommands import AdminCommands


def main():
    """onboarder cli app main.
    """
    log = logging.getLogger()
    formatter = logging.Formatter(
        (
            '%(asctime)s %(funcName)s %(name)s %(levelname)s '
            '%(message)s'
        )
    )
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)
    log.propagate = True

    while True:
        try:
            sys.exit(AdminCommands().main())

        except KeyboardInterrupt:
            log.info("Exit time.")
            break
