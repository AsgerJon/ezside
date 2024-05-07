"""AppSettings subclasses the QSettings class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon, QKeySequence
from icecream import ic

from ezside.app import BaseSettings

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True, )


class AppSettings(BaseSettings):
  """The 'AppSettings' class provides a convenient interface for
  working with the application's variable settings. """

  def __init__(self, *args) -> None:
    """Initialize the AppSettings object."""
    QSettings.__init__(self, *args)
    self.beginGroup('icon', QIcon)
    for name, path in self._getIcons().items():
      self.setValue(name, QIcon(path))
    self.endGroup(QIcon(self._getIcons('risitas')))
    self.beginGroup('shortcut', QKeySequence)
    for name, shortcut in self._getKeyboardShortcuts().items():
      self.setValue(name, QKeySequence(shortcut))
    self.endGroup(QKeySequence())
