"""Spacer widget takes up space"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPaintEvent, QPainter, QPen

from ezqt.core import Expand, Tight, DashLine, SkyBlue
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
    """The paintEvent method paints the widget."""
    # painter = QPainter()
    # painter.begin(self)
    # painter.setBrush(self.emptyBrush())
    # debugPen = QPen()
    # # painter.setPen(DashLine, )  # For debug, the dash line
    # painter.end()


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
