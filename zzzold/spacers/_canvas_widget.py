"""CanvasWidget provides a canvas widget. It supports the box model with
an outer margin, a border and padding. Subclasses should allow the parent
class to paint the background and border before painting the custom
content. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPaintEvent, QColor, QFocusEvent
from icecream import ic

from ezside.widgets import CoreWidget
from ezside.core import parseBrush, SolidFill, emptyPen

ic.configureOutput(includeContext=True)


class CanvasWidget(CoreWidget):
  """CanvasWidget provides a canvas widget. It supports the box model with
  an outer margin, a border and padding. Subclasses should allow the parent
  class to paint the background and border before painting the custom
  content."""

  def paintEvent(self, event: QPaintEvent, ) -> None:
    """The paintEvent method paints the widget."""
    margins = self.getSetting('margins')
    borders = self.getSetting('borders')
    paddings = self.getSetting('paddings')
    radius = self.getSetting('radius')
    backgroundBrush = self.getSetting('backgroundBrush')
    borderBrush = self.getSetting('borderBrush')
    painter = GraffitiVandal()
    painter.begin(self)
    viewRect = painter.viewport()
    pen = emptyPen()
    painter.setPen(pen)
    if radius is None:
      rx, ry = 0, 0
    else:
      rx, ry = radius.x(), radius.y()
    borderedRect = viewRect - margins
    paddedRect = borderedRect - borders
    innerRect = paddedRect - paddings
    borderedRect.moveCenter(viewRect.center())
    paddedRect.moveCenter(viewRect.center())
    innerRect.moveCenter(viewRect.center())
    if self.__has_focus__:
      focusBrush = parseBrush(QColor(255, 0, 0, 63), SolidFill)
      painter.setBrush(focusBrush)
      painter.drawRoundedRect(painter.viewport(), 0, 0, )
    painter.setBrush(borderBrush)
    painter.drawRoundedRect(borderedRect, rx, ry)
    painter.setBrush(backgroundBrush)
    painter.drawRoundedRect(paddedRect, rx, ry)
    painter.setInnerViewport(innerRect)
    self.customPaint(painter)
    painter.end()

  def initUi(self, ) -> None:
    """Initialize the user interface."""

  def initSignalSlot(self) -> None:
    """Initialize the signal slot."""

  def customPaint(self, painter: GraffitiVandal) -> None:
    """Subclasses must reimplement this method to define the painting
    action. The painter is already set up and will be ended by the parent
    class. """

  def focusInEvent(self, event: QFocusEvent) -> None:
    """Handle the widget's focus-in event. """
    self.__has_focus__ = True
    if event.reason() == 777:
      pass
    self.update()

  def focusOutEvent(self, event: QFocusEvent) -> None:
    """Handle the widget's focus-out event. """
    self.__has_focus__ = False
    self.update()
