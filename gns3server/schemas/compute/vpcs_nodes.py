#
# Copyright (C) 2020 GNS3 Technologies Inc.
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

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from ..common import NodeStatus


class ConsoleType(str, Enum):
    """
    Supported console types.
    """

    telnet = "telnet"
    ssh = "ssh"
    none = "none"


class VPCSBase(BaseModel):
    """
    Common VPCS node properties.
    """

    name: str | None = None
    node_id: UUID | None = None
    usage: str | None = Field(None, description="How to use the node")
    console: int | None = Field(None, gt=0, le=65535, description="Console TCP port")
    console_type: ConsoleType | None = Field(None, description="Console type")
    startup_script: str | None = Field(None, description="Content of the VPCS startup script")


class VPCSCreate(VPCSBase):
    """
    Properties to create a VPCS node.
    """

    name: str


class VPCSUpdate(VPCSBase):
    """
    Properties to update a VPCS node.
    """

    pass


class VPCS(VPCSBase):
    name: str
    project_id: UUID = Field(..., description="Project ID")
    node_directory: str = Field(..., description="Path to the node working directory (read only)")
    status: NodeStatus = Field(..., description="Container status (read only)")
    command_line: str = Field(..., description="Last command line used to start VPCS")
