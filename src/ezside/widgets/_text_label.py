"""TextLabel provides a property driven alternative to QLabel. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize
from PySide6.QtGui import (QFont, QFontMetrics, QPaintEvent, QPainter)
from PySide6.QtWidgets import QWidget
from worktoy.desc import AttriBox, EmptyField

from ezside.tools import textPen
from ezside.widgets import BoxWidget


class TextLabel(BoxWidget):
  """TextLabel provides a property driven alternative to QLabel. """

  text = AttriBox[str]('LMAO')
  fontFamily = AttriBox[str]('Courier')
  fontSize = AttriBox[int](12)

  font = EmptyField()

  @font.GET
  def _getFont(self) -> QFont:
    """This method returns the font used by the text label. """
    out = QFont()
    out.setFamily(self.fontFamily)
    out.setPointSize(self.fontSize)
    return out

  def _textBoundingSize(self, ) -> QSize:
    """This method returns the bounding size of the text with the given
    font. """
    if isinstance(self.font, QFont):
      return QFontMetrics(self.font).boundingRect(self.text).size()

  @text.ONSET
  def _handleNewText(self, *args) -> None:
    """This method is triggered when the text at the text field is
    changed. """
    requiredSize = self._textBoundingSize()
    self.setFixedSize(requiredSize)
    self.update()

  def __init__(self, *args, **kwargs) -> None:
    parent, text = None, None
    for arg in args:
      if isinstance(arg, QWidget) and parent is None:
        parent = arg
      if isinstance(arg, str) and text is None:
        text = arg
      if parent is not None and text is not None:
        break
    else:
      if parent is None:
        BoxWidget.__init__(self, )
      else:
        BoxWidget.__init__(self, parent)
    self._handleNewText()

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation of the paint event"""
    BoxWidget.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self)
    painter.setFont(self.font)
    painter.setPen(textPen(self.textColor))

    viewRect = painter.viewport()
    marginedRect = viewRect.marginsRemoved(self._getMargin())
    borderedRect = marginedRect.marginsRemoved(self._getBorder())
    paddedRect = borderedRect.marginsRemoved(self._getPadding())

    painter.drawText(paddedRect, self.text)
    painter.end()
