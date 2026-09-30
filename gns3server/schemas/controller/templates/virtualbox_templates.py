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

from gns3server.schemas.compute.virtualbox_nodes import (
    CustomAdapter,
    VirtualBoxAdapterType,
    VirtualBoxConsoleType,
    VirtualBoxOnCloseAction,
)

from . import Category, TemplateBase


class VirtualBoxTemplateBase(TemplateBase):
    category: Category | None = Category.guest
    default_name_format: str | None = "{name}-{0}"
    symbol: str | None = "vbox_guest"
    vmname: str | None = Field(None, description="VirtualBox VM name (in VirtualBox itself)")
    ram: int | None = Field(256, gt=0, description="Amount of RAM in MB")
    linked_clone: bool | None = Field(False, description="Whether the VM is a linked clone or not")
    adapters: int | None = Field(
        1, ge=0, le=36, description="Number of adapters"
    )  # 36 is the maximum given by the ICH9 chipset in VirtualBox
    use_any_adapter: bool | None = Field(False, description="Allow GNS3 to use any VirtualBox adapter")
    adapter_type: VirtualBoxAdapterType | None = Field(
        VirtualBoxAdapterType.intel_pro_1000_mt_desktop, description="VirtualBox adapter type"
    )
    first_port_name: str | None = Field("", description="Optional name of the first networking port example: eth0")
    port_name_format: str | None = Field(
        "Ethernet{0}", description="Optional formatting of the networking port example: eth{0}"
    )
    port_segment_size: int | None = Field(
        0,
        description="Optional port segment size. A port segment is a block of port. For example Ethernet0/0 Ethernet0/1 is the module 0 with a port segment size of 2",
    )
    headless: bool | None = Field(False, description="Headless mode")
    on_close: VirtualBoxOnCloseAction | None = Field(
        VirtualBoxOnCloseAction.power_off, description="Action to execute on the VM is closed"
    )
    console_type: VirtualBoxConsoleType | None = Field(VirtualBoxConsoleType.none, description="Console type")
    console_auto_start: bool | None = Field(
        False, description="Automatically start the console when the node has started"
    )
    custom_adapters: list[CustomAdapter] | None = Field(default_factory=list, description="Custom adapters")


class VirtualBoxTemplate(VirtualBoxTemplateBase):
    vmname: str = Field(..., description="VirtualBox VM name (in VirtualBox itself)")


class VirtualBoxTemplateUpdate(VirtualBoxTemplateBase):
    pass
