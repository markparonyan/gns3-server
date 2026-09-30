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


class QemuPlatform(str, Enum):
    aarch64 = "aarch64"
    alpha = "alpha"
    arm = "arm"
    cris = "cris"
    i386 = "i386"
    lm32 = "lm32"
    m68k = "m68k"
    microblaze = "microblaze"
    microblazeel = "microblazeel"
    mips = "mips"
    mips64 = "mips64"
    mips64el = "mips64el"
    mipsel = "mipsel"
    moxie = "moxie"
    or32 = "or32"
    ppc = "ppc"
    ppc64 = "ppc64"
    ppcemb = "ppcemb"
    s390x = "s390x"
    sh4 = "sh4"
    sh4eb = "sh4eb"
    sparc = "sparc"
    sparc64 = "sparc64"
    tricore = "tricore"
    unicore32 = "unicore32"
    x86_64 = "x86_64"
    xtensa = "xtensa"
    xtensaeb = "xtensaeb"


class QemuConsoleType(str, Enum):
    """
    Supported console types.
    """

    vnc = "vnc"
    telnet = "telnet"
    ssh = "ssh"
    spice = "spice"
    spice_agent = "spice+agent"
    none = "none"


class QemuBootPriority(str, Enum):
    """
    Supported boot priority types.
    """

    c = "c"
    d = "d"
    n = "n"
    cn = "cn"
    cd = "cd"
    dn = "dn"
    dc = "dc"
    nc = "nc"
    nd = "nd"


class QemuOnCloseAction(str, Enum):
    """
    Supported actions when closing Qemu VM.
    """

    power_off = "power_off"
    shutdown_signal = "shutdown_signal"
    save_vm_state = "save_vm_state"


class QemuProcessPriority(str, Enum):
    realtime = "realtime"
    very_high = "very high"
    high = "high"
    normal = "normal"
    low = "low"
    very_low = "very low"


class QemuAdapterType(str, Enum):
    """
    Supported Qemu VM adapter types.
    """

    e1000 = "e1000"
    e1000_82544gc = "e1000-82544gc"
    e1000_82545em = "e1000-82545em"
    e1000e = "e1000e"
    i82550 = "i82550"
    i82551 = "i82551"
    i82557a = "i82557a"
    i82557b = "i82557b"
    i82557c = "i82557c"
    i82558a = "i82558a"
    i82558b = "i82558b"
    i82559a = "i82559a"
    i82559b = "i82559b"
    i82559c = "i82559c"
    i82559er = "i82559er"
    i82562 = "i82562"
    i82801 = "i82801"
    igb = "igb"
    ne2k_pci = "ne2k_pci"
    pcnet = "pcnet"
    rocker = "rocker"
    rtl8139 = "rtl8139"
    virtio = "virtio"
    virtio_net_pci = "virtio-net-pci"
    vmxnet3 = "vmxnet3"


class QemuDiskInterfaceType(str, Enum):
    """
    Supported Qemu VM disk interface types.
    """

    ide = "ide"
    sate = "sata"
    nvme = "nvme"
    scsi = "scsi"
    sd = "sd"
    mtd = "mtd"
    floppy = "floppy"
    pflash = "pflash"
    virtio = "virtio"
    none = "none"


class QemuBase(BaseModel):
    """
    Common Qemu node properties.
    """

    name: str | None = None
    node_id: UUID | None = None
    usage: str | None = Field(None, description="How to use the node")
    linked_clone: bool | None = Field(None, description="Whether the VM is a linked clone or not")
    qemu_path: str | None = Field(None, description="Qemu executable path")
    platform: QemuPlatform | None = Field(None, description="Platform to emulate")
    console: int | None = Field(None, gt=0, le=65535, description="Console TCP port")
    console_type: QemuConsoleType | None = Field(None, description="Console type")
    aux: int | None = Field(None, gt=0, le=65535, description="Auxiliary console TCP port")
    aux_type: QemuConsoleType | None = Field(None, description="Auxiliary console type")
    hda_disk_image: str | None = Field(None, description="QEMU hda disk image path")
    hda_disk_image_backing_file: str | None = Field(None, description="QEMU hda backing file disk image path")
    hda_disk_image_md5sum: str | None = Field(None, description="QEMU hda disk image checksum")
    hda_disk_interface: QemuDiskInterfaceType | None = Field(None, description="QEMU hda interface")
    hdb_disk_image: str | None = Field(None, description="QEMU hdb disk image path")
    hdb_disk_image_backing_file: str | None = Field(None, description="QEMU hdb backing file disk image path")
    hdb_disk_image_md5sum: str | None = Field(None, description="QEMU hdb disk image checksum")
    hdb_disk_interface: QemuDiskInterfaceType | None = Field(None, description="QEMU hdb interface")
    hdc_disk_image: str | None = Field(None, description="QEMU hdc disk image path")
    hdc_disk_image_backing_file: str | None = Field(None, description="QEMU hdc backing file disk image path")
    hdc_disk_image_md5sum: str | None = Field(None, description="QEMU hdc disk image checksum")
    hdc_disk_interface: QemuDiskInterfaceType | None = Field(None, description="QEMU hdc interface")
    hdd_disk_image: str | None = Field(None, description="QEMU hdd disk image path")
    hdd_disk_image_backing_file: str | None = Field(None, description="QEMU hdd backing file disk image path")
    hdd_disk_image_md5sum: str | None = Field(None, description="QEMU hdd disk image checksum")
    hdd_disk_interface: QemuDiskInterfaceType | None = Field(None, description="QEMU hdd interface")
    cdrom_image: str | None = Field(None, description="QEMU cdrom image path")
    cdrom_image_md5sum: str | None = Field(None, description="QEMU cdrom image checksum")
    bios_image: str | None = Field(None, description="QEMU bios image path")
    bios_image_md5sum: str | None = Field(None, description="QEMU bios image checksum")
    initrd: str | None = Field(None, description="QEMU initrd path")
    initrd_md5sum: str | None = Field(None, description="QEMU initrd checksum")
    kernel_image: str | None = Field(None, description="QEMU kernel image path")
    kernel_image_md5sum: str | None = Field(None, description="QEMU kernel image checksum")
    kernel_command_line: str | None = Field(None, description="QEMU kernel command line")
    boot_priority: QemuBootPriority | None = Field(None, description="QEMU boot priority")
    ram: int | None = Field(None, description="Amount of RAM in MB")
    cpus: int | None = Field(None, ge=1, le=255, description="Number of vCPUs")
    maxcpus: int | None = Field(None, ge=1, le=255, description="Maximum number of hotpluggable vCPUs")
    adapters: int | None = Field(None, ge=0, le=275, description="Number of adapters")
    adapter_type: QemuAdapterType | None = Field(None, description="QEMU adapter type")
    mac_address: str | None = Field(
        None, description="QEMU MAC address", pattern="^([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})$"
    )
    replicate_network_connection_state: bool | None = Field(
        None, description="Replicate the network connection state for links in Qemu"
    )
    create_config_disk: bool | None = Field(
        None, description="Automatically create a config disk on HDD disk interface (secondary slave)"
    )
    tpm: bool | None = Field(None, description="Enable Trusted Platform Module (TPM)")
    uefi: bool | None = Field(None, description="Enable UEFI boot mode")
    on_close: QemuOnCloseAction | None = Field(None, description="Action to execute on the VM is closed")
    cpu_throttling: int | None = Field(None, ge=0, le=800, description="Percentage of CPU allowed for QEMU")
    process_priority: QemuProcessPriority | None = Field(None, description="Process priority for QEMU")
    options: str | None = Field(None, description="Additional QEMU options")
    custom_adapters: list[CustomAdapter] | None = Field(None, description="Custom adapters")


class QemuCreate(QemuBase):
    """
    Properties to create a Qemu node.
    """

    name: str
    disk_images_to_reset: list[str] | None = Field(
        None,
        description="Disk image properties whose stale linked-clone overlays must be recreated",
    )


class QemuUpdate(QemuBase):
    """
    Properties to update a Qemu node.
    """

    pass


class Qemu(QemuBase):
    name: str
    project_id: UUID = Field(..., description="Project ID")
    node_directory: str = Field(..., description="Path to the node working directory (read only)")
    command_line: str = Field(..., description="Last command line used to start IOU (read only)")
    status: NodeStatus = Field(..., description="Container status (read only)")


class QemuBinaryPath(BaseModel):
    path: str
    version: str
