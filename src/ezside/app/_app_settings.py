"""AppSettings provides a subclass of QSettings suitable for use in
an instance of AttriBox"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSettings, QCoreApplication
from icecream import ic

ic.configureOutput(includeContext=True, )


class AppSettings(QSettings):
  """AppSettings provides a subclass of QSettings suitable for use in
  an instance of AttriBox"""

  __running_app__ = None

  def __init__(self, app: QCoreApplication) -> None:
    QSettings.__init__(self, app.organizationName(), app.applicationName())
    self.__running_app__ = app

  def getApp(self) -> QCoreApplication:
    """Getter-function for the app"""
    return self.__running_app__

  def __getattribute__(self, key: str) -> Any:
    """Forwards call to QSettings.value(self, key) as appropriate."""
    try:
      value = object.__getattribute__(self, key)
    except AttributeError as attributeError:

      try:
        value = self.value(key, )
      except Exception as exception:
        raise exception from attributeError
    return value

  def __setattr__(self, key: str, value: Any) -> None:
    """Forwards call to QSettings.setValue(self, key, value)"""
    try:
      object.__getattribute__(self, key, )
      object.__setattr__(self, key, value)
    except AttributeError as attributeError:
      self.setValue(key, value)

  def value(self, *args, **kwargs) -> Any:
    """Returns the value of the key"""
    key, fallback = [*args, None]
    if fallback is None:
      return QSettings.value(self, key, **kwargs)
    try:
      return QSettings.value(self, key, **kwargs)
    except KeyError as keyError:
      self.__missing_names__.append(key)
      return fallback
