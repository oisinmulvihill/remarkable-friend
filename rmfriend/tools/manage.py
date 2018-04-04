# -*- coding: utf-8 -*-
"""
"""
import sys
import logging
import logging.config

from rmfriend.tools.admincommands import AdminCommands


def main():
    """
    """
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': (
                    '%(asctime)s %(name)s.%(funcName)s %(levelname)s '
                    '%(message)s'
                )
            },
        },
        'handlers': {
            'default': {
                'level': 'NOTSET',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': True
            },
            'botocore': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': False
            },
            'paramiko': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': False
            },
            'paramiko.transport': {
                'handlers': ['default'],
                'level': 'ERROR',
                'propagate': False
            },
            'rmfriend.tools.sftp.SFTP.connect': {
                'handlers': ['default'],
                'level': 'ERROR',
                'propagate': False
            },
        }
    }

    logging.config.dictConfig(config)
    log = logging.getLogger()
    while True:
        try:
            sys.exit(AdminCommands().main())

        except KeyboardInterrupt:
            log.info("Exit time.")
            break
