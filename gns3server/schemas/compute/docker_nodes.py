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

from typing import List
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from ..common import AuxType, ConsoleType, CustomAdapter, ExtraConfig, NodeStatus


class DockerBase(BaseModel):
    """
    Common Docker node properties.
    """

    @field_validator("start_command", "environment", "extra_hosts", "startup_config_content", mode="before")
    @classmethod
    def _empty_string_to_none(cls, value):
        # Web clients serialize empty form fields as "" while unset values are
        # stored as None on the node: normalize before the update diff runs,
        # otherwise every full PUT would see a phantom change and recreate
        # the container for nothing.
        return value or None

    @field_validator("console_http_path", mode="before")
    @classmethod
    def _empty_string_to_root_path(cls, value):
        # the canonical "no path" value is "/" (the creation default)
        return value or "/"

    name: str | None = None
    image: str | None = Field(None, description="Docker image name")
    node_id: UUID | None = None
    console: int | None = Field(None, gt=0, le=65535, description="Console TCP port")
    console_type: ConsoleType | None = Field(None, description="Console type")
    console_resolution: str | None = Field(None, pattern="^[0-9]+x[0-9]+$", description="Console resolution for VNC")
    console_http_port: int | None = Field(None, description="Internal port in the container for the HTTP server")
    console_http_path: str | None = Field(None, description="Path of the web interface")
    aux: int | None = Field(None, gt=0, le=65535, description="Auxiliary TCP port")
    aux_type: AuxType | None = Field(None, description="Auxiliary console type")
    usage: str | None = Field(None, description="How to use the Docker container")
    start_command: str | None = Field(None, description="Docker CMD entry")
    adapters: int | None = Field(None, ge=0, le=99, description="Number of adapters")
    mac_address: str | None = Field(
        None, description="Base MAC address", pattern="^([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})$"
    )
    environment: str | None = Field(None, description="Docker environment variables")
    extra_hosts: str | None = Field(None, description="Docker extra hosts (added to /etc/hosts)")
    extra_volumes: List[str] | None = Field(None, description="Additional directories to make persistent")
    extra_configs: List[ExtraConfig] | None = Field(
        None, description="Configuration files injected into the container (bind-mounted read-only)"
    )
    startup_config_content: str | None = Field(
        None, description="Startup-config content (IOL runner images: materialized into the node's NVRAM at start)"
    )
    memory: int | None = Field(None, ge=0, description="Maximum amount of memory the container can use in MB")
    cpus: float | None = Field(None, ge=0, description="Maximum amount of CPU resources the container can use")
    custom_adapters: List[CustomAdapter] | None = Field(None, description="Custom adapters")


class DockerCreate(DockerBase):
    """
    Properties to create a Docker node.
    """

    name: str
    image: str = Field(..., description="Docker image name")
    application_id: int | None = Field(
        None, ge=1, le=1022, description="IOL application ID for iol-runner images (allocated by the controller)"
    )
    image_digest: str | None = Field(
        None,
        pattern=r"^sha256:[a-f0-9]{64}$",
        description="Image id the controller expects for 'image' (sha256:<hex>, resolved from the Docker "
        "daemon on the controller host). When set and the compute holds a different image "
        "under the same tag, the image is reported as missing so the controller re-syncs it",
    )


class DockerUpdate(DockerBase):
    """
    Properties to update a Docker node.
    """

    pass


class Docker(DockerBase):
    name: str
    image: str = Field(..., description="Docker image name")
    container_id: str = Field(
        ..., min_length=12, max_length=64, pattern="^[a-f0-9]+$", description="Docker container ID (read only)"
    )
    project_id: UUID = Field(..., description="Project ID")
    node_directory: str = Field(..., description="Path to the node working directory (read only)")
    status: NodeStatus = Field(..., description="Container status (read only)")
