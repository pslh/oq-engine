# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2010-2011, GEM Foundation.
#
# OpenQuake is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with OpenQuake.  If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.


"""
Unit tests for the utils.version module.
"""


import unittest

from openquake.utils import version


class VersionInfoTestCase(unittest.TestCase):
    """Tests the behaviour of utils.version.info()."""

    def __init__(self, *args, **kwargs):
        super(VersionInfoTestCase, self).__init__(*args, **kwargs)
        self.maxDiff = None

    def test_info_with_major_number_only(self):
        """Only the major version number is set."""
        self.assertEqual(
            "OpenQuake version 2", version.info((2, -1, -1, -1)))

    def test_info_with_minor_number_only(self):
        """Only the minor version number is set."""
        self.assertEqual(
            "OpenQuake version 0.2", version.info((-1, 2, -1, -1)))

    def test_info_with_sprint_number_only(self):
        """Only the sprint number is set."""
        self.assertEqual(
            "OpenQuake version 0.0.2", version.info((-1, -1, 2, -1)))

    def test_info_with_all_data_in_place(self):
        """All the version information is in place."""
        self.assertEqual(
            "OpenQuake version 0.3.2 releaased on 08 Apr 2011 08:04:06 +0200",
            version.info((0, 3, 2, 1302242651)))

    def test_info_with_malformed_version_information(self):
        """The version information is malformed."""
        self.assertEqual(
            "The OpenQuake version is not available.", version.info((-1,)))