"""RGB encapsulates red, green and blue composite colour."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QPen
from attribox import AttriBox
from vistutils.ezdata import EZData
from vistutils.parse import maybe
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import SolidFill


class RGB:
  """RGB encapsulates red, green and blue composite colour."""

  __common_colors__ = {
    'lime': [144, 255, 0],
    'red': [255, 0, 0],
    'blue': [0, 0, 255],
    'yellow': [255, 255, 0],
    'cyan': [0, 255, 255],
    'magenta': [255, 0, 255],
    'white': [255, 255, 255],
    'black': [0, 0, 0],
  }

  red = AttriBox[int](0)
  green = AttriBox[int](0)
  blue = AttriBox[int](0)
  alpha = AttriBox[int](255)

  @classmethod
  def fromName(cls, colorName: str) -> Optional[list[int]]:
    """Returns a common colour by name."""
    return cls.__common_colors__.get(colorName, None)

  @classmethod
  def fromHex(cls, hexColor: str) -> Optional[list[int]]:
    """Converts a string to an RGB instance."""
    if not hexColor.startswith('#'):
      return None
    if len(hexColor) not in [7, 9]:
      return None
    for i in hexColor[1:]:
      if i not in '0123456789ABCDEF':
        return None
    if len(hexColor) == 7:
      hexColor += 'FF'
    return [int(hexColor[i:i + 2], 16) for i in (1, 3, 5, 7)]

  @classmethod
  def fromQColor(cls, qColor: QColor) -> Optional[list[int]]:
    """Converts a QColor to an RGB instance."""
    return [qColor.red(), qColor.green(), qColor.blue(), qColor.alpha()]

  def __init__(self, *args, **kwargs) -> None:
    rgb = self.fromName(args[0])
    if rgb is None:
      rgb = self.fromHex(args[0])
    if rgb is None:
      rgb = self.fromQColor(args[0])
    if rgb is None:
      e = """Unable to parse color!"""
      raise ValueError(e)
    self.red, self.green, self.blue, self.alpha = rgb[:4]

  def getQColor(self) -> QColor:
    """Returns a QColor representation of the RGB colour."""
    return QColor(self.red, self.green, self.blue, self.alpha)

  def getBrush(self) -> QBrush:
    """Returns a QBrush representation of the RGB colour."""
    brush = QBrush()
    brush.setColor(self.getQColor())
    brush.setStyle(SolidFill)
    return brush

  def getPen(self, penStyle: Qt.PenStyle = None) -> QPen:
    """Returns a QPen representation of the RGB colour."""
    if penStyle is None:
      penStyle = Qt.PenStyle.SolidLine
    if not isinstance(penStyle, Qt.PenStyle):
      e = typeMsg('penStyle', penStyle, Qt.PenStyle)
      raise TypeError(e)
    pen = QPen()
    pen.setColor(self.getQColor())
    pen.setStyle(penStyle)
    return pen

  def toStr(self) -> str:
    """Converts the RGB instance to a string."""
    rgba = [self.red, self.green, self.blue, self.alpha]
    return '#' + ''.join(f'{c:02X}' for c in rgba)

  def __str__(self) -> str:
    """Returns a string representation of the RGB instance."""
    return self.toStr()

  def __repr__(self) -> str:
    """Returns a string representation of the RGB instance."""
    return 'RGB(%d, %d, %d, %d)' % (
      self.red, self.green, self.blue, self.alpha)
