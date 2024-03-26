"""The TextLabel class provides a text labels"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRect, QPoint
from PySide6.QtGui import QPainter, QPaintEvent, QFontMetrics
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from ezside.core import Center
from ezside.widgets import BaseWidget
from ezside.moreutils import StrField


class TextLabel(BaseWidget):
  """The TextLabel class provides a text labels"""

  __inner_text__ = None
  innerText = StrField('TextLabel')
  horizontalAlignment = StrField()
  verticalAlignment = StrField()

  def __init__(self, *args, **kwargs) -> None:
    BaseWidget.__init__(self, *args, **kwargs)
    textKeys = stringList("""msg, text, label, innerText""")
    for key in textKeys:
      if key in kwargs:
        val = kwargs.get(key)
        if isinstance(val, str):
          self.__inner_text__ = val
          break
        else:
          e = typeMsg(key, val, str)
          raise TypeError(e)
    else:
      for arg in args:
        if isinstance(arg, str):
          self.__inner_text__ = arg
          break
      else:
        self.__inner_text__ = 'TextLabel'

  def getMetrics(self) -> QFontMetrics:
    """Returns the font metrics of the label."""
    return QFontMetrics(self.defaultFont)

  def getRect(self) -> QRect:
    """Returns the bounding rect of the label."""
    text = self.innerText
    return self.getMetrics().boundingRect(text)

  def setText(self, text: str) -> None:
    """Sets the text of the label."""
    self.innerText = text

  def getText(self, ) -> str:
    """Returns the text of the label."""
    return self.innerText

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the widget."""
    BaseWidget.initUi(self)
    self.defaultFont.setPointSize(12)
    rect = QFontMetrics(self.defaultFont).boundingRect(self.getText())
    self.setMinimumSize(rect.size())

  def alignRect(self, targetRect: QRect) -> QRect:
    """The rectangle returned by this method is the bounding rectangle
    required for the text placed in relation to the target rectangle."""
    hAlign = self.horizontalAlignment or 'center'
    vAlign = self.verticalAlignment or 'center'
    size = self.getMetrics().boundingRect(self.innerText).size()
    if hAlign == 'center':
      left = (targetRect.width() - size.width()) / 2
    elif hAlign == 'right':
      left = targetRect.width() - size.width()
    elif hAlign == 'left':
      left = 0
    else:
      e = """Invalid horizontal alignment: '%s'""" % (hAlign,)
      raise ValueError(e)
    if vAlign == 'center':
      top = (targetRect.height() - size.height()) / 2
    elif vAlign == 'top':
      top = 0
    elif vAlign == 'bottom':
      top = targetRect.height() - size.height()
    else:
      e = """Invalid vertical alignment: '%s'""" % (vAlign,)
      raise ValueError(e)
    left += targetRect.left()
    top += targetRect.top()
    leftTop = QPoint(left, top)
    return QRect(leftTop, size)

  def paintEvent(self, event: QPaintEvent) -> None:
    """The paintEvent method is called when the widget needs to be
    repainted."""
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    textSize = self.getRect().size()
    # # # # # # # # # # # # # # # # #
    # Painting the fill
    painter.setPen(self.emptyLine)
    painter.setBrush(self.solidBrush)
    painter.drawRect(viewRect)
    # # # # # # # # # # # # # # # # #
    # Painting the border
    painter.setPen(self.solidLine)
    painter.setBrush(self.emptyBrush)
    painter.drawRect(viewRect)
    # # # # # # # # # # # # # # # # #
    # Painting the text

    painter.setPen(self.fontLine)
    painter.setFont(self.defaultFont)
    flags = Center
    text = self.getText()
    painter.drawText(viewRect, flags, text)
    painter.end()
