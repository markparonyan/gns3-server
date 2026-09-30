#
# Software Name : GNS3 server
# Version: 3
# SPDX-FileCopyrightText: Copyright (c) 2023 Orange Business Services
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This software is distributed under the GPL-3.0 or any later version,
# the text of which is available at https://www.gnu.org/licenses/gpl-3.0.txt
# or see the "LICENSE" file for more details.
#
# Author: Sylvain MATHIEU
#

"""
API route for privileges
"""

import logging

from fastapi import APIRouter, Depends

import gns3server.db.models as models
from gns3server import schemas
from gns3server.db.repositories.rbac import RbacRepository

from .dependencies.database import get_repository

log = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "",
    response_model=list[schemas.Privilege],
)
async def get_privileges(
    rbac_repo: RbacRepository = Depends(get_repository(RbacRepository)),
) -> list[models.Privilege]:
    """
    Get all privileges.

    Required privilege: None
    """

    return await rbac_repo.get_privileges()
