"""Equalizer provides a widget for an adjustable number of sliders. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal, QTimer, Slot
from PySide6.QtWidgets import QHBoxLayout
from attribox import AttriBox

from ezside.core import VERTICAL, Precise
from ezside.torchcuts import R
from ezside.widgets import CanvasWidget, DoubleSlider
from math import sin


class Equalizer(CanvasWidget):
  """Equalizer provides a widget for an adjustable number of sliders. """

  __inner_sample__ = None

  chn1 = AttriBox[DoubleSlider](VERTICAL, '32', 0, 1)
  chn2 = AttriBox[DoubleSlider](VERTICAL, '64', 0, 1)
  chn3 = AttriBox[DoubleSlider](VERTICAL, '128', 0, 1)
  chn4 = AttriBox[DoubleSlider](VERTICAL, '256', 0, 1)
  chn5 = AttriBox[DoubleSlider](VERTICAL, '512', 0, 1)
  chn6 = AttriBox[DoubleSlider](VERTICAL, '1k', 0, 1)
  chn7 = AttriBox[DoubleSlider](VERTICAL, '2k', 0, 1)
  chn8 = AttriBox[DoubleSlider](VERTICAL, '4k', 0, 1)
  layout = AttriBox[QHBoxLayout]()

  batchSize = AttriBox[int](64)
  __inner_index__ = None
  __inner_time__ = None

  valueChanged = Signal(float)
  emitValue = Signal(float)

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.valueTimer = QTimer()
    self.valueTimer.setInterval(10)
    self.valueTimer.setSingleShot(False)
    self.valueTimer.setTimerType(Precise)
    self.valueTimer.timeout.connect(self.emitValueFunc)

  @Slot()
  def emitValueFunc(self) -> None:
    """Emits the valueChanged signal. """
    if self.__inner_sample__ is None:
      self.filterNoise()
    if self.__inner_index__ is None:
      self.__inner_index__ = 0
    if self.__inner_time__ is None:
      self.__inner_time__ = 0
    t = self.__inner_time__
    self.__inner_time__ += self.__inner_sample__[self.__inner_index__]
    self.__inner_index__ += 1
    if self.__inner_index__ >= self.batchSize:
      self.__inner_index__ = 0
      self.filterNoise()
    value = sum([
      float(self.chn1.value()) * sin(t * 2 ** 1),
      float(self.chn2.value()) * sin(t * 2 ** 2),
      float(self.chn3.value()) * sin(t * 2 ** 3),
      float(self.chn4.value()) * sin(t * 2 ** 4),
      float(self.chn5.value()) * sin(t * 2 ** 5),
      float(self.chn6.value()) * sin(t * 2 ** 6),
      float(self.chn7.value()) * sin(t * 2 ** 7),
      float(self.chn8.value()) * sin(t * 2 ** 8),
    ])
    self.valueChanged.emit(value)
    self.emitValue.emit(value)

  def initUi(self) -> None:
    """Initializes the user interface for the widget. """
    self.layout.setSpacing(2)
    self.layout.setContentsMargins(4, 4, 4, 4)
    self.chn1.initUi()
    self.layout.addWidget(self.chn1)
    self.chn2.initUi()
    self.layout.addWidget(self.chn2)
    self.chn3.initUi()
    self.layout.addWidget(self.chn3)
    self.chn4.initUi()
    self.layout.addWidget(self.chn4)
    self.chn5.initUi()
    self.layout.addWidget(self.chn5)
    self.chn6.initUi()
    self.layout.addWidget(self.chn6)
    self.chn7.initUi()
    self.layout.addWidget(self.chn7)
    self.chn8.initUi()
    self.layout.addWidget(self.chn8)
    self.setLayout(self.layout)

  def initSignalSlot(self) -> None:
    """Initializes the signal-slot connections for the widget. """
    self.chn1.initSignalSlot()
    self.chn1.valueChanged.connect(self.valueChanged)
    self.chn2.initSignalSlot()
    self.chn2.valueChanged.connect(self.valueChanged)
    self.chn3.initSignalSlot()
    self.chn3.valueChanged.connect(self.valueChanged)
    self.chn4.initSignalSlot()
    self.chn4.valueChanged.connect(self.valueChanged)
    self.chn5.initSignalSlot()
    self.chn5.valueChanged.connect(self.valueChanged)
    self.chn6.initSignalSlot()
    self.chn6.valueChanged.connect(self.valueChanged)
    self.chn7.initSignalSlot()
    self.chn7.valueChanged.connect(self.valueChanged)
    self.chn8.initSignalSlot()
    self.chn8.valueChanged.connect(self.valueChanged)
    self.filterNoise()
    self.valueTimer.start()

  def getDials(self) -> list[float]:
    """This method returns the dial values. """
    return [
      self.chn1.value(),
      self.chn2.value(),
      self.chn3.value(),
      self.chn4.value(),
      self.chn5.value(),
      self.chn6.value(),
      self.chn7.value(),
      self.chn8.value(),
    ]

  def filterNoise(self) -> None:
    """This method filters the noise through the equalizer. """
    if self.__inner_sample__ is None:
      self.__inner_sample__ = R(self.batchSize, )
    else:
      self.__inner_sample__.copy_(R(self.batchSize, ))
