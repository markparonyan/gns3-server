#!/usr/bin/env python
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gns3server.utils import *  # noqa: F403


def test_force_unix_path():
    assert force_unix_path("a/b") == "a/b"  # noqa: F405
    assert force_unix_path("a\\b") == "a/b"  # noqa: F405
    assert force_unix_path("a\\b\\..\\c") == "a/c"  # noqa: F405
    assert force_unix_path(r"C:\Temp") == r"C:/Temp"  # noqa: F405
    assert force_unix_path(force_unix_path(r"C:\Temp")) == r"C:/Temp"  # noqa: F405
    assert force_unix_path("a//b") == "a/b"  # noqa: F405


def test_macaddress_to_int():
    assert macaddress_to_int("00:0c:29:11:b0:0a") == 52228632586  # noqa: F405


def test_int_to_macaddress():
    assert int_to_macaddress(52228632586) == "00:0c:29:11:b0:0a"  # noqa: F405


def test_parse_version():
    assert parse_version("1") == ("000001", "00000", "000000", "final")  # noqa: F405
    assert parse_version("1.3") == ("000001", "000003", "000000", "final")  # noqa: F405
    assert parse_version("1.3.dev3") == ("000001", "000003", "000000", "dev", "000003")  # noqa: F405
    assert parse_version("1.3a1") == ("000001", "000003", "000000", "a", "000001")  # noqa: F405
    assert parse_version("1.3rc1") == ("000001", "000003", "000000", "c", "000001")  # noqa: F405

    assert parse_version("1.2.3") > parse_version("1.2.2")  # noqa: F405
    assert parse_version("1.3") > parse_version("1.2.2")  # noqa: F405
    assert parse_version("1.3") > parse_version("1.3alpha1")  # noqa: F405
    assert parse_version("1.3") > parse_version("1.3rc1")  # noqa: F405
    assert parse_version("1.3rc1") > parse_version("1.3alpha3")  # noqa: F405
    assert parse_version("1.3dev1") > parse_version("1.3rc1")  # noqa: F405
    assert parse_version("1.2.3") > parse_version("1.2")  # noqa: F405
