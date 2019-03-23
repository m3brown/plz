#!/usr/bin/env python
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="plz-cmd",
    description="command line app for running configurable shell commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.5.1",
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=['plz'],
    install_requires=[
        'PyYAML>=3.0',
        'colorama>=0.3.0',
        'sh>=1.12.14',
    ],
    entry_points={
        'console_scripts': [
            'plz = plz.main:main',
        ]
    }
)
