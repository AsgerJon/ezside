"""Brush implements the descriptor protocol for QBrush."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Optional

from PySide6.QtGui import QBrush, QColor

from ezside.app import EZObject, MissingSettingsError
from ezside.desc import SettingsDescriptor, parseColour, FillStyle
from ezside.desc import SolidFill, Black, NoFill


def emptyBrush() -> QBrush:
  """Returns an empty brush."""
  brush = QBrush()
  brush.setStyle(NoFill)
  brush.setColor(QColor(0, 0, 0, 0))
  return brush


def parseBrush(*args, **kwargs) -> Optional[QBrush]:
  """Parses the arguments and returns a QBrush."""
  brush, fillStyle, fillColor = QBrush(), None, parseColour(*args, )
  if fillColor is None:
    fillColor = kwargs.get('fillColor', None)
    if fillColor is None:
      return
  brush.setColor(fillColor)
  for arg in args:
    if isinstance(arg, FillStyle):
      brush.setStyle(arg)
      return brush
  fillStyle = kwargs.get('fillStyle', SolidFill)
  brush.setStyle(fillStyle)
  return brush


class Brush(SettingsDescriptor):
  """Brush implements the descriptor protocol for QBrush."""

  def getContentClass(self) -> type:
    """Returns the content class."""
    return QBrush

  def create(self, instance: EZObject, owner: type, **kwargs) -> QBrush:
    """Create the content."""
    brush = parseBrush(*self.getArgs())
    if isinstance(brush, QBrush):
      return brush
    raise MissingSettingsError(self.__class__.__name__)

  def getFallbackValues(self) -> dict[str, Any]:
    """Returns the fallback values."""
    return {
      'normal/brush/margins' : emptyBrush(),
      'normal/brush/borders' : parseBrush(Black, SolidFill),
      'normal/brush/paddings': emptyBrush(),
    }
