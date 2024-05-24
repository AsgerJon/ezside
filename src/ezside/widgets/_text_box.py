"""TextBox provides a descriptor protocol for a widget text box. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QRect, QSize, QSizeF, QPointF, QRectF, QPoint
from PySide6.QtGui import QFontMetrics, QShowEvent, QResizeEvent
from attribox import AttriBox
from icecream import ic
from vistutils.waitaminute import typeMsg

from ezside.app import EZDesc, EZObject
from ezside.desc import Pen, \
  SolidLine, \
  HAlign, \
  VAlign, \
  AlignLeft, \
  AlignTop, \
  fitText, Expand
from ezside.desc import Font, Black, AlignBottom, AlignCenter
from ezside.desc import AlignRight, AlignHCenter, AlignVCenter

from ezside.widgets import CanvasWidget, GraffitiVandal

Rect = QRect | QRectF | QSizeF | QSize
Rects = tuple[Rect, Rect]

ic.configureOutput(includeContext=True)


class TextBoxWidget(CanvasWidget):
  """TextBox provides a descriptor protocol for a widget text box. """

  text = AttriBox[str]('')
  pen = Pen(Black, 1, SolidLine)
  font = Font('Montserrat', 12, 'Normal')
  hAlign = HAlign(AlignLeft)
  vAlign = VAlign(AlignTop)
  lineChars = AttriBox[int](77)

  def alignRect(self, staticRect: Rect, movingRect: Rect, ) -> QRectF:
    """Calculates the aligned rectangle for text"""
    if isinstance(movingRect, QSizeF):
      newSize = movingRect
    elif isinstance(movingRect, QSize):
      newSize = movingRect.toSizeF()
    elif isinstance(movingRect, QRect):
      newSize = movingRect.size().toSizeF()
    elif isinstance(movingRect, QRectF):
      newSize = movingRect.size()
    else:
      e = typeMsg('movingRect', movingRect, QRect)
      raise TypeError(e)
    newLeft, newTop = None, None
    if self.hAlign == AlignLeft:
      newLeft = staticRect.left()
    elif self.hAlign in [AlignHCenter, AlignCenter]:
      newCenterX = staticRect.center().x()
      newLeft = newCenterX - newSize.width() / 2
    elif self.hAlign == AlignRight:
      newLeft = staticRect.right() - newSize.width()
    if self.vAlign == AlignTop:
      newTop = staticRect.top()
    elif self.vAlign in [AlignVCenter, AlignCenter]:
      newCenterY = staticRect.center().y()
      newTop = newCenterY - newSize.height() / 2
    elif self.vAlign == AlignBottom:
      newTop = staticRect.bottom() - newSize.height()
    newTopLeft = QPointF(newLeft, newTop)
    return QRectF(newTopLeft, newSize)

  def getFittedText(self) -> list[tuple[str, QSize]]:
    """Getter-function for fitted text"""
    lines = fitText(self.text, self.lineChars)
    sizes = []
    metrics = QFontMetrics(self.font)
    out = []
    for line in lines:
      textLine = ' '.join(line)
      size = metrics.boundingRect(textLine).size()
      out.append((textLine, size))
    return out

  def getWordLines(self) -> list[list[tuple[str, QSize]]]:
    """Getter-function for fitted words. """
    lines = fitText(self.text, self.lineChars)
    metrics = QFontMetrics(self.font)
    newLines = []
    newLine: list[tuple[str, QSize]] = []
    left, top = 0, 0
    prevLeft, prevTop = 0, 0
    for line in lines:
      for word in line:
        newLine.append((word, metrics.boundingRect(word).size()))
    return newLines

  def getFittedLines(self) -> list[str]:
    """Getter-function for the text lines"""
    return [line for (line, size) in self.getFittedText()]

  def getFittedSizes(self, ) -> list[QSize]:
    """Getter-function for the sizes"""
    return [size for (line, size) in self.getFittedText()]

  def getTotalTextSize(self) -> QSize:
    """Getter-function for the size required to show the total text."""
    width = max([s.width() for s in self.getFittedSizes()])
    height = sum([s.height() for s in self.getFittedSizes()])
    return QSize(width, height)

  def initUi(self) -> None:
    """Initializes the user interface."""
    self.setSizePolicy(Expand, Expand)
    rect = QRect(QPoint(0, 0, ), self.getTotalTextSize())
    rect += self.paddingGeometry
    rect += self.borderGeometry
    rect += self.marginGeometry
    self.setMinimumSize(rect.size())
    ic(self.getTotalTextSize())

  def update(self) -> None:
    """Updates the widget."""
    rect = QRect(QPoint(0, 0, ), self.getTotalTextSize())
    rect += self.paddingGeometry
    rect += self.borderGeometry
    rect += self.marginGeometry
    self.setMinimumSize(rect.size())
    self.parent().update()
    self.parent().adjustSize()
    self.app.main.update()
    CanvasWidget.update(self)

  def customPaint(self, painter: GraffitiVandal) -> None:
    """Paints the widget."""
    viewRect = painter.viewport()
    left, top = 0, 0,
    painter.setFont(self.font)
    painter.setPen(self.pen)
    for (line, size) in self.getFittedText():
      textRect = QRect(QPoint(left, top), size)
      painter.drawText(textRect, AlignCenter, line)
      top += size.height()

  def resizeEvent(self, event: QResizeEvent) -> None:
    """Handles the resize event."""
    super().resizeEvent(event)
    self.parent().adjustSize()
    self.app.main.adjustSize()
    self.app.main.centralWidget().adjustSize()
    self.app.main.centralWidget().adjustSize()


class TextBox(EZDesc):
  """TextBox provides a descriptor protocol for a widget text box. """

  def getContentClass(self) -> type:
    """Returns the content class."""
    return TextBoxWidget

  def create(self, instance: EZObject, owner: type, **kwargs) -> Any:
    """Create the content."""
    widget = TextBoxWidget()
    posArgs = []
    for arg in self.getArgs():
      if isinstance(arg, str):
        widget.text = arg
        break
    else:
      widget.text = 'lmao'
      posArgs = self.getArgs()
    posArgs = []
    for arg in self.getArgs():
      if isinstance(arg, str) and arg != widget.text:
        posArgs.append(arg)
      if isinstance(arg, int):
        ic(arg)
        widget.lineChars = arg
    return widget
