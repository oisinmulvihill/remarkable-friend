# -*- coding: utf-8 -*-
"""
"""
from setuptools import setup, find_packages

with open('requirements.txt') as fd:
    requirements = fd.readlines()

with open('test-requirements.txt') as fd:
    test_requirements = fd.readlines()


setup(
    name='remarkable-friend',
    packages=find_packages(),
    setup_requires=[],
    install_requires=requirements,
    entry_points={
        'console_scripts': 'rmfriend=rmfriend.tools.manage:main'
    },
)
