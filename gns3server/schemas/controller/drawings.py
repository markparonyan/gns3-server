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

from pydantic import BaseModel, Field


class Drawing(BaseModel):
    """
    Drawing data.
    """

    drawing_id: UUID | None = None
    project_id: UUID | None = None
    x: int | None = None
    y: int | None = None
    z: int | None = None
    locked: bool | None = None
    rotation: int | None = Field(None, ge=-359, le=360)
    svg: str | None = None
