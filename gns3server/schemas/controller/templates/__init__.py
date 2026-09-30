#
# Copyright (C) 2021 GNS3 Technologies Inc.
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
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..base import DateTimeModelMixin
from ..nodes import NodeType


class Category(str, Enum):
    """
    Supported categories
    """

    router = "router"
    switch = "switch"
    guest = "guest"
    firewall = "firewall"


class ApplianceMetadata(BaseModel):
    """
    Metadata kept on a template installed from an appliance: vendor
    information, default credentials and other fields that describe
    the appliance but are not node properties.
    """

    model_config = ConfigDict(extra="allow")

    appliance_id: str | None = Field(None, description="ID of the appliance the template was installed from")
    description: str | None = None
    vendor_name: str | None = None
    vendor_url: str | None = None
    vendor_logo_url: str | None = None
    documentation_url: str | None = None
    product_name: str | None = None
    product_url: str | None = None
    status: str | None = None
    availability: str | None = None
    maintainer: str | None = None
    maintainer_email: str | None = None
    installation_instructions: str | None = None
    default_username: str | None = None
    default_password: str | None = None


class TemplateBase(BaseModel):
    """
    Common template properties.
    """

    template_id: UUID | None = None
    name: str | None = None
    version: str | None = None
    category: Category | None = None
    default_name_format: str | None = None
    symbol: str | None = None
    template_type: NodeType | None = None
    compute_id: str | None = None
    usage: str | None = ""
    netmiko_device_type: str | None = Field(
        None,
        description="Device type for Netmiko-based automation tools (e.g. 'cisco_xr' or 'nokia_srl')",
        pattern=r"^[a-z0-9_]+$|^$",
    )
    tags: List[str] | None = Field(
        default_factory=list, description="User-defined metadata tags (e.g. 'vendor:cisco' or 'model:7200')"
    )
    appliance_metadata: ApplianceMetadata | None = Field(
        None, description="Metadata inherited from the appliance the template was installed from"
    )


class TemplateCreate(TemplateBase):
    """
    Properties to create a template.
    """

    name: str
    template_type: NodeType
    model_config = ConfigDict(extra="allow")


class TemplateUpdate(TemplateBase):
    model_config = ConfigDict(extra="allow")


class Template(DateTimeModelMixin, TemplateBase):
    template_id: UUID
    name: str
    category: Category
    symbol: str
    builtin: bool
    template_type: NodeType
    model_config = ConfigDict(extra="allow", from_attributes=True)


class TemplateUsage(BaseModel):
    x: int
    y: int
    name: str | None = Field(None, description="Use this name to create a new node")
    compute_id: str | None = Field(None, description="Used if the template doesn't have a default compute")
