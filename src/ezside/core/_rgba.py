"""RGBA encapsulates colors in the RGB color space including an alpha
channel."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Self

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QPen
from worktoy.desc import AttriBox, THIS, Field
from worktoy.base import BaseObject, overload


class InvalidHexException(ValueError):
  """InvalidHexException is raised when a hex color string is not valid. """
  pass


class RGBA(BaseObject):
  """RGBA encapsulates colors in the RGB color space including an alpha
  channel."""

  red = AttriBox[int](0)
  green = AttriBox[int](0)
  blue = AttriBox[int](0)
  alpha = AttriBox[int](255)

  Q = Field()
  brush = Field()
  pen = Field()

  @Q.GET
  def _getQColor(self) -> QColor:
    return QColor(self.red, self.green, self.blue, self.alpha)

  @brush.GET
  def _getBrush(self) -> QBrush:
    """Getter-function for simple brush filling with this color. """
    brush = QBrush()
    brush.setColor(self.Q)
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    return brush

  @pen.GET
  def _getPen(self) -> QPen:
    """Getter-function for simple pen drawing with this color. """
    pen = QPen()
    pen.setColor(self.Q)
    pen.setStyle(Qt.PenStyle.SolidLine)
    pen.setWidth(1)
    return pen

  @overload(int, int, int, int)
  def __init__(self, R: int, G: int, B: int, A: int) -> None:
    self.red = R
    self.green = G
    self.blue = B
    self.alpha = A

  @overload(int, int, int)
  def __init__(self, R: int, G: int, B: int) -> None:
    self.red = R
    self.green = G
    self.blue = B
    self.alpha = 255

  @overload(int)
  def __init__(self, A: int) -> None:
    self.red = A
    self.green = A
    self.blue = A
    self.alpha = 255

  @overload()
  def __init__(self, **kwargs) -> None:
    self.red = kwargs.get('red', 0)
    self.green = kwargs.get('green', 0)
    self.blue = kwargs.get('blue', 0)
    self.alpha = kwargs.get('alpha', 255)

  @overload(THIS)
  def __init__(self, other: RGBA) -> None:
    self.red = other.red
    self.green = other.green
    self.blue = other.blue
    self.alpha = other.alpha

  @overload(QColor)
  def __init__(self, other: QColor) -> None:
    self.red = other.red()
    self.green = other.green()
    self.blue = other.blue()
    self.alpha = other.alpha()

  @overload(tuple)
  def __init__(self, args: tuple) -> None:
    if TYPE_CHECKING:
      assert callable(self.__init__)
    self.__init__(*args)

  @overload(list)
  def __init__(self, args: list) -> None:
    if TYPE_CHECKING:
      assert callable(self.__init__)
    self.__init__(*args)

  @overload(dict)
  def __init__(self, args: dict) -> None:
    if TYPE_CHECKING:
      assert callable(self.__init__)
    self.__init__(**args)

  @overload(str)
  def __init__(self, data: str) -> None:
    if TYPE_CHECKING:
      assert callable(self.__init__)
    try:
      r, g, b, a = self._parseHex(data)
    except InvalidHexException:
      try:
        r, g, b, a = self._parseName(data)
      except NameError:
        try:
          rgb = json.loads(data)
          r = rgb['red']
          g = rgb['green']
          b = rgb['blue']
          a = rgb.get('alpha', 255)
        except json.JSONDecodeError:
          raise ValueError(data)

  @classmethod
  def _parseHex(cls, hexColor: str) -> tuple[int, int, int, int]:
    """Parses a hex color string into a tuple of RGBA values. """

    if not hexColor.startswith('#'):
      raise InvalidHexException(hexColor)

    hexColor = hexColor[1:].lower()
    for char in hexColor:
      if char not in '0123456789abcdef':
        raise InvalidHexException(hexColor)

    if len(hexColor[1:]) not in [6, 8]:
      raise InvalidHexException(hexColor)

    if len(hexColor) == 6:
      return cls._parseHex('%sff' % hexColor)

    R = int(hexColor[:2], 16)
    G = int(hexColor[2:4], 16)
    B = int(hexColor[4:6], 16)
    A = int(hexColor[6:], 16)

    return R, G, B, A

  @classmethod
  def _parseName(cls, colorName: str) -> tuple[int, int, int, int]:
    """Parses a color name into a tuple of RGBA values. """

    colors = {
        "red"    : (255, 0, 0),
        "green"  : (0, 128, 0),
        "blue"   : (0, 0, 255),
        "yellow" : (255, 255, 0),
        "cyan"   : (0, 255, 255),
        "magenta": (255, 0, 255),
        "black"  : (0, 0, 0),
        "white"  : (255, 255, 255),
        "gray"   : (128, 128, 128),
        "orange" : (255, 165, 0),
        "purple" : (128, 0, 128),
        "pink"   : (255, 192, 203),
        "brown"  : (165, 42, 42)
    }

    if colorName not in colors:
      e = """%s is not recognized as the name of a color!""" % colorName
      raise NameError(e)

    r, g, b = colors[colorName]
    return r, g, b, 255
