"""Font implements the descriptor protocol for QFont."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtGui import QFont

from ezside.app import EZDesc
from ezside.core import parseFont

if TYPE_CHECKING:
  from ezside.app import EZObject


class Font(EZDesc):
  """Font implements the descriptor protocol for QFont."""

  def getContentClass(self) -> type:
    """Returns the content class."""
    return QFont

  def create(self,
             instance: EZObject,
             owner: type,
             **kwargs) -> QFont:
    """Create the content."""
    font = parseFont(*self.getArgs(), **self.getKwargs())
    if isinstance(font, QFont):
      return font
    settingsKey = '%s/font' % instance.settingsId
    font = self.settings.value(self.__settings_id__)
    if isinstance(font, QFont):
      return font
