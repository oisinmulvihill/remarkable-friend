# -*- coding: utf-8 -*-
"""
Manages user's configuration

"""
import os
import configparser
from pathlib import Path


def rmfriend_dir():
    """Returns the directory which will contain the configuration and cache."""
    return Path.home() / '.rmfriend'


def notebook_cache_director():
    """Return the path to the .rmfriend/notebooks in the user's home."""
    return str(rmfriend_dir() / 'notebooks')


def config_file_and_path():
    """Return the path to the .rmfriend.cfg file in the user's home."""
    return str(rmfriend_dir() / 'config.cfg')


def recover_or_create():
    """Recover or create the configuration if its not present.

    This will set up the configuration file and cache directory if not present.

    :returns: A configparser.ConfigParser instance.

    This will have the 'rmfriend' section with the configuration fields

        - address
        - port
        - username
        - cache_dir

    """
    cache_dir = notebook_cache_director()
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    config_file = config_file_and_path()
    if not os.path.isfile(config_file):
        config = configparser.ConfigParser()
        config['rmfriend'] = {
            'address': '10.11.99.1',
            'port': '22',
            'username': 'root',
            'cache_dir': cache_dir
        }
        with open(config_file, 'w') as fd:
            config.write(fd)

    else:
        config = configparser.ConfigParser()
        config.read(config_file)

    return config
