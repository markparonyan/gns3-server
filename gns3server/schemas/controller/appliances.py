#
# Copyright (C) 2026 GNS3 Technologies Inc.
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

# Unified Pydantic model supporting both appliance registry versions using discriminated unions

from enum import Enum
from typing import Annotated, Literal
from uuid import UUID

from pydantic import AnyUrl, BaseModel, Discriminator, EmailStr, Field, Tag, TypeAdapter, model_validator

from ..common import ExtraConfig

# ============================================================================
# Shared Enums
# ============================================================================


class Category(str, Enum):
    """Appliance category enum"""

    router = "router"
    multilayer_switch = "multilayer_switch"
    switch = "switch"
    firewall = "firewall"
    guest = "guest"


class Status(str, Enum):
    """Appliance status enum"""

    stable = "stable"
    experimental = "experimental"
    broken = "broken"


class Availability(str, Enum):
    """Image availability enum"""

    free = "free"
    with_registration = "with-registration"
    free_to_try = "free-to-try"
    service_contract = "service-contract"


class Compression(str, Enum):
    """Compression type enum"""

    bzip2 = "bzip2"
    gzip = "gzip"
    lzma = "lzma"
    xz = "xz"
    rar = "rar"
    zip = "zip"
    field_7z = "7z"


class DynamipsPlatform(str, Enum):
    """Dynamips platform enum"""

    c1700 = "c1700"
    c2600 = "c2600"
    c2691 = "c2691"
    c3725 = "c3725"
    c3745 = "c3745"
    c3600 = "c3600"
    c7200 = "c7200"


class DynamipsChassis(str, Enum):
    """Dynamips chassis enum"""

    chassis_1720 = "1720"
    chassis_1721 = "1721"
    chassis_1750 = "1750"
    chassis_1751 = "1751"
    chassis_1760 = "1760"
    chassis_2610 = "2610"
    chassis_2620 = "2620"
    chassis_2610XM = "2610XM"
    chassis_2620XM = "2620XM"
    chassis_2650XM = "2650XM"
    chassis_2621 = "2621"
    chassis_2611XM = "2611XM"
    chassis_2621XM = "2621XM"
    chassis_2651XM = "2651XM"
    chassis_3620 = "3620"
    chassis_3640 = "3640"
    chassis_3660 = "3660"
    _ = ""


class DynamipsSlot(str, Enum):
    """Dynamips slot enum"""

    C7200_IO_2FE = "C7200-IO-2FE"
    C7200_IO_FE = "C7200-IO-FE"
    C7200_IO_GE_E = "C7200-IO-GE-E"
    NM_16ESW = "NM-16ESW"
    NM_1E = "NM-1E"
    NM_1FE_TX = "NM-1FE-TX"
    NM_4E = "NM-4E"
    NM_4T = "NM-4T"
    PA_2FE_TX = "PA-2FE-TX"
    PA_4E = "PA-4E"
    PA_4T_ = "PA-4T+"
    PA_8E = "PA-8E"
    PA_8T = "PA-8T"
    PA_A1 = "PA-A1"
    PA_FE_TX = "PA-FE-TX"
    PA_GE = "PA-GE"
    PA_POS_OC3 = "PA-POS-OC3"
    C2600_MB_2FE = "C2600-MB-2FE"
    C2600_MB_1E = "C2600-MB-1E"
    C1700_MB_1FE = "C1700-MB-1FE"
    C2600_MB_2E = "C2600-MB-2E"
    C2600_MB_1FE = "C2600-MB-1FE"
    C1700_MB_WIC1 = "C1700-MB-WIC1"
    GT96100_FE = "GT96100-FE"
    Leopard_2FE = "Leopard-2FE"
    _ = ""


class DynamipsWic(str, Enum):
    """Dynamips WIC enum"""

    WIC_1ENET = "WIC-1ENET"
    WIC_1T = "WIC-1T"
    WIC_2T = "WIC-2T"
    _ = ""


class DynamipsMidplane(str, Enum):
    """Dynamips midplane enum"""

    std = "std"
    vxr = "vxr"


class DynamipsNpe(str, Enum):
    """Dynamips NPE enum"""

    npe_100 = "npe-100"
    npe_150 = "npe-150"
    npe_175 = "npe-175"
    npe_200 = "npe-200"
    npe_225 = "npe-225"
    npe_300 = "npe-300"
    npe_400 = "npe-400"
    npe_g2 = "npe-g2"


class QemuConsoleType(str, Enum):
    """Qemu console type enum"""

    telnet = "telnet"
    ssh = "ssh"
    vnc = "vnc"
    spice = "spice"
    spice_agent = "spice+agent"
    none = "none"


class QemuAdapterType(str, Enum):
    """Qemu adapter type enum"""

    e1000 = "e1000"
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
    rtl8139 = "rtl8139"
    virtio = "virtio"
    virtio_net_pci = "virtio-net-pci"
    vmxnet3 = "vmxnet3"


class QemuPlatform(str, Enum):
    """Qemu platform enum"""

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


class QemuDiskInterface(str, Enum):
    """Disk interface enum"""

    ide = "ide"
    sata = "sata"
    nvme = "nvme"
    scsi = "scsi"
    sd = "sd"
    mtd = "mtd"
    floppy = "floppy"
    pflash = "pflash"
    virtio = "virtio"
    none = "none"


class QemuBootPriority(str, Enum):
    """Boot priority enum"""

    c = "c"
    d = "d"
    n = "n"
    cn = "cn"
    cd = "cd"
    dn = "dn"
    dc = "dc"
    nc = "nc"
    nd = "nd"


class QemuOnClose(str, Enum):
    """Qemu on_close action enum"""

    power_off = "power_off"
    shutdown_signal = "shutdown_signal"
    save_vm_state = "save_vm_state"


class QemuProcessPriority(str, Enum):
    """Qemu process priority enum"""

    realtime = "realtime"
    very_high = "very high"
    high = "high"
    normal = "normal"
    low = "low"
    very_low = "very low"


class DockerConsoleType(str, Enum):
    """Docker console type enum"""

    telnet = "telnet"
    ssh = "ssh"
    vnc = "vnc"
    http = "http"
    https = "https"
    none = "none"
    docker_exec = "docker_exec"


class ChecksumType(str, Enum):
    """Checksum type enum"""

    md5 = "md5"


class TemplateType(str, Enum):
    """Template type enum"""

    docker = "docker"
    iou = "iou"
    dynamips = "dynamips"
    qemu = "qemu"


# ============================================================================
# Version 1-6 Specific Enums
# ============================================================================


class Kvm(str, Enum):
    """KVM requirements enum"""

    require = "require"
    allow = "allow"
    disable = "disable"


# ============================================================================
# Version 1-6 Models
# ============================================================================


class Docker(BaseModel):
    """Docker configuration for v1-6"""

    adapters: int = Field(..., title="Number of Ethernet adapters")
    image: str = Field(..., title="Docker image in the Docker Hub")
    start_command: str | None = Field(
        None, title="Command executed when the container start. Empty will use the default"
    )
    environment: str | None = Field(None, title="One KEY=VAR environment by line")
    console_type: DockerConsoleType | None = Field(
        None, title="Type of console connection for the administration of the appliance"
    )
    console_http_port: int | None = Field(None, description="Internal port in the container of the HTTP server")
    console_http_path: str | None = Field(None, description="Path of the web interface")
    extra_hosts: str | None = Field(None, description="Hosts which will be written to /etc/hosts into container")
    extra_volumes: list[str] | None = Field(
        None,
        description="Additional directories to make persistent that are not included in the images VOLUME directive",
    )
    extra_configs: list[ExtraConfig] | None = Field(
        None, description="Configuration files injected into the container (bind-mounted read-only)"
    )


class Iou(BaseModel):
    """IOU configuration for v1-6"""

    ethernet_adapters: int = Field(..., title="Number of Ethernet adapters")
    serial_adapters: int = Field(..., title="Number of serial adapters")
    nvram: int = Field(..., title="Host NVRAM")
    ram: int = Field(..., title="Host RAM")
    startup_config: str = Field(..., title="Config loaded at startup")


class Dynamips(BaseModel):
    """Dynamips configuration for v1-6"""

    chassis: DynamipsChassis | None = Field(None, title="Chassis type")
    platform: DynamipsPlatform = Field(..., title="Platform type")
    ram: Annotated[int, Field(ge=1)] = Field(..., title="Amount of ram")
    nvram: Annotated[int, Field(ge=1)] = Field(..., title="Amount of nvram")
    startup_config: str | None = Field(None, title="Config loaded at startup")
    wic0: DynamipsWic | None = None
    wic1: DynamipsWic | None = None
    wic2: DynamipsWic | None = None
    slot0: DynamipsSlot | None = None
    slot1: DynamipsSlot | None = None
    slot2: DynamipsSlot | None = None
    slot3: DynamipsSlot | None = None
    slot4: DynamipsSlot | None = None
    slot5: DynamipsSlot | None = None
    slot6: DynamipsSlot | None = None
    midplane: DynamipsMidplane | None = None
    npe: DynamipsNpe | None = None


class Qemu(BaseModel):
    """QEMU configuration for v1-6"""

    adapter_type: QemuAdapterType = Field(..., title="Type of network adapter")
    adapters: int = Field(..., title="Number of adapters")
    ram: int = Field(..., title="RAM allocated to the appliance (MB)")
    cpus: int | None = Field(None, title="Number of Virtual CPU")
    hda_disk_interface: QemuDiskInterface | None = Field(None, title="Disk interface for the installed hda_disk_image")
    hdb_disk_interface: QemuDiskInterface | None = Field(None, title="Disk interface for the installed hdb_disk_image")
    hdc_disk_interface: QemuDiskInterface | None = Field(None, title="Disk interface for the installed hdc_disk_image")
    hdd_disk_interface: QemuDiskInterface | None = Field(None, title="Disk interface for the installed hdd_disk_image")
    arch: QemuPlatform = Field(..., title="Architecture emulated")
    console_type: QemuConsoleType = Field(
        ..., title="Type of console connection for the administration of the appliance"
    )
    boot_priority: QemuBootPriority | None = Field(None, title="Disk boot priority")
    kernel_command_line: str | None = Field(None, title="Command line parameters sent to the kernel")
    kvm: Kvm = Field(..., title="KVM requirements")
    options: str | None = Field(None, title="Optional additional qemu command line options")
    cpu_throttling: Annotated[float, Field(ge=0.0, le=100.0)] | None = Field(None, title="Throttle the CPU")
    on_close: QemuOnClose | None = Field(None, title="Action to execute on the VM is closed")
    process_priority: QemuProcessPriority | None = Field(None, title="Process priority for QEMU")


class ApplianceVersionImages(BaseModel):
    """Appliance version images configuration for v1-6"""

    kernel_image: str | None = Field(None, title="Kernel image")
    initrd: str | None = Field(None, title="Initrd disk image")
    image: str | None = Field(None, title="OS image")
    bios_image: str | None = Field(None, title="Bios image")
    hda_disk_image: str | None = Field(None, title="Hda disk image")
    hdb_disk_image: str | None = Field(None, title="Hdc disk image")
    hdc_disk_image: str | None = Field(None, title="Hdd disk image")
    hdd_disk_image: str | None = Field(None, title="Hdd diskimage")
    cdrom_image: str | None = Field(None, title="cdrom image")


class ApplianceVersion(BaseModel):
    """Appliance version definition for v1-6"""

    name: str = Field(..., title="Name of the version")
    idlepc: str | None = Field(None, pattern="^0x[0-9a-f]{8}")
    images: ApplianceVersionImages | None = Field(None, title="Images used for this version")


class ApplianceImage(BaseModel):
    """Appliance image definition - compatible with both versions"""

    filename: str = Field(..., title="Filename")
    version: str = Field(..., title="Version of the file")
    md5sum: str | None = Field(None, title="md5sum of the file", pattern="^[a-f0-9]{32}$")
    filesize: int = Field(..., title="File size in bytes")
    download_url: AnyUrl | Annotated[str, Field(max_length=0)] | None = Field(
        None, title="Download url where you can download the appliance from a browser"
    )
    direct_download_url: AnyUrl | Annotated[str, Field(max_length=0)] | None = Field(
        None,
        title="Optional. Non authenticated url to the image file where you can download the image.",
    )
    compression: Compression | None = Field(None, title="Optional, compression type of direct download url image.")
    checksum: str | None = Field(None, title="checksum of the image file")
    checksum_type: ChecksumType | None = Field(None, title="checksum type of the image file")
    compression_target: str | None = Field(
        None, title="Optional, file name of the image file inside the compressed file."
    )


# ============================================================================
# Version 8 Models
# ============================================================================


class CustomAdapterItem(BaseModel):
    """Custom adapter configuration (v8)"""

    adapter_number: int = Field(..., title="Adapter number")
    port_name: str | None = Field(None, title="Custom port name")
    adapter_type: QemuAdapterType | None = Field(None, title="Custom adapter type")
    mac_address: str | None = Field(
        None,
        title="Custom MAC address",
        pattern=r"^([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})$",
    )


class DockerPropertiesV8(BaseModel):
    """Docker template properties (v8)"""

    name: str | None = Field(None, title="Name of the template")
    category: Category | None = Field(None, title="Category of the template")
    default_name_format: str | None = Field(None, title="Default name format")
    usage: str | None = Field(None, title="How to use the template")
    symbol: str | None = Field(None, title="Symbol of the template")
    image: str = Field(..., title="Docker image")
    adapters: int | None = Field(None, title="Number of ethernet adapters")
    start_command: str | None = Field(
        None, title="Command executed when the container start. Empty will use the default"
    )
    environment: str | None = Field(None, title="One KEY=VAR environment by line")
    console_type: DockerConsoleType | None = Field(None, title="Type of console")
    console_http_port: int | None = Field(None, title="Internal port in the container of the HTTP server")
    console_http_path: str | None = Field(None, title="Path of the web interface")
    console_resolution: str | None = Field(
        None,
        title="Console resolution for VNC, for example 1024x768",
        pattern=r"^[0-9]+x[0-9]+$",
    )
    extra_hosts: str | None = Field(None, title="Docker extra hosts (added to /etc/hosts)")
    extra_volumes: list[str] | None = Field(None, title="Additional directories to make persistent")
    custom_adapters: list[CustomAdapterItem] | None = Field(None, title="Custom adapters")
    extra_configs: list[ExtraConfig] | None = Field(
        None, title="Configuration files injected into the container (bind-mounted read-only)"
    )


class IouPropertiesV8(BaseModel):
    """IOU template properties (v8)"""

    name: str | None = Field(None, title="Name of the template")
    category: Category | None = Field(None, title="Category of the template")
    default_name_format: str | None = Field(None, title="Default name format")
    usage: str | None = Field(None, title="How to use the template")
    symbol: str | None = Field(None, title="Symbol of the template")
    ethernet_adapters: int | None = Field(None, title="Number of ethernet adapters")
    serial_adapters: int | None = Field(None, title="Number of serial adapters")
    ram: int | None = Field(None, title="Host RAM")
    nvram: int | None = Field(None, title="Host NVRAM")
    startup_config: str | None = Field(None, title="Config loaded at startup")


class DynamipsPropertiesV8(BaseModel):
    """Dynamips template properties (v8)"""

    name: str | None = Field(None, title="Name of the template")
    category: Category | None = Field(None, title="Category of the template")
    default_name_format: str | None = Field(None, title="Default name format")
    usage: str | None = Field(None, title="How to use the template")
    symbol: str | None = Field(None, title="Symbol of the template")
    chassis: DynamipsChassis | None = Field(None, title="Chassis type")
    platform: DynamipsPlatform | None = Field(None, title="Platform type")
    ram: Annotated[int, Field(ge=1)] | None = Field(None, title="Amount of ram")
    nvram: Annotated[int, Field(ge=1)] | None = Field(None, title="Amount of nvram")
    idlepc: str | None = Field(None, pattern=r"^0x[0-9a-f]{8}")
    startup_config: str | None = Field(None, title="Config loaded at startup")
    wic0: str | None = Field(None)
    wic1: str | None = Field(None)
    wic2: str | None = Field(None)
    slot0: str | None = Field(None)
    slot1: str | None = Field(None)
    slot2: str | None = Field(None)
    slot3: str | None = Field(None)
    slot4: str | None = Field(None)
    slot5: str | None = Field(None)
    slot6: str | None = Field(None)
    midplane: DynamipsMidplane | None = Field(None)
    npe: DynamipsNpe | None = Field(None)


class QemuPropertiesV8(BaseModel):
    """Qemu template properties (v8)"""

    name: str | None = Field(None, title="Name of the template")
    category: Category | None = Field(None, title="Category of the template")
    default_name_format: str | None = Field(None, title="Default name format")
    usage: str | None = Field(None, title="How to use the template")
    symbol: str | None = Field(None, title="Symbol of the template")
    adapter_type: QemuAdapterType | None = Field(None, title="Type of network adapter")
    adapters: int | None = Field(None, title="Number of adapters")
    custom_adapters: list[CustomAdapterItem] | None = Field(None, title="Custom adapters")
    first_port_name: str | None = Field(None, title="Optional name of the first networking port example: eth0")
    port_name_format: str | None = Field(None, title="Optional formating of the networking port example: eth{0}")
    port_segment_size: int | None = Field(
        None,
        title="Optional port segment size. A port segment is a block of port. For example Ethernet0/0 Ethernet0/1 is the module 0 with a port segment size of 2",
    )
    linked_clone: bool | None = Field(None, title="False if you don't want to use a single image for all nodes")
    ram: int | None = Field(None, title="Ram allocated to the appliance (MB)")
    cpus: int | None = Field(None, title="Number of Virtual CPU")
    hda_disk_interface: QemuDiskInterface | None = Field(None, title="Disk interface for the installed hda_disk_image")
    hdb_disk_interface: QemuDiskInterface | None = Field(None, title="Disk interface for the installed hdb_disk_image")
    hdc_disk_interface: QemuDiskInterface | None = Field(None, title="Disk interface for the installed hdc_disk_image")
    hdd_disk_interface: QemuDiskInterface | None = Field(None, title="Disk interface for the installed hdd_disk_image")
    platform: QemuPlatform | None = Field(None, title="Platform to emulate")
    console_type: QemuConsoleType | None = Field(
        None, title="Type of console connection for the administration of the appliance"
    )
    boot_priority: QemuBootPriority | None = Field(
        None,
        title="Optional define the disk boot priory. Refer to -boot option in qemu manual for more details.",
    )
    kernel_command_line: str | None = Field(None, title="Command line parameters send to the kernel")
    kvm: Kvm | None = Field(None, title="KVM requirements")
    options: str | None = Field(None, title="Optional additional qemu command line options")
    cpu_throttling: Annotated[int, Field(ge=0, le=800)] | None = Field(None, title="Throttle the CPU")
    tpm: bool | None = Field(None, title="Enable the Trusted Platform Module (TPM)")
    uefi: bool | None = Field(None, title="Enable the UEFI boot mode")
    on_close: QemuOnClose | None = Field(None, title="Action to execute on the VM is closed")
    process_priority: QemuProcessPriority | None = Field(None, title="Process priority for QEMU")


_V8_PROPERTIES_MODELS = {
    TemplateType.qemu: QemuPropertiesV8,
    TemplateType.dynamips: DynamipsPropertiesV8,
    TemplateType.iou: IouPropertiesV8,
    TemplateType.docker: DockerPropertiesV8,
}


class TemplateSetting(BaseModel):
    """Emulator settings configuration (v8)"""

    name: str | None = Field(None, title="Name of the settings set")
    default: bool | None = Field(None, title="Whether these are the default settings")
    inherit_default_properties: bool | None = Field(True, title="Whether the default properties should be used")
    template_type: TemplateType = Field(..., title="Type of emulator properties")
    template_properties: QemuPropertiesV8 | DynamipsPropertiesV8 | IouPropertiesV8 | DockerPropertiesV8 = Field(
        ..., title="Properties for the template"
    )

    @model_validator(mode="before")
    @classmethod
    def _validate_template_properties(cls, data):
        """
        Validate template_properties against the model matching template_type.
        The template_type discriminator lives at the settings level (not inside
        template_properties), so the union cannot be discriminated by pydantic
        alone and would misroute properties between the per-type models.
        """

        if isinstance(data, dict):
            # work on a copy: replacing template_properties with the validated
            # model must not mutate the caller's data
            data = data.copy()
            template_type = data.get("template_type")
            template_properties = data.get("template_properties")
            model = _V8_PROPERTIES_MODELS.get(template_type)
            if model is not None and isinstance(template_properties, dict):
                data["template_properties"] = model.model_validate(template_properties)
        return data


class ApplianceVersionV8(BaseModel):
    """Appliance version definition (v8)"""

    name: str = Field(..., title="Name of the version")
    settings: str | None = Field(None, title="Template settings to use to run the version")
    idlepc: str | None = Field(None, pattern=r"^0x[0-9a-f]{8}")
    category: Category | None = Field(None, title="Category of the version")
    installation_instructions: str | None = Field(None, title="Optional installation instructions for the version")
    usage: str | None = Field(None, title="Optional instructions about using the version")
    default_username: str | None = Field(None, title="Default username for the version")
    default_password: str | None = Field(None, title="Default password for the version")
    symbol: str | None = Field(None, title="An optional symbol for the version")
    images: ApplianceVersionImages | None = Field(None, title="Images used for this version")


# ============================================================================
# Child Models with Discriminated Union
# ============================================================================


class ApplianceV1_6(BaseModel):
    """GNS3 Appliance model for registry versions 1-6"""

    registry_version: Literal[1, 2, 3, 4, 5, 6] = Field(
        ..., title="Version of the registry compatible with this appliance"
    )
    appliance_id: UUID = Field(..., title="Appliance ID")
    name: str = Field(..., title="Appliance name")
    builtin: bool | None = Field(None, title="Whether the appliance is builtin or not")
    category: Category = Field(..., title="Category of the appliance")
    description: str = Field(..., title="Description of the appliance. Could be a marketing description")
    vendor_name: str = Field(..., title="Name of the vendor")
    vendor_url: AnyUrl | Annotated[str, Field(max_length=0)] | None = Field(None, title="Website of the vendor")
    documentation_url: AnyUrl | Annotated[str, Field(max_length=0)] | None = Field(
        None, title="An optional documentation for using the appliance on vendor website"
    )
    product_name: str = Field(..., title="Product name")
    product_url: AnyUrl | Annotated[str, Field(max_length=0)] | None = Field(
        None, title="An optional product url on vendor website"
    )
    status: Status = Field(..., title="Document if the appliance is working or not")
    availability: Availability | None = Field(
        None,
        title="About image availability: can be downloaded directly; download requires a free registration; paid but a trial version (time or feature limited) is available; not available publicly",
    )
    maintainer: str = Field(..., title="Maintainer name")
    maintainer_email: EmailStr | Annotated[str, Field(max_length=0)] | None = Field(None, title="Maintainer email")
    usage: str | None = Field(None, title="How to use the appliance")
    symbol: str | None = Field(None, title="An optional symbol for the appliance")
    netmiko_device_type: str | None = Field(
        None, title="Device type for Netmiko-based automation tools", pattern=r"^[a-z0-9_]+$|^$"
    )
    first_port_name: str | None = Field(None, title="Optional name of the first networking port example: eth0")
    port_name_format: str | None = Field(None, title="Optional formating of the networking port example: eth{0}")
    port_segment_size: int | None = Field(
        None,
        title="Optional port segment size. A port segment is a block of port. For example Ethernet0/0 Ethernet0/1 is the module 0 with a port segment size of 2",
    )
    custom_adapters: list[CustomAdapterItem] | None = Field(
        None, title="Optional per-adapter overrides (port name, adapter type, MAC address)"
    )
    linked_clone: bool | None = Field(None, title="False if you don't want to use a single image for all nodes")
    docker: Docker | None = Field(None, title="Docker specific options")
    iou: Iou | None = Field(None, title="IOU specific options")
    dynamips: Dynamips | None = Field(None, title="Dynamips specific options")
    qemu: Qemu | None = Field(None, title="Qemu specific options")
    tags: list[str] | None = Field(None, title="User-defined metadata tags for the appliance")
    images: list[ApplianceImage] | None = Field(None, title="Images for this appliance")
    versions: list[ApplianceVersion] | None = Field(None, title="Versions of the appliance")


class ApplianceV8(BaseModel):
    """GNS3 Appliance model for registry version 8"""

    registry_version: Literal[8] = Field(
        ...,
        title="Version of the registry compatible with this appliance (version >=8 introduced breaking changes)",
    )
    appliance_id: str = Field(
        ...,
        title="Appliance ID",
        pattern=r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
    )
    name: str = Field(..., title="Appliance name")
    builtin: bool | None = Field(None, title="Whether the appliance is builtin or not")
    category: Category = Field(..., title="Category of the appliance")
    description: str = Field(..., title="Description of the appliance. Could be a marketing description")
    vendor_name: str = Field(..., title="Name of the vendor")
    vendor_url: AnyUrl = Field(..., title="Website of the vendor")
    vendor_logo_url: AnyUrl | None = Field(None, title="Link to the vendor logo (used by the GNS3 marketplace)")
    documentation_url: AnyUrl | None = Field(
        None, title="An optional documentation for using the appliance on vendor website"
    )
    product_name: str = Field(..., title="Product name")
    product_url: AnyUrl | None = Field(None, title="An optional product url on vendor website")
    status: Status = Field(..., title="Document if the appliance is working or not")
    availability: Availability | None = Field(
        None,
        title="About image availability: can be downloaded directly; download requires a free registration; paid but a trial version (time or feature limited) is available; not available publicly",
    )
    maintainer: str = Field(..., title="Maintainer name")
    maintainer_email: EmailStr = Field(..., title="Maintainer email")
    installation_instructions: str | None = Field(None, title="Optional installation instructions")
    usage: str | None = Field(None, title="How to use the appliance")
    default_username: str | None = Field(None, title="Default username for the appliance")
    default_password: str | None = Field(None, title="Default password for the appliance")
    symbol: str | None = Field(None, title="An optional symbol for the appliance")
    netmiko_device_type: str | None = Field(
        None, title="Device type for Netmiko-based automation tools", pattern=r"^[a-z0-9_]+$|^$"
    )
    tags: list[str] | None = Field(None, title="User-defined metadata tags for the appliance")
    settings: list[TemplateSetting] = Field(..., title="Settings for running the appliance")
    images: list[ApplianceImage] | None = Field(None, title="Images for this appliance")
    versions: list[ApplianceVersionV8] | None = Field(None, title="Versions of the appliance")


# ============================================================================
# Discriminated Union
# ============================================================================

# Define the discriminated union type
ApplianceUnion = Annotated[
    Annotated[ApplianceV1_6, Tag("v1_6")] | Annotated[ApplianceV8, Tag("v8")],
    Discriminator("registry_version"),
]
"""
Discriminated union type supporting both registry versions 1-6 and 8.
Uses registry_version field to automatically route to correct model.
"""

# For type hints in function signatures
Appliance = ApplianceUnion

_appliance_validator: TypeAdapter[ApplianceV1_6 | ApplianceV8] = TypeAdapter(ApplianceUnion)


class ApplianceModel:
    """
    Wrapper class to provide model_validate() method for the Appliance union type.
    This allows seamless usage of schemas.Appliance.model_validate() in existing code.
    """

    @staticmethod
    def model_validate(data: dict) -> ApplianceV1_6 | ApplianceV8:
        """
        Validate appliance data and return appropriate model instance.
        Automatically routes to ApplianceV1_6 or ApplianceV8 based on registry_version.
        """
        return _appliance_validator.validate_python(data)
