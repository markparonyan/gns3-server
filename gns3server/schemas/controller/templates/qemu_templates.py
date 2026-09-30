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

from gns3server.schemas.compute.qemu_nodes import (
    CustomAdapter,
    QemuAdapterType,
    QemuBootPriority,
    QemuConsoleType,
    QemuDiskInterfaceType,
    QemuOnCloseAction,
    QemuPlatform,
    QemuProcessPriority,
)

from . import Category, TemplateBase


class QemuTemplate(TemplateBase):
    category: Category | None = Category.guest
    default_name_format: str | None = "{name}-{0}"
    symbol: str | None = "qemu_guest"
    qemu_path: str | None = Field("", description="Qemu executable path")
    platform: QemuPlatform | None = Field(QemuPlatform.x86_64, description="Platform to emulate")
    linked_clone: bool | None = Field(True, description="Whether the VM is a linked clone or not")
    ram: int | None = Field(256, gt=0, description="Amount of RAM in MB")
    cpus: int | None = Field(1, ge=1, le=255, description="Number of vCPUs")
    maxcpus: int | None = Field(1, ge=1, le=255, description="Maximum number of hotpluggable vCPUs")
    adapters: int | None = Field(1, ge=0, le=275, description="Number of adapters")
    adapter_type: QemuAdapterType | None = Field(QemuAdapterType.e1000, description="QEMU adapter type")
    mac_address: str | None = Field(
        "", description="QEMU MAC address", pattern="^([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})$|^$"
    )
    first_port_name: str | None = Field("", description="Optional name of the first networking port example: eth0")
    port_name_format: str | None = Field(
        "Ethernet{0}", description="Optional formatting of the networking port example: eth{0}"
    )
    port_segment_size: int | None = Field(
        0,
        description="Optional port segment size. A port segment is a block of port. For example Ethernet0/0 Ethernet0/1 is the module 0 with a port segment size of 2",
    )
    console_type: QemuConsoleType | None = Field(QemuConsoleType.telnet, description="Console type")
    console_auto_start: bool | None = Field(
        False, description="Automatically start the console when the node has started"
    )
    aux_type: QemuConsoleType | None = Field(QemuConsoleType.none, description="Auxiliary console type")
    boot_priority: QemuBootPriority | None = Field(QemuBootPriority.c, description="QEMU boot priority")
    hda_disk_image: str | None = Field("", description="QEMU hda disk image path")
    hda_disk_interface: QemuDiskInterfaceType | None = Field(
        QemuDiskInterfaceType.none, description="QEMU hda interface"
    )
    hdb_disk_image: str | None = Field("", description="QEMU hdb disk image path")
    hdb_disk_interface: QemuDiskInterfaceType | None = Field(
        QemuDiskInterfaceType.none, description="QEMU hdb interface"
    )
    hdc_disk_image: str | None = Field("", description="QEMU hdc disk image path")
    hdc_disk_interface: QemuDiskInterfaceType | None = Field(
        QemuDiskInterfaceType.none, description="QEMU hdc interface"
    )
    hdd_disk_image: str | None = Field("", description="QEMU hdd disk image path")
    hdd_disk_interface: QemuDiskInterfaceType | None = Field(
        QemuDiskInterfaceType.none, description="QEMU hdd interface"
    )
    cdrom_image: str | None = Field("", description="QEMU cdrom image path")
    initrd: str | None = Field("", description="QEMU initrd path")
    kernel_image: str | None = Field("", description="QEMU kernel image path")
    bios_image: str | None = Field("", description="QEMU bios image path")
    kernel_command_line: str | None = Field("", description="QEMU kernel command line")
    replicate_network_connection_state: bool | None = Field(
        True, description="Replicate the network connection state for links in Qemu"
    )
    create_config_disk: bool | None = Field(
        False, description="Automatically create a config disk on HDD disk interface (secondary slave)"
    )
    tpm: bool | None = Field(False, description="Enable Trusted Platform Module (TPM)")
    uefi: bool | None = Field(False, description="Enable UEFI boot mode")
    on_close: QemuOnCloseAction | None = Field(
        QemuOnCloseAction.power_off, description="Action to execute on the VM is closed"
    )
    cpu_throttling: int | None = Field(0, ge=0, le=800, description="Percentage of CPU allowed for QEMU")
    process_priority: QemuProcessPriority | None = Field(
        QemuProcessPriority.normal, description="Process priority for QEMU"
    )
    options: str | None = Field("", description="Additional QEMU options")
    custom_adapters: List[CustomAdapter] | None = Field(default_factory=list, description="Custom adapters")


class QemuTemplateUpdate(QemuTemplate):
    pass
