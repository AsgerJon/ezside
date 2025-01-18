"""Font encapsulates font settings. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPen, QFontMetrics
from worktoy.parse import maybe
from worktoy.text import typeMsg
from worktoy.desc import AttriBox, THIS, Field
from worktoy.base import BaseObject, overload

from . import FontFamily, RGBA


class Font(BaseObject):
  """Font encapsulates font settings. """

  __fallback_weight__ = 500
  __font_weight__ = None

  family = AttriBox[FontFamily]()
  ptSize = AttriBox[int](12)
  italic = AttriBox[bool](False)
  underline = AttriBox[bool](False)
  color = AttriBox[RGBA](0, 0, 0, 255)

  weight = Field()
  Q = Field()
  pen = Field()
  metrics = Field()

  @weight.GET
  def _getWeight(self) -> QFont.Weight:
    w = maybe(self.__font_weight__, self.__fallback_weight__)
    for item in QFont.Weight:
      if item.value == w:
        return item
    e = """The font weight: '%s' is not supported by the current
    application!""" % w
    raise ValueError(e)

  @Q.GET
  def _getQFont(self) -> QFont:
    if TYPE_CHECKING:
      assert isinstance(self.family, FontFamily)
      assert isinstance(self.ptSize, int)
      assert isinstance(self.weight, QFont.Weight)
      assert isinstance(self.italic, bool)
      assert isinstance(self.underline, bool)
    font = QFont()
    font.setFamily(self.family.name)
    font.setPointSize(self.ptSize)
    font.setWeight(self.weight)
    font.setItalic(self.italic)
    font.setUnderline(self.underline)
    return font

  @pen.GET
  def _getPen(self) -> QPen:
    pen = QPen()
    pen.setStyle(Qt.PenStyle.SolidLine)
    pen.setWidth(1)
    pen.setColor(self.color.Q)
    return pen

  @metrics.GET
  def _getMetrics(self) -> QFontMetrics:
    if TYPE_CHECKING:
      assert isinstance(self.Q, QFont)
    return QFontMetrics(self.Q)

  def _applyKwargs(self, **kwargs) -> None:
    """This method applies keyword arguments. """
    if 'weight' in kwargs:
      weight = kwargs['weight']
      if weight is True:
        self.weight = 700
      elif weight is False:
        self.weight = 500
      elif isinstance(weight, int):
        self.weight = weight
      else:
        e = typeMsg('weight', weight, int)
        raise TypeError(e)
    if 'italic' in kwargs:
      italic = kwargs['italic']
      if isinstance(italic, bool):
        self.italic = True if italic else False
    if 'underline' in kwargs:
      underline = kwargs['underline']
      if isinstance(underline, bool):
        self.underline = True if underline else False

  @overload(FontFamily, int)
  def __init__(self, family: FontFamily, ptSize: int, **kwargs) -> None:
    self.family = family
    self.ptSize = ptSize
    self._applyKwargs(**kwargs)

  @overload(str)
  def __init__(self, familyName: str, **kwargs) -> None:
    self.family = FontFamily(familyName)
    self.ptSize = 12
    self._applyKwargs(**kwargs)

  @overload(str, int)
  def __init__(self, family: str, ptSize: int, **kwargs) -> None:
    self.family = FontFamily(family)
    self.ptSize = ptSize
    self._applyKwargs(**kwargs)

  @overload(QFont)
  def __init__(self, font: QFont) -> None:
    self.family = FontFamily(font)
    self.ptSize = font.pointSize()
    self.weight = font.weight()
    self.italic = font.italic()
    self.underline = font.underline()

  @overload(THIS)
  def __init__(self, other: Font) -> None:
    self.family = other.family
    self.ptSize = other.ptSize
    self.weight = other.weight
    self.italic = other.italic
    self.underline = other.underline

  @overload(int)
  def __init__(self, ptSize: int) -> None:
    self.family = FontFamily('MesloLGS NF')
    self.ptSize = ptSize

  @overload()
  def __init__(self) -> None:
    self.family = FontFamily('MesloLGS NF')
    self.ptSize = 12
