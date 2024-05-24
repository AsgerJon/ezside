"""BrushDesc implements the descriptor protocol for the QBrush instances. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QBrush

from ezside.app import EZDesc
from ezside.core import parseBrush


class Brush(EZDesc):
  """BrushDesc implements the descriptor protocol for the QBrush
  instances. """

  def getContentClass(self) -> type:
    """Returns the content class."""
    return QBrush

  def create(self, instance: object, owner: type, **kwargs) -> Any:
    """Create the content."""
    brush = parseBrush(*self.getArgs(), **self.getKwargs())
    if isinstance(brush, QBrush):
      return brush
    brush = self.settings.value(self.__settings_id__)
    if isinstance(brush, QBrush):
      return brush
