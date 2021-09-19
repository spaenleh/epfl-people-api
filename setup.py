#!/usr/bin/env python3

import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

PACKAGE_NAME = "epflpeople"
README = (HERE / "README.md").read_text()
CHANGELOG = (HERE / "CHANGELOG.md").read_text()
LONG_DESCRIPTION = README + CHANGELOG
VERSION = (HERE / PACKAGE_NAME / "VERSION").read_text().strip()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="EPFL People API wrapper for python",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/spaenleh/epfl-people-api",
    author="spaenleh",
    author_email="spaenleh@gmail.com",
    classifiers=["License :: OSI Approved :: MIT License"],
    packages=[PACKAGE_NAME],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            f"{PACKAGE_NAME}={PACKAGE_NAME}.__main__:main",
            f"{PACKAGE_NAME}_pretty={PACKAGE_NAME}.__main__:main_highlighted",
        ]
    },
    project_urls={
        "Documentation": "https://github.com/spaenleh/epfl-people-api/blob/main/README.md",
        "Github": "https://github.com/spaenleh/epfl-people-api",
        "Changelog": "https://github.com/spaenleh/epfl-people-api/blob/main/CHANGELOG.md",
    },
)
