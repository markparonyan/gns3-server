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

from ..common import CustomAdapter, NodeStatus


class VirtualBoxConsoleType(str, Enum):
    """
    Supported console types.
    """

    telnet = "telnet"
    ssh = "ssh"
    none = "none"


class VirtualBoxOnCloseAction(str, Enum):
    """
    Supported actions when closing VirtualBox VM.
    """

    power_off = "power_off"
    shutdown_signal = "shutdown_signal"
    save_vm_state = "save_vm_state"


class VirtualBoxAdapterType(str, Enum):
    pcnet_pci_ii = ("PCnet-PCI II (Am79C970A)",)
    pcnet_fast_iii = ("PCNet-FAST III (Am79C973)",)
    intel_pro_1000_mt_desktop = ("Intel PRO/1000 MT Desktop (82540EM)",)
    intel_pro_1000_t_server = ("Intel PRO/1000 T Server (82543GC)",)
    intel_pro_1000_mt_server = ("Intel PRO/1000 MT Server (82545EM)",)
    paravirtualized_network = "Paravirtualized Network (virtio-net)"


class VirtualBoxBase(BaseModel):
    """
    Common VirtualBox node properties.
    """

    name: str | None = None
    vmname: str | None = None
    node_id: UUID | None = None
    linked_clone: bool | None = Field(None, description="Whether the VM is a linked clone or not")
    usage: str | None = Field(None, description="How to use the node")
    # 36 adapters is the maximum given by the ICH9 chipset in VirtualBox
    adapters: int | None = Field(None, ge=0, le=36, description="Number of adapters")
    adapter_type: VirtualBoxAdapterType | None = Field(None, description="VirtualBox adapter type")
    use_any_adapter: bool | None = Field(None, description="Allow GNS3 to use any VirtualBox adapter")
    console: int | None = Field(None, gt=0, le=65535, description="Console TCP port")
    console_type: VirtualBoxConsoleType | None = Field(None, description="Console type")
    ram: int | None = Field(None, ge=0, le=65535, description="Amount of RAM in MB")
    headless: bool | None = Field(None, description="Headless mode")
    on_close: VirtualBoxOnCloseAction | None = Field(None, description="Action to execute on the VM is closed")
    custom_adapters: list[CustomAdapter] | None = Field(None, description="Custom adapters")


class VirtualBoxCreate(VirtualBoxBase):
    """
    Properties to create a VirtualBox node.
    """

    name: str
    vmname: str = Field(..., description="VirtualBox VM name (in VirtualBox itself)")


class VirtualBoxUpdate(VirtualBoxBase):
    """
    Properties to update a VirtualBox node.
    """

    pass


class VirtualBox(VirtualBoxBase):
    name: str
    vmname: str = Field(..., description="VirtualBox VM name (in VirtualBox itself)")
    project_id: UUID = Field(..., description="Project ID")
    node_directory: str | None = Field(None, description="Path to the node working directory (read only)")
    status: NodeStatus = Field(..., description="Container status (read only)")
