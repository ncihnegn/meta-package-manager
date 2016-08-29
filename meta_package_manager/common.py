# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Kevin Deldycke <kevin@deldycke.com>
#                    and contributors.
# All Rights Reserved.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

""" Common operations to all package managers. """

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

import inspect
from glob import glob
from importlib import import_module
from os import path

from . import logger
from .base import PackageManager


_package_managers = {}


def package_managers():
    """ Search for package manager definitions locally and return a dict. """
    if not _package_managers:

        here = path.dirname(path.abspath(__file__))

        for py_file in glob(path.join(here, '*.py')):
            module_name = path.splitext(path.basename(py_file))[0]
            logger.debug(
                "Search for package manager definitions in {}".format(py_file))
            module = import_module(
                '.{}'.format(module_name), package=__package__)
            for klass_id, klass in inspect.getmembers(module, inspect.isclass):
                if issubclass(
                        klass, PackageManager) and klass is not PackageManager:
                    manager = klass()
                    _package_managers[manager.id] = manager

    return _package_managers