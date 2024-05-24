"""SettingsDesc exposes the AppSettings class through the descriptor
protocol. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from attribox import AbstractDescriptor
from PySide6.QtCore import QObject, QCoreApplication

if TYPE_CHECKING:
  from ezside.app import AppSettings
  from ezside.windows import App


class Settings(AbstractDescriptor):
  """SettingsDesc exposes the AppSettings class through the descriptor
  protocol. """

  def __instance_get__(self, instance: QObject, owner: type) -> AppSettings:
    """Implementation of the getter. The remaining functionality required
    by the descriptor protocol is implemented in the AbstractDescriptor
    class. """
    if instance is None:
      return self
    app = QCoreApplication.instance()
    if TYPE_CHECKING:
      assert isinstance(app, App)
    return app.settings
