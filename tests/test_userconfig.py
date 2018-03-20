# -*- coding: utf-8 -*-
"""
"""
from pathlib import Path as RPath
from unittest.mock import patch

from rmfriend import userconfig


@patch('rmfriend.userconfig.Path')
def test_config_file_path(Path):
    """Test the function that works out the file and path for the config.
    """
    Path.home.side_effect = lambda: RPath('/my/home/directory')
    result = userconfig.config_file_and_path()
    assert result == '/my/home/directory/.rmfriend/config.cfg'


@patch('rmfriend.userconfig.Path')
def test_notebook_cache_directory(Path):
    """Test the function that works out the file and path for the config.
    """
    Path.home.side_effect = lambda: RPath('/my/home/directory')
    result = userconfig.notebook_cache_director()
    assert result == '/my/home/directory/.rmfriend/notebooks'


@patch('rmfriend.userconfig.Path')
def test_recover_or_create(Path, tmpdir):
    """Test the function that works out the file and path for the config.
    """
    Path.home.side_effect = lambda: tmpdir

    cfg = userconfig.recover_or_create()
    base_dir = tmpdir / '.rmfriend'
    assert base_dir.isdir()

    notebooks = base_dir / 'notebooks'
    assert notebooks.isdir()

    config_file = base_dir / 'config.cfg'
    assert config_file.isfile()

    assert 'rmfriend' in cfg
    assert cfg['rmfriend']['address'] == '10.11.99.1'
    assert cfg['rmfriend']['port'] == '22'
    assert cfg['rmfriend']['username'] == 'root'
    assert cfg['rmfriend']['cache_dir'] == str(notebooks)

    # Calling the second time will re-read from the already present config
    # file so there should be no problems.
    cfg = userconfig.recover_or_create()
    assert 'rmfriend' in cfg
    assert cfg['rmfriend']['address'] == '10.11.99.1'
    assert cfg['rmfriend']['port'] == '22'
    assert cfg['rmfriend']['username'] == 'root'
    assert cfg['rmfriend']['cache_dir'] == str(notebooks)
