"""DigitalClock provides a widget displaying the current time using seven
segment displays."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt, QRectF, QPointF, QSizeF, QRect
from PySide6.QtGui import QColor, QBrush, QPainter, QShowEvent
from PySide6.QtWidgets import QSizePolicy
from icecream import ic
from worktoy.desc import AttriBox, Field

from ezside.layouts import AbstractLayout
from ezside.basewidgets import BoxWidget, SevenSeg

ic.configureOutput(includeContext=True)


class Spacer(BoxWidget):
  """Spacer provides a widget that can be used to add space between
  basewidgets."""

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

  @brush.GET
  def _getBrush(self) -> QBrush:
    """Getter-function for the brush"""
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    brush.setColor(self.color)
    return brush

  def requiredSize(self) -> QSizeF:
    """This method returns the required size of the widget."""
    return self.requiredRect().size()

  def requiredRect(self) -> QRectF:
    """This method returns the required rectangle of the widget."""
    return QRectF(QPointF(0, 0), QSizeF(16, 32))

  def paintMeLike(self, rect: QRectF, painter: QPainter) -> None:
    """Paints the colon with the current color."""
    viewRect = rect
    center = viewRect.center()
    marginRect = QRectF.marginsRemoved(viewRect, self.margins)
    borderRect = QRectF.marginsRemoved(marginRect, self.borders)
    paddedRect = QRectF.marginsRemoved(borderRect, self.paddings)
    marginRect.moveCenter(center)
    borderRect.moveCenter(center)
    paddedRect.moveCenter(center)
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    brush.setColor(QColor(255, 0, 0, 255))
    painter.setBrush(brush)
    viewRect = QRect.toRectF(painter.viewport())
    h = viewRect.height()
    d = h / 4
    y1 = d * 1.25
    y2 = h - d * 1.25
    x = rect.center().x()
    topCenter = QPointF(x, y1)
    bottomCenter = QPointF(x, y2)
    r = d / 4
    painter.drawEllipse(topCenter, r, r)
    painter.drawEllipse(bottomCenter, r, r)


class DigitalClock(AbstractLayout):
  """DigitalClock provides a widget displaying the current time using seven
  segment displays."""

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

  def __init__(self, *args) -> None:
    """The constructor method for the DigitalClock widget."""
    AbstractLayout.__init__(self, *args)
    self.backgroundColor = QColor(0, 0, 0, 255)
    self.tenHour = SevenSeg()
    self.oneHour = SevenSeg()
    self.colon1 = Colon()
    self.tenMin = SevenSeg()
    self.oneMin = SevenSeg()
    self.colon2 = Colon()
    self.tenSec = SevenSeg()
    self.oneSec = SevenSeg()
    self.addWidget(self.tenHour, 0, 0)
    self.addWidget(self.oneHour, 0, 1)
    self.addWidget(self.colon1, 0, 2)
    self.addWidget(self.tenMin, 0, 3)
    self.addWidget(self.oneMin, 0, 4)
    self.addWidget(self.colon2, 0, 5)
    self.addWidget(self.tenSec, 0, 6)
    self.addWidget(self.oneSec, 0, 7)
    self.refreshTime()

  def _getWidgets(self) -> list[BoxWidget]:
    """This method returns the basewidgets in the layout."""
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

  def showEvent(self, event: QShowEvent) -> None:
    """This method is responsible for showing the widget."""
    self.refreshTime(_recursion=True)
    BoxWidget.showEvent(self, event)
