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

from pydantic import BaseModel, ConfigDict, Field

from .base import DateTimeModelMixin


class PrivilegeBase(BaseModel):
    """
    Common privilege properties.
    """

    name: str
    description: str | None = None


class Privilege(DateTimeModelMixin, PrivilegeBase):
    privilege_id: UUID
    model_config = ConfigDict(from_attributes=True)


class ACEType(str, Enum):
    user = "user"
    group = "group"


class ACEBase(BaseModel):
    """
    Common ACE properties.
    """

    ace_type: ACEType = Field(..., description="Type of the ACE")
    path: str
    propagate: bool | None = True
    allowed: bool | None = True
    user_id: UUID | None = None
    group_id: UUID | None = None
    role_id: UUID
    model_config = ConfigDict(use_enum_values=True)


class ACECreate(ACEBase):
    """
    Properties to create an ACE.
    """

    pass


class ACEUpdate(ACEBase):
    """
    Properties to update an ACE.
    """

    pass


class ACE(DateTimeModelMixin, ACEBase):
    ace_id: UUID
    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    """
    Common role properties.
    """

    name: str | None = None
    description: str | None = None


class RoleCreate(RoleBase):
    """
    Properties to create a role.
    """

    name: str


class RoleUpdate(RoleBase):
    """
    Properties to update a role.
    """

    pass


class Role(DateTimeModelMixin, RoleBase):
    role_id: UUID
    is_builtin: bool
    privileges: list[Privilege]
    model_config = ConfigDict(from_attributes=True)
