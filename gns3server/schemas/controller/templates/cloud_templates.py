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


from pydantic import Field

from gns3server.schemas.compute.cloud_nodes import CloudConsoleType, EthernetPort, TAPPort, UDPPort

from . import Category, TemplateBase


class CloudTemplate(TemplateBase):
    category: Category | None = Category.guest
    default_name_format: str | None = "Cloud{0}"
    symbol: str | None = "cloud"
    ports_mapping: list[EthernetPort | TAPPort | UDPPort] = Field(default_factory=list)
    remote_console_host: str | None = Field("127.0.0.1", description="Remote console host or IP")
    remote_console_port: int | None = Field(23, gt=0, le=65535, description="Remote console TCP port")
    remote_console_type: CloudConsoleType | None = Field(CloudConsoleType.none, description="Remote console type")
    remote_console_http_path: str | None = Field("/", description="Path of the remote web interface")


class CloudTemplateUpdate(CloudTemplate):
    pass
