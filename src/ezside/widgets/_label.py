"""Label provides a widget for showing short and single-line text. If
longer text is required use the TextBox widget instead, which provide
support for multi-line text. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QRect, QSize, QPoint, QMargins
from PySide6.QtGui import QFont, QColor, QPen, QFontMetrics, QBrush
from attribox import AttriBox
from vistutils.fields import EmptyField
from vistutils.waitaminute import typeMsg

from ezside.app import EZDesc
from ezside.desc import Bold, \
  AlignHCenter, \
  AlignLeft, \
  AlignVCenter, \
  AlignTop, \
  SolidFill, AlignCenter
from ezside.desc import SolidLine, AlignFlag

from ezside.widgets import CanvasWidget, GraffitiVandal


class LabelWidget(CanvasWidget):
  """Label provides a widget for showing short and single-line text. If
  longer text is required use the TextBox widget instead, which provide
  support for multi-line text. """

  __style_id__ = None
  text = AttriBox[str]()
  textFont = EmptyField()
  textPen = EmptyField()
  textBackgroundBrush = EmptyField()
  textRect = EmptyField()
  textSize = EmptyField()
  textWidth = EmptyField()
  textHeight = EmptyField()
  hAlign = EmptyField()
  vAlign = EmptyField()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the Label."""
    CanvasWidget.__init__(self, *args, **kwargs)
    for arg in args:
      if isinstance(arg, str):
        self.text = arg
        break
    self.__style_id__ = kwargs.get('id', 'normal')

  @textBackgroundBrush.GET
  def getTextBackgroundBrush(self) -> QBrush:
    """Returns the background brush for the text."""
    if self.__style_id__ == 'warning':
      color = QColor(255, 255, 0, 255)
    else:
      color = QColor(223, 223, 223, 255)
    brush = QBrush()
    brush.setStyle(SolidFill)
    brush.setColor(color)
    return brush

  @textFont.GET
  def getFont(self) -> QFont:
    """Returns the font for the text."""
    if self.__style_id__ == 'normal':
      font = QFont()
      font.setFamily('MesloLGS NF')
      font.setPointSize(12)
      return font
    if self.__style_id__ == 'title':
      font = QFont()
      font.setFamily('MesloLGS NF')
      font.setPointSize(20)
      return font
    if self.__style_id__ == 'header':
      font = QFont()
      font.setFamily('MesloLGS NF')
      font.setPointSize(16)
      return font
    if self.__style_id__ == 'warning':
      font = QFont()
      font.setFamily('MesloLGS NF')
      font.setPointSize(12)
      font.setWeight(Bold)
      return font
    if self.__style_id__ == 'info':
      font = QFont()
      font.setFamily('MesloLGS NF')
      font.setPointSize(12)
      font.setItalic(True)
      return font

  @textRect.GET
  def getTextRect(self) -> QRect:
    """Returns the rectangle for the text."""
    if not isinstance(self.textFont, QFont):
      e = typeMsg('textFont', self.textFont, QFont)
      raise TypeError(e)
    if not isinstance(self.text, str):
      e = typeMsg('text', self.text, str)
      raise TypeError(e)
    fontMetrics = QFontMetrics(self.textFont)
    return fontMetrics.boundingRect(' %s ' % self.text)

  @textSize.GET
  def getTextSize(self) -> QSize:
    """Returns the size of the text."""
    if not isinstance(self.textRect, QRect):
      e = typeMsg('textRect', self.textRect, QRect)
      raise TypeError(e)
    return self.textRect.size()

  @textWidth.GET
  def getTextWidth(self) -> int:
    """Returns the width of the text."""
    if not isinstance(self.textSize, QSize):
      e = typeMsg('textSize', self.textSize, QSize)
      raise TypeError(e)
    return self.textSize.width()

  @textHeight.GET
  def getTextHeight(self) -> int:
    """Returns the height of the text."""
    if not isinstance(self.textSize, QSize):
      e = typeMsg('textSize', self.textSize, QSize)
      raise TypeError(e)
    return self.textSize.height()

  @textPen.GET
  def getTextPen(self) -> QPen:
    """Returns the pen for the text."""
    if self.__style_id__ == 'warning':
      color = QColor(255, 0, 0, 255)
    else:
      color = QColor(0, 0, 0, 255)
    pen = QPen()
    pen.setStyle(SolidLine)
    pen.setColor(color)
    pen.setWidth(1)
    return pen

  @hAlign.GET
  def getHAlign(self) -> AlignFlag:
    """Returns the horizontal alignment."""
    if self.__style_id__ == 'title':
      return AlignHCenter
    return AlignLeft

  @vAlign.GET
  def getVAlign(self) -> AlignFlag:
    """Returns the vertical alignment."""
    if self.__style_id__ == 'title':
      return AlignVCenter
    return AlignLeft

  def _align(self, viewRect: QRect) -> QRect:
    """Aligns text rect in view rect."""
    if not isinstance(self.textWidth, int):
      e = typeMsg('textWidth', self.textWidth, int)
      raise TypeError(e)
    if self.hAlign == AlignLeft:
      left = viewRect.left()
    elif self.hAlign == AlignHCenter:
      left = viewRect.left() + (viewRect.width() - self.textWidth) // 2
    else:
      left = viewRect.right() - self.textWidth
    if not isinstance(self.textHeight, int):
      e = typeMsg('textHeight', self.textHeight, int)
      raise TypeError(e)
    if self.vAlign == AlignTop:
      top = viewRect.top()
    elif self.vAlign == AlignVCenter:
      top = viewRect.top() + (viewRect.height() - self.textHeight) // 2
    else:
      top = viewRect.bottom() - self.textHeight
    if not isinstance(self.textSize, QSize):
      e = typeMsg('textSize', self.textSize, QSize)
      raise TypeError(e)
    topLeft = QPoint(int(left), int(top))
    return QRect(topLeft, self.textSize)

  def customPaint(self, painter: GraffitiVandal) -> None:
    """Custom paint event."""
    viewRect = painter.viewport()
    if TYPE_CHECKING:
      assert isinstance(self.textPen, QPen)
      assert isinstance(self.textFont, QFont)
      assert isinstance(self.textBackgroundBrush, QBrush)
    painter.setFont(self.textFont)
    textRect = self._align(viewRect)
    painter.setBrush(self.textBackgroundBrush)
    painter.drawRect(viewRect)
    brush = QBrush()
    brush.setColor(self.textBackgroundBrush.color().darker(125))
    brush.setStyle(SolidFill)
    painter.setBrush(brush)
    painter.drawRect(textRect)
    painter.setPen(self.textPen)
    painter.drawText(textRect, AlignCenter, self.text)


class Label(EZDesc):
  """Label provides the descriptor protocol for the LabelWidget class."""

  def getContentClass(self) -> type:
    """Returns the content class."""
    return LabelWidget

  def create(self, instance: object, owner: type, **kwargs) -> LabelWidget:
    """Create the content."""
    return LabelWidget(*self.getArgs(), **self.getKwargs())
