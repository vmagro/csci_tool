#!/usr/bin/env python3
# Copyright (c) 2017-present, Vinnie Magro
# All rights reserved.

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='csci',
    version='0.1',
    description='A tool for managing USC CSCI course GitHub repos',
    long_description=long_description,
    author='Vinnie Magro',
    author_email='smagro@usc.edu',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='usc csci github',
    url='https://www.github.com/vmagro/csci-tool',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'jinja2', 'gitpython'
    ],
    tests_require=[
        'pytest', 'pytest-cov', 'coverage', 'mock', 'pyfakefs', 'pytest-mock',
    ],
    setup_requires=[
        'pytest-runner', 'flake8'
    ],
    entry_points={
        'console_scripts': ['csci=csci_tool.main:main'],
    },
)
