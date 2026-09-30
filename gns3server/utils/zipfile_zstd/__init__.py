# NOTE: this patches the standard zipfile module
from zipfile import *  # noqa: F403

from . import _zipfile  # noqa: F401
from ._zipfile import ZIP_ZSTANDARD, ZSTANDARD_VERSION  # noqa: F401
