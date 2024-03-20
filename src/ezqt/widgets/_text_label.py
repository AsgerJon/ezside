"""The TextLabel class provides a text labels"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPainter, QPaintEvent, QFontMetrics
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from ezqt.core import Center
from ezqt.widgets import BaseWidget


class TextLabel(BaseWidget):
  """The TextLabel class provides a text labels"""

  __inner_text__ = None

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

  def setText(self, text: str) -> None:
    """Sets the text of the label."""
    self.__inner_text__ = text

  def getText(self, ) -> str:
    """Returns the text of the label."""
    return self.__inner_text__

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the widget."""
    BaseWidget.initUi(self)
    self.defaultFont.setPointSize(12)
    rect = QFontMetrics(self.defaultFont).boundingRect(self.getText())
    self.setMinimumSize(rect.size())

  def paintEvent(self, event: QPaintEvent) -> None:
    """The paintEvent method is called when the widget needs to be
    repainted."""
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
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
