import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

PACKAGE_NAME = "epflpeople"
README = (HERE / "README.md").read_text()
VERSION = (HERE / PACKAGE_NAME / "VERSION").read_text().strip()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="EPFL People API wrapper for python",
    long_description=README,
    long_description_content_type="text/markdown",
    # TODO: add project url on Github
    url="",
    author="spaenleh",
    author_email="spaenleh@gmail.com",
    license="MIT",
    classifiers=["License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
    packages=[PACKAGE_NAME],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            f"{PACKAGE_NAME}={PACKAGE_NAME}.__main__:main",
        ]
    },
)

