"""Spacer widget takes up space"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QMargins
from PySide6.QtGui import QPaintEvent, QPainter, QPen, QColor, QBrush

from ezqt.core import Expand, Tight, White, DashLine
from ezqt.widgets import BaseWidget


class AbstractSpacer(BaseWidget):
  """Spacer widget takes up space"""

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the widget."""
    self.initUi()
    self.connectActions()

  def connectActions(self) -> None:
    """The connectActions method connects the widget actions."""
    pass

  def paintEvent(self, event: QPaintEvent) -> None:
    """The paintEvent method is called when the widget needs to be
    repainted."""
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    paintRect = viewRect - QMargins(6, 6, 6, 6)
    paintRect.moveCenter(viewRect.center())
    debugBrush = QBrush()
    debugBrush.setColor(QColor(255, 255, 255, 31))
    debugPen = QPen()
    debugPen.setColor(White)
    debugPen.setStyle(DashLine)
    painter.setBrush(debugBrush)
    painter.setPen(debugPen)
    painter.drawRoundedRect(painter.viewport(), 4, 4)
    painter.end()


class VSpacer(AbstractSpacer):
  """Spacer widget takes up space"""

  def __init__(self, *args, **kwargs) -> None:
    AbstractSpacer.__init__(self, *args, **kwargs)
    self.setSizePolicy(Tight, Expand)


class HSpacer(AbstractSpacer):
  """Spacer widget takes up space"""

  def __init__(self, *args, **kwargs) -> None:
    AbstractSpacer.__init__(self, *args, **kwargs)
    self.setSizePolicy(Expand, Tight)


class Spacer(AbstractSpacer):
  """Spacer widget takes up space"""

  def __init__(self, *args, **kwargs) -> None:
    AbstractSpacer.__init__(self, *args, **kwargs)
    self.setSizePolicy(Expand, Expand)
