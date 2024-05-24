"""PointDesc implements the descriptor protocol for QPoint."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QPoint, QPointF

from ezside.app import EZDesc


class Point(EZDesc):
  """PointDesc implements the descriptor protocol for QPoint."""

  def getContentClass(self) -> type:
    """Returns the content class."""
    return QPoint

  def create(self, instance: object, owner: type, **kwargs) -> Any:
    """Create the content."""
    point = parsePoint(*self.getArgs(), **self.getKwargs())
    if isinstance(point, QPoint):
      return point
    if isinstance(point, QPointF):
      return point.toPoint()
    point = self.settings.value(self.__settings_id__)
    if isinstance(point, QPoint):
      return point
    if isinstance(point, QPointF):
      return point.toPoint()
