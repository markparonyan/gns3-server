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

from typing import ClassVar, Tuple

from pydantic import BaseModel, ConfigDict, model_validator


def _remove_defaults(schema: dict) -> None:
    for property_schema in schema.get("properties", {}).values():
        property_schema.pop("default", None)


class PartialUpdateModel(BaseModel):
    """
    Turns a model into a partial update model: every field can be omitted, keeps its
    type and constraints, and publishes no default. The fields listed in
    `update_excluded_fields` are dropped. Use it as the first base of an update schema.
    """

    model_config = ConfigDict(json_schema_extra=_remove_defaults)

    update_excluded_fields: ClassVar[Tuple[str, ...]] = ()

    @model_validator(mode="before")
    @classmethod
    def _drop_excluded_fields(cls, data):
        if isinstance(data, dict):
            return {key: value for key, value in data.items() if key not in cls.update_excluded_fields}
        return data

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        for name in cls.update_excluded_fields:
            cls.model_fields.pop(name, None)
        for field in cls.model_fields.values():
            field.default = None
            field.default_factory = None
        cls.model_rebuild(force=True)
