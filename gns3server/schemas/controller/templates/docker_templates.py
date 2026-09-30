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

from pydantic import Field

from ...common import AuxType, ConsoleType, CustomAdapter, ExtraConfig
from . import Category, TemplateBase


class DockerTemplateBase(TemplateBase):
    category: Category | None = Category.guest
    default_name_format: str | None = "{name}-{0}"
    symbol: str | None = "docker_guest"
    image: str | None = Field(None, description="Docker image name")
    adapters: int | None = Field(1, ge=0, le=100, description="Number of adapters")
    mac_address: str | None = Field(
        "", description="Base MAC address", pattern="^([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})$|^$"
    )
    start_command: str | None = Field("", description="Docker CMD entry")
    environment: str | None = Field("", description="Docker environment variables")
    console_type: ConsoleType | None = Field(ConsoleType.telnet, description="Console type")
    aux_type: AuxType | None = Field(AuxType.none, description="Auxiliary console type")
    console_auto_start: bool | None = Field(
        False, description="Automatically start the console when the node has started"
    )
    console_http_port: int | None = Field(
        80, gt=0, le=65535, description="Internal port in the container for the HTTP server"
    )
    console_http_path: str | None = Field(
        "/",
        description="Path of the web interface",
    )
    console_resolution: str | None = Field(
        "1024x768", pattern="^[0-9]+x[0-9]+$", description="Console resolution for VNC"
    )
    extra_hosts: str | None = Field("", description="Docker extra hosts (added to /etc/hosts)")
    extra_volumes: List | None = Field([], description="Additional directories to make persistent")
    extra_configs: List[ExtraConfig] | None = Field(
        default_factory=list, description="Configuration files injected into the container (bind-mounted read-only)"
    )
    memory: int | None = Field(0, ge=0, description="Maximum amount of memory the container can use in MB")
    cpus: float | None = Field(0, ge=0, description="Maximum amount of CPU resources the container can use")
    custom_adapters: List[CustomAdapter] | None = Field(default_factory=list, description="Custom adapters")


class DockerTemplate(DockerTemplateBase):
    image: str = Field(..., description="Docker image name")


class DockerTemplateUpdate(DockerTemplateBase):
    pass
