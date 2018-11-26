"""setup.py"""
import re
import os
import codecs
import textwrap
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

DEPENDENCIES = (
    "google-auth-oauthlib",
    "google-auth",
    "google-api-python-client",
    "retrying",
    "ratelimit",
)


def read(*parts):
    """read"""
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    """find_version"""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="gtm-manager",
    version=find_version("gtm_manager", "__init__.py"),
    description="An object-oriented helper library wrapping the Tag Manager API Client Library for Python.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=["gtm_manager"],
    author="Trakken Web Services",
    author_email="christian@trakken.de",
    classifiers=textwrap.dedent(
        """
        Development Status :: 4 - Beta
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Programming Language :: Python :: 3.7
        License :: OSI Approved :: MIT License
    """
    )
    .strip()
    .splitlines(),
    keywords=["gtm", "google tag manager"],
    install_requires=DEPENDENCIES,
    extras_require={
        "tests": ["pytest"],
        "docs": ["sphinx >= 1.8.2", "sphinx_rtd_theme"],
    },
)
