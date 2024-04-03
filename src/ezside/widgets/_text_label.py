"""The TextLabel class provides a text labels"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt, QRect, QRectF
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QPaintEvent
from PySide6.QtGui import QFontMetrics
from vistutils.waitaminute import typeMsg

from ezside import Settings
from ezside.core import SolidFill, SolidLine
from ezside.core import emptyPen, emptyBrush, AlignLeft, Tight
from ezside.core import AlignVCenter
from ezside.moreutils import EmptyField
from ezside.widgets import BaseWidget


class TextLabel(BaseWidget):
  """The TextLabel class provides a text labels"""

  __fallback_alignment__ = AlignLeft | AlignVCenter
  __alignment_flags__ = None
  __fallback_text__ = 'LMAO'
  __inner_text__ = None

  text = EmptyField()

  @text.GET
  def getText(self) -> str:
    """Get the text."""
    return self.__inner_text__

  @text.SET
  def setText(self, text: str) -> None:
    """Set the text."""
    self.__inner_text__ = text
    rect = self.getTextRect()
    self.setMinimumSize(rect.size())
    self.update()

  @text.DEL
  def delText(self) -> None:
    """Delete the text."""
    self.__inner_text__ = None

  @staticmethod
  def getTextPen() -> QPen:
    """Returns the pen of the label."""
    pen = QPen()
    pen.setColor(Settings.getLabelTextColor())
    return pen

  @staticmethod
  def getBorderPen() -> QPen:
    """Returns the border pen of the label."""
    pen = QPen()
    pen.setColor(Settings.getLabelBorderColor())
    pen.setWidth(Settings.labelBorderWidth)
    pen.setStyle(SolidLine)
    return pen

  @staticmethod
  def getBackgroundBrush() -> QBrush:
    """Returns the background brush of the label."""
    brush = QBrush()
    brush.setStyle(SolidFill)
    brush.setColor(Settings.getLabelBackgroundColor())
    return brush

  @staticmethod
  def getTextFont() -> QFont:
    """Returns the font of the label."""
    font = QFont()
    font.setFamily(Settings.fontFamily)
    font.setPointSize(Settings.labelFontSize)
    return font

  @classmethod
  def getFontMetrics(cls) -> QFontMetrics:
    """Returns the font metrics of the label."""
    return QFontMetrics(cls.getTextFont())

  def getTextRect(self) -> QRect:
    """Returns the bounding rect of the label."""
    margins = Settings.getLabelMargins()
    n = max([len(self.text), 8])
    sampleText = self.text.center(n + 2, '|')
    if isinstance(sampleText, str):
      return self.getFontMetrics().boundingRect(sampleText) + margins
    e = typeMsg('self.text', self.text, str)
    raise TypeError(e)

  def update(self) -> None:
    """Update the label."""
    self.setMinimumSize(self.getTextRect().size())
    self.adjustSize()
    BaseWidget.update(self)

  def __init__(self, text: str = None) -> None:
    """Initialize the widget."""
    BaseWidget.__init__(self)
    if text is not None:
      if isinstance(text, str):
        self.text = text
      else:
        e = typeMsg('text', text, str)
        raise TypeError(e)
    else:
      self.text = self.__fallback_text__

  def initUi(self) -> None:
    """Initialize the user interface."""
    BaseWidget.initUi(self)
    self.setMinimumSize(self.getTextRect().size())
    self.setSizePolicy(Tight, Tight)

  def getAlignment(self) -> Qt.AlignmentFlag:
    """Returns the alignment of the label."""
    return self.__alignment_flags__ or self.__fallback_alignment__

  def setAlignment(self, alignment: Qt.AlignmentFlag) -> None:
    """Set the alignment of the label."""
    self.__alignment_flags__ = alignment

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paint the label."""
    painter = QPainter()
    painter.begin(self)
    painter.setRenderHint(QPainter.Antialiasing)
    textRect = self.getTextRect()
    viewRect = painter.viewport()
    textRect.moveCenter(viewRect.center())
    painter.setBrush(self.getBackgroundBrush())
    painter.setPen(emptyPen())
    painter.drawRect(viewRect)
    painter.setPen(self.getBorderPen())
    painter.setBrush(emptyBrush())
    painter.drawRect(viewRect)
    painter.setPen(self.getTextPen())
    painter.setBrush(emptyBrush())
    if not isinstance(textRect, (QRect, QRectF)):
      e = typeMsg('textRect', textRect, QRect)
      raise TypeError(e)
    if not isinstance(self.text, str):
      e = typeMsg('self.text', self.text, str)
      raise TypeError(e)
    painter.setFont(self.getTextFont())
    painter.drawText(textRect, self.getAlignment(), self.text)
    # painter.drawText(textRect, Qt.AlignCenter, self.text)
    painter.end()
    self.setMinimumSize(viewRect.size())
    self.adjustSize()