#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: setup.py

:Synopsis:

:Author:
    servilla

:Created:
    6/23/2020
"""
from os import path
from setuptools import find_packages, setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'LICENSE'), encoding='utf-8') as f:
    full_license = f.read()

setup(
    name="load",
    version="2020.06.23",
    description="Load test web service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mark Servilla",
    url="https://github.com/servilla/Load",
    license=full_license,
    packages=find_packages(where="src"),
    include_package_data=True,
    exclude_package_data={"": ["settings.py, properties.py, config.py"],},
    package_dir={"": "src"},
    python_requires=">3.8.*",
    install_requires=[
        "click >= 7.1.2",
        "daiquiri >= 2.1.1",
        ],
    entry_points={"console_scripts": ["load=Load.load:main"]},
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
)


def main():
    return 0


if __name__ == "__main__":
    main()
