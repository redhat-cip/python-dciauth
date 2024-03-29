#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017-2023 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import os
import setuptools
import subprocess

# dcibuild can be loaded only when doing the sdist sub-command because
# dci-packaging is extracted at the same level. When doing the other
# sub-commands like build, we extract the version from version.py.
try:
    from dcibuild import sdist, get_version

    sdist.dci_mod = "dciauth"
except:
    sdist = None

    def get_version():
        from dciauth import version

        return version.__version__


root_dir = os.path.dirname(os.path.abspath(__file__))
readme = open(os.path.join(root_dir, "README.md")).read()


setuptools.setup(
    name="dciauth",
    version=get_version(),
    packages=["dciauth", "dciauth.v2"],
    author="Distributed CI team",
    author_email="distributed-ci@redhat.com",
    description="DCI authentication module used by dci-control-server and python-dciclient",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=[],
    url="https://github.com/redhat-cip/python-dciauth",
    license="Apache v2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Security :: Cryptography",
    ],
    cmdclass={
        "sdist": sdist,
    },
)
