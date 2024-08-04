"""DigitalClock provides a widget displaying the current time using seven
segment displays."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt, QMargins, QSize, QRect, QPoint, QSizeF, \
  QRectF, QMarginsF
from PySide6.QtGui import QColor, QBrush, QPaintEvent, QPainter, \
  QResizeEvent, QShowEvent
from PySide6.QtWidgets import QHBoxLayout, QSizePolicy
from icecream import ic
from worktoy.desc import AttriBox, Field

from ezside.tools import emptyPen, Align
from ezside.widgets import BoxWidget, SevenSeg

ic.configureOutput(includeContext=True)


class Spacer(BoxWidget):
  """Spacer provides a widget that can be used to add space between
  widgets."""

  def __init__(self, parent=None) -> None:
    """The constructor method for the Spacer widget."""
    BoxWidget.__init__(self, parent)
    self.setSizePolicy(QSizePolicy.Policy.Expanding,
                       QSizePolicy.Policy.Expanding)


class Colon(BoxWidget):
  """Colon provides a widget displaying a colon using two seven segment
  displays."""

  color = AttriBox[QColor](QColor(255, 0, 0, 255))

  brush = Field()

  def minimumSizeHint(self) -> QSize:
    """This method returns the size hint of the widget."""
    return QSize(48, 16)

  @brush.GET
  def _getBrush(self) -> QBrush:
    """Getter-function for the brush"""
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    brush.setColor(self.color)
    return brush

  def paintEvent(self, event: QPaintEvent) -> None:
    """This method is responsible for painting the widget."""
    BoxWidget.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self)
    painter.setBrush(self.brush)
    painter.setPen(emptyPen())
    diameter = self.contentRect.height() / 5
    x = painter.viewport().width() / 2 - diameter / 2
    y1 = 1 * diameter + self.contentRect.top()
    y2 = 3 * diameter + self.contentRect.top()
    painter.drawEllipse(x, y1, diameter, diameter)
    painter.drawEllipse(x, y2, diameter, diameter)
    painter.end()


class DigitalClock(BoxWidget):
  """DigitalClock provides a widget displaying the current time using seven
  segment displays."""

  __fallback_height__ = 48

  layout = AttriBox[QHBoxLayout]()
  oneSec = AttriBox[SevenSeg]()
  tenSec = AttriBox[SevenSeg]()
  colon1 = AttriBox[Colon]()
  oneMin = AttriBox[SevenSeg]()
  tenMin = AttriBox[SevenSeg]()
  colon2 = AttriBox[Colon]()
  oneHour = AttriBox[SevenSeg]()
  tenHour = AttriBox[SevenSeg]()
  spacer = AttriBox[Spacer]()

  hour = Field()
  minute = Field()
  second = Field()

  @hour.GET
  def _getHour(self) -> int:
    """This method returns the current hour."""
    return datetime.now().hour

  @minute.GET
  def _getMinute(self) -> int:
    """This method returns the current minute."""
    return datetime.now().minute

  @second.GET
  def _getSecond(self) -> int:
    """This method returns the current second."""
    return datetime.now().second

  def __init__(self, parent=None, *args) -> None:
    """The constructor method for the DigitalClock widget."""
    BoxWidget.__init__(self, parent)
    self.backgroundColor = QColor(0, 0, 0, 255)
    self.borderColor = QColor(255, 0, 169, 255)
    self.marginColor = QColor(31, 0, 0, 255)
    self.margins = QMarginsF(2, 1, 2, 1, ) * 3
    ic(self.margins)
    self.aspectRatio = 0.2
    QHBoxLayout.setContentsMargins(self.layout, self.margins.toMargins())
    QHBoxLayout.setSpacing(self.layout, 0)
    QHBoxLayout.setAlignment(self.layout, Align.RIGHT.qt)
    for widget in self._getWidgets():
      if type(widget) is SevenSeg:
        setattr(widget, 'aspectRatio', 1.5)
      elif type(widget) is Colon:
        setattr(widget, 'aspectRatio', 2.)
      # setattr(widget, 'paddings', QMarginsF(1, 1, 1, 1, ))
      setattr(widget, 'lowColor', QColor(95, 0, 0, 255))
      setattr(widget, 'highColor', QColor(255, 0, 0, 255))
      setattr(widget, 'backgroundColor', QColor(0, 0, 0, 255))
      self.layout.addWidget(widget)
    self.setLayout(self.layout)
    self.refreshTime()

  def minimumSizeHint(self) -> QSize:
    """This method returns the size hint of the widget."""
    return QSize(160, 32)

  def _getWidgets(self) -> list[BoxWidget]:
    """This method returns the widgets in the layout."""
    return [
        self.tenHour,
        self.oneHour,
        self.colon1,
        self.tenMin,
        self.oneMin,
        self.colon2,
        self.tenSec,
        self.oneSec,
    ]

  def refreshTime(self, **kwargs) -> None:
    """This method is responsible for refreshing the time."""
    self.oneSec.digit = self.second % 10
    self.tenSec.digit = self.second // 10
    self.oneMin.digit = self.minute % 10
    self.tenMin.digit = self.minute // 10
    self.oneHour.digit = self.hour % 10
    self.tenHour.digit = self.hour // 10
    if not kwargs.get('_recursion', False):
      self.update()

  def resizeEvent(self, event: QResizeEvent) -> None:
    """This method is responsible for resizing the widget."""
    size = QResizeEvent.size(event)
    rect = self._enforceAspect(QRect(QPoint(0, 0), size))
    e = QResizeEvent(QSizeF.toSize(rect.size()), event.oldSize())
    self.resize(e.size())
    BoxWidget.resizeEvent(self, e)

  def showEvent(self, event: QShowEvent) -> None:
    """This method is responsible for showing the widget."""
    self.refreshTime(_recursion=True)
    BoxWidget.showEvent(self, event)

  def resize(self, newSize: QSize) -> None:
    """This method is responsible for resizing the widget."""
    rect = QRectF.toRect(self._enforceAspect(QRect(QPoint(0, 0), newSize)))
    BoxWidget.resize(self, rect.size())
