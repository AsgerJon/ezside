"""The 'ezside.app' package provides convenient functions for implementing
and customizing application wide functionalities. Please note that this
does not include the implementation of the QCoreApplication itself. The
design pattern of this framework requires that all implemented classes are
available to the instances of QCoreApplication before it is runs. This
means that the application should be imported last making it unavailable
for import by other modules. The general nature of the functionalities
implemented here, means that the objs here should be the first to be
imported."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._app_desc import AppDesc
from ._settings_desc import Settings
from ._missing_settings_error import MissingSettingsError
from ._casting_exception import CastingException
from ._ez_object import EZObject
from ._ez_desc import EZDesc
from ._app_settings import AppSettings
