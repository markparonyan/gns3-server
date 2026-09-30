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

from pydantic import Field

from gns3server.schemas.compute.dynamips_nodes import (
    DynamipsAdapters,
    DynamipsConsoleType,
    DynamipsMidplane,
    DynamipsNPE,
    DynamipsPlatform,
    DynamipsWics,
)

from . import Category, TemplateBase


class DynamipsTemplateBase(TemplateBase):
    category: Category | None = Category.router
    default_name_format: str | None = "R{0}"
    symbol: str | None = "router"
    platform: DynamipsPlatform | None = Field(None, description="Cisco router platform")
    image: str | None = Field(None, description="Path to the IOS image")
    exec_area: int | None = Field(64, ge=0, description="Exec area value")
    mmap: bool | None = Field(True, description="MMAP feature")
    mac_addr: str | None = Field(
        "", description="Base MAC address", pattern="^([0-9a-fA-F]{4}\\.){2}[0-9a-fA-F]{4}$|^$"
    )
    system_id: str | None = Field("FTX0945W0MY", description="System ID")
    startup_config: str | None = Field("ios_base_startup-config.txt", description="IOS startup configuration file")
    private_config: str | None = Field("", description="IOS private configuration file")
    idlepc: str | None = Field("", description="Idle-PC value", pattern="^(0x[0-9a-fA-F]+)?$|^$")
    idlemax: int | None = Field(500, ge=0, description="Idlemax value")
    idlesleep: int | None = Field(30, ge=0, description="Idlesleep value")
    disk0: int | None = Field(0, ge=0, description="Disk0 size in MB")
    disk1: int | None = Field(0, ge=0, description="Disk1 size in MB")
    auto_delete_disks: bool | None = Field(False, description="Automatically delete nvram and disk files")
    console_type: DynamipsConsoleType | None = Field(DynamipsConsoleType.telnet, description="Console type")
    console_auto_start: bool | None = Field(
        False, description="Automatically start the console when the node has started"
    )
    aux_type: DynamipsConsoleType | None = Field(DynamipsConsoleType.none, description="Auxiliary console type")
    slot0: DynamipsAdapters | None = Field(None, description="Network module slot 0")
    slot1: DynamipsAdapters | None = Field(None, description="Network module slot 1")
    slot2: DynamipsAdapters | None = Field(None, description="Network module slot 2")
    slot3: DynamipsAdapters | None = Field(None, description="Network module slot 3")
    slot4: DynamipsAdapters | None = Field(None, description="Network module slot 4")
    slot5: DynamipsAdapters | None = Field(None, description="Network module slot 5")
    slot6: DynamipsAdapters | None = Field(None, description="Network module slot 6")
    wic0: DynamipsWics | None = Field(None, description="Network module WIC slot 0")
    wic1: DynamipsWics | None = Field(None, description="Network module WIC slot 1")
    wic2: DynamipsWics | None = Field(None, description="Network module WIC slot 2")


class DynamipsTemplate(DynamipsTemplateBase):
    platform: DynamipsPlatform = Field(..., description="Cisco router platform")
    image: str = Field(..., description="Path to the IOS image")


class C7200DynamipsTemplateUpdate(DynamipsTemplateBase):
    ram: int | None = Field(512, gt=0, description="Amount of RAM in MB")
    nvram: int | None = Field(512, gt=0, description="Amount of NVRAM in KB")
    npe: DynamipsNPE | None = Field(DynamipsNPE.npe_400, description="NPE model")
    midplane: DynamipsMidplane | None = Field(DynamipsMidplane.vxr, description="Midplane model")
    sparsemem: bool | None = Field(True, description="Sparse memory feature")


class C7200DynamipsTemplate(C7200DynamipsTemplateUpdate):
    platform: DynamipsPlatform = Field(..., description="Cisco router platform")
    image: str = Field(..., description="Path to the IOS image")


class C3725DynamipsTemplateUpdate(DynamipsTemplateBase):
    ram: int | None = Field(128, gt=0, description="Amount of RAM in MB")
    nvram: int | None = Field(256, gt=0, description="Amount of NVRAM in KB")
    iomem: int | None = Field(5, ge=0, le=100, description="I/O memory percentage")
    sparsemem: bool | None = Field(True, description="Sparse memory feature")


class C3725DynamipsTemplate(C3725DynamipsTemplateUpdate):
    platform: DynamipsPlatform = Field(..., description="Cisco router platform")
    image: str = Field(..., description="Path to the IOS image")


class C3745DynamipsTemplateUpdate(DynamipsTemplateBase):
    ram: int | None = Field(256, gt=0, description="Amount of RAM in MB")
    nvram: int | None = Field(256, gt=0, description="Amount of NVRAM in KB")
    iomem: int | None = Field(5, ge=0, le=100, description="I/O memory percentage")
    sparsemem: bool | None = Field(True, description="Sparse memory feature")


class C3745DynamipsTemplate(C3745DynamipsTemplateUpdate):
    platform: DynamipsPlatform = Field(..., description="Cisco router platform")
    image: str = Field(..., description="Path to the IOS image")


class C3600ChassisType(str, Enum):
    chassis_3620 = "3620"
    chassis_3640 = "3640"
    chassis_3660 = "3660"


class C3600DynamipsTemplateUpdate(DynamipsTemplateBase):
    chassis: C3600ChassisType | None = Field(C3600ChassisType.chassis_3660, description="Chassis type")
    ram: int | None = Field(192, gt=0, description="Amount of RAM in MB")
    nvram: int | None = Field(128, gt=0, description="Amount of NVRAM in KB")
    iomem: int | None = Field(5, ge=0, le=100, description="I/O memory percentage")
    sparsemem: bool | None = Field(True, description="Sparse memory feature")


class C3600DynamipsTemplate(C3600DynamipsTemplateUpdate):
    platform: DynamipsPlatform = Field(..., description="Cisco router platform")
    image: str = Field(..., description="Path to the IOS image")


class C2691DynamipsTemplateUpdate(DynamipsTemplateBase):
    ram: int | None = Field(192, gt=0, description="Amount of RAM in MB")
    nvram: int | None = Field(256, gt=0, description="Amount of NVRAM in KB")
    iomem: int | None = Field(5, ge=0, le=100, description="I/O memory percentage")
    sparsemem: bool | None = Field(True, description="Sparse memory feature")


class C2691DynamipsTemplate(C2691DynamipsTemplateUpdate):
    platform: DynamipsPlatform = Field(..., description="Cisco router platform")
    image: str = Field(..., description="Path to the IOS image")


class C2600ChassisType(str, Enum):
    chassis_2610 = "2610"
    chassis_2620 = "2620"
    chassis_2610xm = "2610XM"
    chassis_2620xm = "2620XM"
    chassis_2650xm = "2650XM"
    chassis_2621 = "2621"
    chassis_2611xm = "2611XM"
    chassis_2621xm = "2621XM"
    chassis_2651xm = "2651XM"


class C2600DynamipsTemplateUpdate(DynamipsTemplateBase):
    chassis: C2600ChassisType | None = Field(C2600ChassisType.chassis_2651xm, description="Chassis type")
    ram: int | None = Field(160, gt=0, description="Amount of RAM in MB")
    nvram: int | None = Field(128, gt=0, description="Amount of NVRAM in KB")
    iomem: int | None = Field(15, ge=0, le=100, description="I/O memory percentage")
    sparsemem: bool | None = Field(True, description="Sparse memory feature")


class C2600DynamipsTemplate(C2600DynamipsTemplateUpdate):
    platform: DynamipsPlatform = Field(..., description="Cisco router platform")
    image: str = Field(..., description="Path to the IOS image")


class C1700ChassisType(str, Enum):
    chassis_1720 = "1720"
    chassis_1721 = "1721"
    chassis_1750 = "1750"
    chassis_1751 = "1751"
    chassis_1760 = "1760"


class C1700DynamipsTemplateUpdate(DynamipsTemplateBase):
    chassis: C1700ChassisType | None = Field(C1700ChassisType.chassis_1760, description="Chassis type")
    ram: int | None = Field(160, gt=0, description="Amount of RAM in MB")
    nvram: int | None = Field(128, gt=0, description="Amount of NVRAM in KB")
    iomem: int | None = Field(15, ge=0, le=100, description="I/O memory percentage")
    sparsemem: bool | None = Field(False, description="Sparse memory feature")


class C1700DynamipsTemplate(C1700DynamipsTemplateUpdate):
    platform: DynamipsPlatform = Field(..., description="Cisco router platform")
    image: str = Field(..., description="Path to the IOS image")
