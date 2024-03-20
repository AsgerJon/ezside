"""Noisinator creates a noise signal."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtGui import QPaintEvent, QPainter
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from attribox import AttriBox
from icecream import ic

from moreutils import IntField
from ezqt.core import Precise, LawnGreen
from ezqt.widgets import TextLabel, Equalizer, BaseWidget, \
  VerticalAbstractControl
from ezqt.widgets import Timer
from settings import Default


class WhiteNoise(BaseWidget):
  """Noisinator creates a noise signal."""

  noise = Signal(float)
  start = Signal()
  stop = Signal()
  pause = Signal()

  resumeTimer = IntField()

  timer = AttriBox[Timer](Default.noiseTimer, Precise, False)
  baseLayout = AttriBox[QVBoxLayout]()
  horizontalWidget = AttriBox[BaseWidget]()
  horizontalLayout = AttriBox[QHBoxLayout]()
  equalizer = AttriBox[Equalizer](6, )
  control = AttriBox[VerticalAbstractControl]()
  titleBanner = AttriBox[TextLabel]("""Let's make some noise!""")

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(400, 400)
    self.equalizer.initUi()
    self.horizontalLayout.addWidget(self.equalizer)
    self.control.initUi()
    self.horizontalLayout.addWidget(self.control)
    self.horizontalWidget.setLayout(self.horizontalLayout)
    self.baseLayout.addWidget(self.horizontalWidget)
    self.setLayout(self.baseLayout)
    self.connectActions()

  def connectActions(self) -> None:
    """The connectActions method connects the actions."""
    self.control.start.connect(self.start)
    self.control.stop.connect(self.stop)
    self.control.pause.connect(self.pause)
    self.start.connect(self.startHandle)
    self.stop.connect(self.stopHandle)
    self.pause.connect(self.pauseHandle)
    self.timer.timeout.connect(self.emitNoise)

  def startHandle(self) -> None:
    """Handles the start signal"""
    ic()
    if self.resumeTimer:
      timer = Timer(self.resumeTimer, Precise, True)
      timer.timeout.connect(self.timer.start)
      return timer.start()
    self.timer.start()

  def stopHandle(self) -> None:
    """Handles the stop signal"""
    self.resumeTimer = 0
    self.timer.stop()

  def pauseHandle(self) -> None:
    """Handles the pause signal"""
    self.resumeTimer = self.timer.remainingTime()
    self.timer.stop()

  def emitNoise(self, ) -> None:
    """Emit the noise signal."""
    self.noise.emit(float(self))

  def __float__(self) -> float:
    """The float method returns the float representation of the object."""
    if isinstance(self.equalizer, Equalizer):
      return abs(self.equalizer).real
    return NotImplemented

  def paintEvent(self, event: QPaintEvent) -> None:
    """The paintEvent method paints the widget."""
    painter = QPainter()
    painter.begin(self)
    rect = painter.viewport()
    painter.setRenderHint(QPainter.Antialiasing)
    self.solidBrush.setColor(LawnGreen)
    painter.setBrush(self.solidBrush)
    painter.setPen(self.emptyLine)
    painter.drawRoundedRect(rect, 2, 2)
    painter.end()
