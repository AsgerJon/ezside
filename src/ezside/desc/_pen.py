"""Pen implements a descriptor protocol for QPen."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional, Any

from PySide6.QtGui import QPen, QColor

from ezside.app import EZObject, MissingSettingsError
from ezside.desc import SettingsDescriptor, \
  LineStyle, \
  parseColor, \
  SolidLine, \
  NoPen, Black


def emptyPen() -> QPen:
  """Returns an empty pen."""
  pen = QPen()
  pen.setStyle(NoPen)
  pen.setColor(QColor(0, 0, 0, 0))
  return pen


def parsePen(*args) -> Optional[QPen]:
  """Parse a pen from a list of arguments."""
  width, style, color = None, None, None
  for arg in args:
    if isinstance(arg, QPen):
      return arg
    if isinstance(arg, LineStyle) and style is None:
      style = arg
    if isinstance(arg, QColor) and color is None:
      color = arg
    if isinstance(arg, int) and width is None:
      width = arg
  pen = QPen()
  if color is None:
    color = parseColor(*args, )
    if color is None:
      return
  pen.setColor(color)
  pen.setStyle(SolidLine if style is None else style)
  pen.setWidth(1 if width is None else width)
  return pen


class Pen(SettingsDescriptor):
  """Pen implements a descriptor protocol for QPen."""

  def getContentClass(self) -> type:
    """Returns the content class for the pen."""
    return QPen

  def create(self, instance: EZObject, owner: type, **kwargs) -> QPen:
    """Creates the pen."""
    pen = parsePen(*self.getArgs())
    if isinstance(pen, QPen):
      return pen
    raise MissingSettingsError(self.__class__.__name__)

  def getFallbackValues(self) -> dict[str, Any]:
    """Returns the fallback values."""
    return {
      'normal/pen': parsePen(Black, SolidLine, 1),
    }
