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
#

"""
Schemas for the server settings endpoints (GET/PUT /v3/settings).

The VirtualBox and VMware sections are deprecated and intentionally not
exposed. Controller.jwt_secret_key is excluded everywhere: it is loaded
from the secrets directory and overrides whatever the configuration file
says, so exposing or writing it via the API would be useless at best and
a secret leak at worst.
"""

from pathlib import Path
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from ..config import (
    BuiltinSymbolTheme,
    ControllerSettings,
    DynamipsSettings,
    IOUSettings,
    QemuSettings,
    ServerProtocol,
    ServerSettings,
    UbridgeControlTransport,
    VPCSSettings,
    WebWiresharkSettings,
)

# matches the pydantic v2 SecretStr serialization mask
SECRET_MASK = "**********"


class ServerSettingsResponse(ServerSettings):
    # plain strings instead of FilePath/DirectoryPath: paths are validated when
    # the settings are loaded or updated, not when echoed back to the client
    secrets_dir: Path | None = Field(None, description="Directory where secrets are stored (e.g. the JWT secret key)")
    certfile: Path | None = Field(None, description="SSL certificate file, requires enable_ssl")
    certkey: Path | None = Field(None, description="SSL key file, requires enable_ssl")
    # Optional overrides: typed as plain "str = None" in the config schema,
    # which fails re-validation when the value actually is None
    resources_path: str | None = Field(
        None,
        description="Path where files like built-in appliances and Docker resources are stored "
        "(defaults to the local user data directory)",
    )
    default_nat_interface: str | None = Field(
        None, description="Interface used by the NAT node, default is virbr0 on Linux (requires libvirt)"
    )


class ControllerSettingsResponse(ControllerSettings):
    # never serialized: managed via the secrets directory, not the configuration file
    jwt_secret_key: str | None = Field(
        default=None,
        exclude=True,
        description="Secret key used to sign the JWT authentication tokens "
        "(normally managed via the secrets directory, not the configuration file)",
    )


class IOUSettingsResponse(IOUSettings):
    iourc_path: str | None = Field(
        None, description="Path of your .iourc file, the file is searched in $HOME/.iourc if not provided"
    )


class SettingsResponse(BaseModel):
    Server: ServerSettingsResponse
    Controller: ControllerSettingsResponse
    VPCS: VPCSSettings
    Dynamips: DynamipsSettings
    IOU: IOUSettingsResponse
    Qemu: QemuSettings
    WebWireshark: WebWiresharkSettings


class ServerSettingsUpdate(BaseModel):
    """
    Every field optional: JSON null removes the option from the configuration
    file (restoring its default), missing fields are left untouched.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    local: bool | None = None
    enable_http_auth: bool | None = None
    name: str | None = None
    protocol: ServerProtocol | None = None
    host: str | None = None
    port: int | None = Field(None, gt=0, le=65535)
    secrets_dir: str | None = None
    certfile: str | None = None
    certkey: str | None = None
    enable_ssl: bool | None = None
    images_path: str | None = None
    projects_path: str | None = None
    appliances_path: str | None = None
    symbols_path: str | None = None
    configs_path: str | None = None
    resources_path: str | None = None
    default_symbol_theme: BuiltinSymbolTheme | None = None
    allow_raw_images: bool | None = None
    auto_discover_images: bool | None = None
    image_sync_interval: int | None = Field(None, ge=10)
    report_errors: bool | None = None
    additional_images_paths: List[str] | None = None
    console_start_port_range: int | None = Field(None, gt=0, le=65535)
    console_end_port_range: int | None = Field(None, gt=0, le=65535)
    vnc_console_start_port_range: int | None = Field(None, ge=5900, le=65535)
    vnc_console_end_port_range: int | None = Field(None, ge=5900, le=65535)
    udp_start_port_range: int | None = Field(None, gt=0, le=65535)
    udp_end_port_range: int | None = Field(None, gt=0, le=65535)
    ubridge_path: str | None = None
    ubridge_control_transport: UbridgeControlTransport | None = None
    marker_listen_host: str | None = None
    marker_listen_port: int | None = Field(None, ge=0, le=65535)
    compute_username: str | None = None
    # plain str so the route can compare against SECRET_MASK / empty string
    compute_password: str | None = None
    allowed_interfaces: List[str] | None = None
    default_nat_interface: str | None = None
    allow_remote_console: bool | None = None
    enable_builtin_templates: bool | None = None
    install_builtin_appliances: bool | None = None
    skills_repo_url: str | None = None
    skills_repo_branch: str | None = None
    skills_auto_update: bool | None = None
    mcp_enable_dns_rebinding_protection: bool | None = None
    mcp_allowed_hosts: List[str] | None = None
    mcp_allowed_origins: List[str] | None = None


class ControllerSettingsUpdate(BaseModel):
    """
    No jwt_secret_key field on purpose (see module docstring).
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    jwt_algorithm: str | None = None
    jwt_access_token_expire_minutes: int | None = None
    jwt_refresh_token_expire_minutes: int | None = None
    default_admin_username: str | None = None
    default_admin_password: str | None = None


class VPCSSettingsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    vpcs_path: str | None = None


class DynamipsSettingsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    allocate_aux_console_ports: bool | None = None
    mmap_support: bool | None = None
    dynamips_path: str | None = None
    sparse_memory_support: bool | None = None
    ghost_ios_support: bool | None = None


class IOUSettingsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    iourc_path: str | None = None
    license_check: bool | None = None


class QemuSettingsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    enable_monitor: bool | None = None
    monitor_host: str | None = None
    enable_hardware_acceleration: bool | None = None
    require_hardware_acceleration: bool | None = None
    allow_unsafe_options: bool | None = None
    ovmf_firmware_dir: str | None = None


class WebWiresharkSettingsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    enabled: bool | None = None
    image: str | None = None
    network_subnet: str | None = None
    memory: str | None = None
    cpus: float | None = None
    pids_limit: int | None = None


class SettingsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    Server: ServerSettingsUpdate | None = None
    Controller: ControllerSettingsUpdate | None = None
    VPCS: VPCSSettingsUpdate | None = None
    Dynamips: DynamipsSettingsUpdate | None = None
    IOU: IOUSettingsUpdate | None = None
    Qemu: QemuSettingsUpdate | None = None
    WebWireshark: WebWiresharkSettingsUpdate | None = None


class SettingsUpdateResponse(SettingsResponse):
    restart_required: List[str] = Field(
        default_factory=list,
        description="Changed 'Section.option' settings that require a server restart to take effect",
    )
