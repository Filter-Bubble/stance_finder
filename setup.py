#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

test_deps = [
    'pytest',
    'pytest-cov',
    'pycodestyle',
]

__version__ = None
with open(os.path.join(os.path.dirname(__file__), 'stance_finder/__version__.py')) as versionpy:
    exec(versionpy.read())

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='stance_finder',
    version=__version__,
    description="Python module for finding (candidate) stances in Dutch news articles",
    long_description=readme + '\n\n',
    author="Dafne van Kuppevelt",
    author_email='d.vankuppevelt@esciencecenter.nl',
    url='https://github.com/Filter-Bubble/stance_finder',
    packages=[
        'stance_finder',
    ],
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='stance_finder',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    install_requires=[
        "stanza",
        "e2e-Dutch",
        "stroll-srl",
        "amcatclient"],
    setup_requires=[
        # dependency for `python setup.py test`
        'pytest-runner',
        # dependencies for `python setup.py build_sphinx`
        'sphinx',
        'sphinx_rtd_theme',
        'recommonmark'
    ],
    dependency_links=['http://github.com/Filter-Bubble/strol/tarball/master#egg=stroll-srl'],
    tests_require=test_deps,
    extras_require={
        'dev':  ['prospector[with_pyroma]', 'yapf', 'isort'] + test_deps,
    },
    data_files=[('citation/stance_finder', ['CITATION.cff'])]
)
