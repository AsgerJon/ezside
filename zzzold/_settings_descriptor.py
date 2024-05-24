"""SettingsDescriptor class for the ezside app."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSettings, QCoreApplication, QObject
from attribox import AbstractDescriptor
from vistutils.waitaminute import typeMsg


class Settings(AbstractDescriptor):
  """SettingsDescriptor class for the ezside app."""

  def __instance_get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Implementation of the getter. The remaining functionality required
    by the descriptor protocol is implemented in the AbstractDescriptor
    class. """
    if instance is None:
      return self
    format_ = QSettings.Format.IniFormat
    scope = QSettings.Scope.UserScope
    app = QCoreApplication.instance()
    appName, orgName = app.applicationName(), app.organizationName()
    if isinstance(instance, QObject):
      return QSettings(format_, scope, orgName, appName, instance)
    e = typeMsg('instance', instance, QObject)
    raise TypeError(e)
