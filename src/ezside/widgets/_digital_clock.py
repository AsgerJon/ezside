"""DigitalClock provides a widget displaying the current time using seven
segment displays."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from datetime import datetime
from typing import TypeAlias, Union, TYPE_CHECKING, Any

from PySide6.QtCore import Qt, QPointF, QSizeF
from PySide6.QtGui import QColor, QBrush, QPointerEvent
from icecream import ic
from worktoy.desc import AttriBox
from PySide6.QtCore import QRect, QRectF
from PySide6.QtGui import QPainter, QPaintEvent
from worktoy.desc import Field

from ezside.layouts import HorizontalLayout
from ezside.base_widgets import BoxWidget, SevenSeg

if TYPE_CHECKING:
  pass

Rect: TypeAlias = Union[QRect, QRectF]

ic.configureOutput(includeContext=True)


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
    brush.setColor(QColor(255, 0, 0, 255))
    return brush

  def __init__(self, *args) -> None:
    """The constructor method for the Colon widget."""
    BoxWidget.__init__(self, *args)
    self.paddingColor = QColor(63, 0, 0, 255)

  def requiredSize(self) -> QSizeF:
    """This method returns the required size of the widget."""
    return QSizeF(18, 36)

  def paintMeLike(self,
                  rect: Rect,
                  painter: QPainter,
                  event: QPaintEvent) -> Any:
    """Paints the colon with the current color."""
    rect, painter, event = BoxWidget.paintMeLike(self, rect, painter, event)
    c = rect.center()
    top = rect.top()
    rect -= self.allMargins
    rect.moveCenter(c)
    x = rect.center().x()
    y1 = rect.height() * 0.2 + top
    y2 = y1 + rect.height() * 0.6
    r = rect.height() * 0.1
    painter.setBrush(self.brush)
    painter.drawEllipse(QPointF(x, y1), r, r)
    painter.drawEllipse(QPointF(x, y2), r, r)
    return rect, painter, event

  def handlePointerEvent(self, pointerEvent: QPointerEvent) -> bool:
    """This method is responsible for handling pointer events."""
    return False


class DigitalClock(HorizontalLayout):
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
    HorizontalLayout.__init__(self, *args, styleId='digital_clock')
    self.spacing = 5
    self.tenHour = SevenSeg()
    self.oneHour = SevenSeg()
    self.colon1 = Colon()
    self.tenMin = SevenSeg()
    self.oneMin = SevenSeg()
    self.colon2 = Colon()
    self.tenSec = SevenSeg()
    self.oneSec = SevenSeg()
    self.addWidget(self.tenHour)
    self.addWidget(self.oneHour)
    self.addWidget(self.colon1)
    self.addWidget(self.tenMin)
    self.addWidget(self.oneMin)
    self.addWidget(self.colon2)
    self.addWidget(self.tenSec)
    self.addWidget(self.oneSec)
    self.refreshTime()

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

  def handlePointerEvent(self, pointerEvent: QPointerEvent) -> None:
    """This method is responsible for handling pointer events."""
    pass
