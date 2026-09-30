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

from uuid import UUID

from pydantic import BaseModel

from ..common import NodeStatus


class FrameRelaySwitchBase(BaseModel):
    """
    Common Frame Relay switch properties.
    """

    name: str | None = None
    node_id: UUID | None = None
    usage: str | None = None
    mappings: dict | None = None


class FrameRelaySwitchCreate(FrameRelaySwitchBase):
    """
    Properties to create an Frame Relay node.
    """

    node_id: UUID | None = None


class FrameRelaySwitchUpdate(FrameRelaySwitchBase):
    """
    Properties to update an Frame Relay node.
    """

    name: str | None = None
    node_id: UUID | None = None


class FrameRelaySwitch(FrameRelaySwitchBase):
    project_id: UUID
    status: NodeStatus | None = None
