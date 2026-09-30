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


class VMwareConsoleType(str, Enum):
    """
    Supported console types.
    """

    telnet = "telnet"
    ssh = "ssh"
    none = "none"


class VMwareOnCloseAction(str, Enum):
    """
    Supported actions when closing VMware VM.
    """

    power_off = "power_off"
    shutdown_signal = "shutdown_signal"
    save_vm_state = "save_vm_state"


class VMwareAdapterType(str, Enum):
    """
    Supported VMware VM adapter types.
    """

    default = "default"
    e1000 = "e1000"
    e1000e = "e1000e"
    flexible = "flexible"
    vlance = "vlance"
    vmxnet = "vmxnet"
    vmxnet2 = "vmxnet2"
    vmxnet3 = "vmxnet3"


class VMwareBase(BaseModel):
    """
    Common VMware node properties.
    """

    name: str | None = None
    vmx_path: str | None = None
    linked_clone: bool | None = None
    node_id: UUID | None = None
    usage: str | None = Field(None, description="How to use the node")
    console: int | None = Field(None, gt=0, le=65535, description="Console TCP port")
    console_type: VMwareConsoleType | None = Field(None, description="Console type")
    headless: bool | None = Field(None, description="Headless mode")
    on_close: VMwareOnCloseAction | None = Field(None, description="Action to execute on the VM is closed")
    # 10 adapters is the maximum supported by VMware VMs.
    adapters: int | None = Field(None, ge=0, le=10, description="Number of adapters")
    adapter_type: VMwareAdapterType | None = Field(None, description="VMware adapter type")
    use_any_adapter: bool | None = Field(None, description="Allow GNS3 to use any VMware adapter")
    custom_adapters: list[CustomAdapter] | None = Field(None, description="Custom adpaters")


class VMwareCreate(VMwareBase):
    """
    Properties to create a VMware node.
    """

    name: str
    vmx_path: str = Field(..., description="Path to the vmx file")
    linked_clone: bool = Field(..., description="Whether the VM is a linked clone or not")


class VMwareUpdate(VMwareBase):
    """
    Properties to update a VMware node.
    """

    pass


class VMware(VMwareBase):
    name: str
    vmx_path: str = Field(..., description="Path to the vmx file")
    linked_clone: bool = Field(..., description="Whether the VM is a linked clone or not")
    project_id: UUID = Field(..., description="Project ID")
    node_directory: str | None = Field(None, description="Path to the node working directory (read only)")
    status: NodeStatus = Field(..., description="Container status (read only)")
