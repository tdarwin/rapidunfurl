#!/usr/bin/env python
# -*- coding: utf-8 -*-

# For a fully annotated version of this file and what it does, see
# https://github.com/pypa/sampleproject/blob/master/setup.py

# To upload this file to PyPI you must build it then upload it:
# python setup.py sdist bdist_wheel  # build in 'dist' folder
# python-m twine upload dist/*  # 'twine' must be installed: 'pip install twine'


import io
import os
from setuptools import find_packages, setup

DEPENDENCIES = ['pyquery', 'requests', 'uritools', 'micawber']
EXCLUDE_FROM_PACKAGES = ["contrib", "docs", "tests*"]
CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


setup(
    name="rapidunfurl",
    version='0.0.1',
    author="Davin Taddeo",
    author_email="pyunfurl@unfurl.dev",
    description="library designed to pull and process metadata very quickly to unfurl URL contents into a JSON object that can the be used by other programs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tdarwin/rapidunfurl",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    install_requires=DEPENDENCIES,
    test_suite="tests.test_project",
    python_requires=">=3.6",
    # license and classifier list:
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    license="License :: OSI Approved :: MIT License",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
