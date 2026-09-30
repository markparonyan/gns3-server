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

from pydantic import BaseModel, Field, HttpUrl


class ProjectStatus(str, Enum):
    """
    Supported project statuses.
    """

    opened = "opened"
    closed = "closed"


class Supplier(BaseModel):
    logo: str = Field(..., description="Path to the project supplier logo")
    url: HttpUrl | None = Field(None, description="URL to the project supplier site")


class Variable(BaseModel):
    name: str = Field(..., description="Variable name")
    value: str | None = Field(None, description="Variable value")


class ProjectBase(BaseModel):
    """
    Common properties for projects.
    """

    name: str | None = None
    project_id: UUID | None = None
    path: str | None = Field(None, description="Project directory")
    auto_close: bool | None = Field(None, description="Close project when last client leaves")
    auto_open: bool | None = Field(None, description="Project opens when GNS3 starts")
    auto_start: bool | None = Field(None, description="Project starts when opened")
    scene_height: int | None = Field(None, description="Height of the drawing area")
    scene_width: int | None = Field(None, description="Width of the drawing area")
    zoom: int | None = Field(None, description="Zoom of the drawing area")
    show_layers: bool | None = Field(None, description="Show layers on the drawing area")
    snap_to_grid: bool | None = Field(None, description="Snap to grid on the drawing area")
    show_grid: bool | None = Field(None, description="Show the grid on the drawing area")
    grid_size: int | None = Field(None, description="Grid size for the drawing area for nodes")
    drawing_grid_size: int | None = Field(None, description="Grid size for the drawing area for drawings")
    show_interface_labels: bool | None = Field(None, description="Show interface labels on the drawing area")
    supplier: Supplier | None = Field(None, description="Supplier of the project")
    variables: list[Variable] | None = Field(None, description="Variables required to run the project")


class ProjectCreate(ProjectBase):
    """
    Properties for project creation.
    """

    name: str


class ProjectDuplicate(ProjectBase):
    """
    Properties for project duplication.
    """

    name: str
    reset_mac_addresses: bool | None = Field(False, description="Reset MAC addresses for this project")


class ProjectUpdate(ProjectBase):
    """
    Properties for project update.
    """

    pass


class Project(ProjectBase):
    project_id: UUID
    status: ProjectStatus | None = None
    filename: str | None = None
    created_by: str | None = Field(None, description="Username of the user who created the project")


class ProjectFile(BaseModel):
    path: str = Field(..., description="File path")
    md5sum: str = Field(..., description="File checksum")


class NodeFile(BaseModel):
    """
    Detailed file information for node files.
    """

    path: str = Field(..., description="File name")
    size: int = Field(..., description="File size in bytes")
    created_at: str = Field(..., description="File creation time (ISO 8601)")
    modified_at: str = Field(..., description="File modification time (ISO 8601)")
    file_type: str = Field(..., description="File type determined by the file command")


class ProjectCompression(str, Enum):
    """
    Supported project compression.
    """

    none = "none"
    zip = "zip"
    bzip2 = "bzip2"
    lzma = "lzma"
    zstd = "zstd"
