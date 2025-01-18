"""TextModel encapsulates text painting on a widget. Instances provide
both the current text, font and pen settings. Widget classes requiring
text should an instance of this class which implements the descriptor
protocol. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtGui import QFontMetrics, QPainter
from worktoy.parse import maybe
from worktoy.base import BaseObject, overload
from worktoy.text import wordWrap, typeMsg
from worktoy.desc import AttriBox, Field

from . import EmptyPen, EmptyBrush, Font, Size, Rect, RGBA, Margin
from . import FontFamily
from ..enums import Align


class TextModel(BaseObject):
  """TextModel encapsulates text painting on a widget. Instances provide
  both the current text, font and pen settings. Widget classes requiring
  text should an instance of this class which implements the descriptor
  protocol. """

  text = AttriBox[str]('label')
  lineLength = AttriBox[int](-1)  # Characters per line (-1 for no limit)
  font = AttriBox[Font]()
  fontColor = AttriBox[RGBA](0, 0, 0, 255)
  shadowMargin = AttriBox[Margin](4, 1, 4, 1)
  shadowFill = AttriBox[RGBA](223, 223, 223, 255)
  shadowBorder = AttriBox[RGBA](0, 0, 0, 255)
  align = AttriBox[Align]('CENTER')

  textLines = Field()  # The text split into lines in a list
  requiredSize = Field()  # The size necessary for the text to be displayed
  shadowSize = Field()

  emptyPen = EmptyPen()
  emptyBrush = EmptyBrush()

  @textLines.GET
  def _getTextLines(self) -> list[str]:
    """Getter-function for the text split into lines in a list. """
    if self.lineLength < 0:
      return self.text.split('\n')
    if self.lineLength:
      return wordWrap(self.lineLength, self.text)
    e = """Received zero line-length!"""
    raise ValueError(e)

  @requiredSize.GET
  def getRequiredSize(self, ) -> Size:
    """Getter-function for the size necessary for the text to be
    displayed. """
    if TYPE_CHECKING:
      assert isinstance(self.font.metrics, QFontMetrics)
      assert isinstance(self.textLines, list)
    width, height = 0, 0
    for line in self.textLines or ['DEFAULT']:
      line = """ %s """ % line
      lineSize = self.font.metrics.boundingRect(line).size()
      width = max(width, lineSize.width())
      height += lineSize.height()
    n = len(self.textLines) or 1
    lineSpace = self.font.metrics.lineSpacing()
    return Size(width, height + (n - 1) * lineSpace)

  @shadowSize.GET
  def _getShadowSize(self) -> Size:
    """Getter-function for the size of the shadow. """
    if TYPE_CHECKING:
      assert isinstance(self.requiredSize, Size)
      assert isinstance(self.shadowMargin, Margin)
    return self.requiredSize + self.shadowMargin

  def __str__(self, ) -> str:
    """Returns the text wrapped to fit the line length. """
    if TYPE_CHECKING:
      assert isinstance(self.textLines, list)
      assert isinstance(self.textLines[0], str)
    return '\n'.join(self.textLines)

  def __repr__(self, ) -> str:
    """Code representation of the text model. """
    if TYPE_CHECKING:
      assert isinstance(self.text, str)
      assert isinstance(self.font, Font)
      assert isinstance(self.align, Align)
    textBit = self.text if len(self.text) < 20 else self.text[:17] + '...'
    family = self.font.family.name
    alignName = self.align.name
    lineLen = ', %d' % self.lineLength if self.lineLength > 0 else ''
    fmtSpec = """<TextModel Object: %s, %s, %s%s>"""
    return fmtSpec % (textBit, family, alignName, lineLen)

  @overload()
  def __init__(self, ) -> None:
    pass

  @overload(str)
  def __init__(self, text: str) -> None:
    self.text = text

  @overload(str, str)
  def __init__(self, text: str, family: str) -> None:
    self.text = text
    if family in Align:
      self.align = Align(family)
    elif family in FontFamily:
      self.font = Font(family)

  @overload(str, Font)
  def __init__(self, text: str, font: Font) -> None:
    self.text = text
    self.font = font

  @overload(str, int)
  def __init__(self, text: str, lineLen: int) -> None:
    self.text = text
    self.lineLength = lineLen

  @overload(str, int, int)
  def __init__(self, text: str, lineLen: int, fontSize: int) -> None:
    self.text = text
    self.lineLength = lineLen
    self.font = Font(fontSize)

  @overload(str, str, int)
  def __init__(self, text: str, family: str, lineLen: int) -> None:
    self.text = text
    if family in Align:
      self.align = Align(family)
    elif family in FontFamily:
      self.font = Font(family, )
    self.lineLength = lineLen

  @overload(str, str, int, int)
  def __init__(self, *args) -> None:
    strArgs = [arg for arg in args if isinstance(arg, str)]
    intArgs = [arg for arg in args if isinstance(arg, int)]
    self.text, arg = strArgs
    self.lineLength, fontSize = intArgs
    if arg in Align:
      self.align = Align(arg)
      self.font = Font(fontSize)
    else:
      self.font = Font(arg, fontSize)

  def readyTextPainter(self, painter: QPainter) -> QPainter:
    """Sets the painter up for painting the text. """
    if TYPE_CHECKING:
      assert isinstance(self.font, Font)
      assert isinstance(self.fontColor, RGBA)
    painter.setFont(self.font.Q)
    painter.setPen(self.fontColor.pen)
    painter.setBrush(self.emptyBrush)
    return painter

  def readyShadowPainter(self, painter: QPainter) -> QPainter:
    """Sets the painter up for painting the shadow. """
    if TYPE_CHECKING:
      assert isinstance(self.shadowFill, RGBA)
    painter.setPen(self.emptyPen)
    painter.setBrush(self.shadowFill.brush)
    return painter

  def fitText(self, targetRect: Rect) -> Rect:
    """Fits the text into the target rectangle as demanded by the
    alignment. """
    if TYPE_CHECKING:
      assert isinstance(self.align, Align)
      assert isinstance(self.requiredSize, Size)
    return self.align.apply(targetRect, self.requiredSize)

  def fitShadow(self, targetRect: Rect) -> Rect:
    """Fits the shadow into the target rectangle. """
    if TYPE_CHECKING:
      assert isinstance(self.shadowMargin, Margin)
      assert isinstance(self.shadowSize, Size)
      assert isinstance(self.align, Align)
    return self.align.apply(targetRect, self.shadowSize)

  def paint(self, painter: QPainter, rect: Rect) -> QPainter:
    """Paints the text on the given rectangle. """
    if TYPE_CHECKING:
      assert isinstance(self.shadowMargin, Margin)
      assert isinstance(self.shadowSize, Size)
      assert isinstance(self.align, Align)
    shadowRect = self.fitShadow(rect)
    textRect = self.fitText(rect)

    painter.setPen(self.shadowBorder.pen)
    painter.setBrush(self.shadowFill.brush)
    painter.drawRect(shadowRect.Q)
    painter.setPen(self.fontColor.pen)
    painter.setBrush(self.emptyBrush)
    painter.setFont(self.font.Q)
    alignFlag = self.align.Q
    painter.drawText(textRect.Q, alignFlag, str(self))
    return painter
