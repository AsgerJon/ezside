"""Noisinator creates a noise signal."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time
from math import sin

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton
from icecream import ic

from attribox import AttriBox
from ezqt.core import Precise
from ezqt.widgets import BaseWidget, VerticalSlider, Timer, TextLabel


class Noisinator(BaseWidget):
  """Noisinator creates a noise signal."""

  baseLayout = AttriBox[QVBoxLayout]()
  timer = AttriBox[Timer](10, Precise, False)
  sliderWidget = AttriBox[BaseWidget]()
  sliderLayout = AttriBox[QHBoxLayout]()
  f1 = AttriBox[VerticalSlider](0, 100, 1, 10, 50)
  f2 = AttriBox[VerticalSlider](0, 100, 1, 10, 50)
  f4 = AttriBox[VerticalSlider](0, 100, 1, 10, 50)
  f8 = AttriBox[VerticalSlider](0, 100, 1, 10, 50)
  f16 = AttriBox[VerticalSlider](0, 100, 1, 10, 50)
  f32 = AttriBox[VerticalSlider](0, 100, 1, 10, 50)
  startButton = AttriBox[QPushButton]("""Start""")
  stopButton = AttriBox[QPushButton]("""Stop""")
  titleBanner = AttriBox[TextLabel]("""Let's make some noise!""")
  controlWidget = AttriBox[BaseWidget]()
  controlLayout = AttriBox[QVBoxLayout]()

  noise = Signal(float)

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.sliderLayout.addWidget(self.f1)
    self.sliderLayout.addWidget(self.f2)
    self.sliderLayout.addWidget(self.f4)
    self.sliderLayout.addWidget(self.f8)
    self.sliderLayout.addWidget(self.f16)
    self.sliderLayout.addWidget(self.f32)
    self.controlLayout.addWidget(self.startButton)
    self.controlLayout.addWidget(self.stopButton)
    self.controlWidget.setLayout(self.controlLayout)
    self.sliderLayout.addWidget(self.controlWidget)
    self.sliderWidget.setLayout(self.sliderLayout)
    self.baseLayout.addWidget(self.sliderWidget)
    self.setLayout(self.baseLayout)

  @Slot()
  def emitNoise(self, ) -> None:
    """Emit the noise signal."""
    t = time.time()
    x1 = self.f1.value() / 100 * sin(t)
    x2 = self.f2.value() / 100 * sin(2 * t)
    x4 = self.f4.value() / 100 * sin(4 * t)
    x8 = self.f8.value() / 100 * sin(8 * t)
    x16 = self.f16.value() / 100 * sin(16 * t)
    x32 = self.f32.value() / 100 * sin(32 * t)
    x = x1 + x2 + x4 + x8 + x16 + x32
    self.noise.emit(x)
