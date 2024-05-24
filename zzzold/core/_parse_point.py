"""The 'parsePoint' parses an instance of QPoint from the given arguments."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QPoint, QPointF


def parsePoint(*args, **kwargs) -> Optional[QPoint]:
  """The 'parsePoint' parses an instance of QPoint from the given
  arguments."""
  x, y = None, None

  for arg in args:
    if isinstance(arg, QPoint):
      return arg
    if isinstance(arg, QPointF):
      return arg.toPoint()
    if isinstance(arg, int):
      if x is None:
        x = arg
      elif y is None:
        return QPoint(x, arg)
