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

from gns3server.schemas.compute.iou_nodes import ConsoleType

from . import Category, TemplateBase


class IOUTemplateBase(TemplateBase):
    category: Category | None = Category.router
    default_name_format: str | None = "IOU{0}"
    symbol: str | None = "multilayer_switch"
    path: str | None = Field(None, description="Path of IOU executable")
    ethernet_adapters: int | None = Field(2, ge=0, description="Number of ethernet adapters")
    serial_adapters: int | None = Field(2, ge=0, description="Number of serial adapters")
    ram: int | None = Field(1024, gt=0, description="Amount of RAM in MB")
    nvram: int | None = Field(256, gt=0, description="Amount of NVRAM in KB")
    use_default_iou_values: bool | None = Field(False, description="Use default IOU values")
    startup_config: str | None = Field("iou_l3_base_startup-config.txt", description="Startup-config of IOU")
    private_config: str | None = Field("", description="Private-config of IOU")
    l1_keepalives: bool | None = Field(
        False,
        description="Enable Layer 1 keepalives so IOU interfaces report accurate link state",
    )
    console_type: ConsoleType | None = Field(ConsoleType.telnet, description="Console type")
    console_auto_start: bool | None = Field(
        False, description="Automatically start the console when the node has started"
    )


class IOUTemplate(IOUTemplateBase):
    path: str = Field(..., description="Path of IOU executable")


class IOUTemplateUpdate(IOUTemplateBase):
    pass
