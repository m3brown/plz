#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="plz",
    description="command line app for running configurable shell commands",
    version="0.1.0",
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
    packages=find_packages(exclude=('tests*')),
    install_requires=[
        'PyYAML>=3.0',
        'colorama>=0.3.0',
    ],
    entry_points={
        'console_scripts': [
            'plz = plz.main:main',
        ]
    }
)
