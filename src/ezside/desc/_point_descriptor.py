"""PointDescriptor implements the descriptor protocol for the Point class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QPoint, QPointF

from ezside.desc import SettingsDescriptor


def parsePoint(*args, **kwargs) -> QPoint:
  """Parse the Point arguments."""
  x, y = kwargs.get('x', None), kwargs.get('y', None)
  if isinstance(x, int) and isinstance(y, int):
    return QPoint(x, y)
  intArgs = []
  for arg in args:
    if isinstance(arg, QPoint):
      return arg
    if isinstance(arg, QPointF):
      return arg.toPoint()
    if isinstance(arg, int):
      intArgs.append(arg)
  if len(intArgs) > 1:
    return QPoint(*intArgs[:2])


class Point(SettingsDescriptor):
  """PointDescriptor implements the descriptor protocol for the Point
  class."""

  def getContentClass(self) -> type:
    """Returns the content class."""
    return QPoint

  def create(self, instance: object, owner: type, **kwargs) -> QPoint:
    """Create the content."""
    point = parsePoint(*self.getArgs(), **self.getKwargs())
    if point is None:
      return QPoint(0, 0)
    return point
