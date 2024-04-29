"""HorizontalSlider represents a slider that can distinguish between 100
different values and which is horizontal. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSlider
from attribox import AttriBox

from ezside.core import Tight, HORIZONTAL
from ezside.widgets import BaseWidget, Label, Vertical


class HorizontalSlider(BaseWidget):
  """HorizontalSlider represents a slider that can distinguish between 100
  different values and which is horizontal. """

  __variable_name__ = None
  baseLayout = AttriBox[Vertical]()
  header = AttriBox[Label]('')
  slider = AttriBox[QSlider]()
  indicator = AttriBox[Label]('')

  valueChanged = Signal(float)
  sliderPressed = Signal()
  sliderReleased = Signal()

  def __init__(self, name: str, *args) -> None:
    self.__variable_name__ = name
    BaseWidget.__init__(self, *args)

  def getValue(self) -> float:
    """Return the value of the slider."""
    return self.slider.value() / 100

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.header.setText(self.__variable_name__)
    self.header.setSizePolicy(Tight, Tight)
    self.slider.setOrientation(HORIZONTAL)
    self.slider.setRange(0, 100)
    self.slider.setTickInterval(5)
    self.slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
    self.slider.setSingleStep(1)
    self.slider.setPageStep(5)
    self.slider.setValue(50)
    self.slider.setStyleSheet('QSlider::handle:horizontal {width: 10px;}')
    self.indicator.setText('%.2f' % self.getValue())
    self.indicator.setSizePolicy(Tight, Tight)
    self.baseLayout.addWidget(self.header)
    self.baseLayout.addWidget(self.slider)
    self.baseLayout.addWidget(self.indicator)
    self.setLayout(self.baseLayout)

  def connectActions(self) -> None:
    """The connectActions method connects the actions to the signals."""
    self.slider.sliderMoved.connect(self._updateValue)
    self.slider.sliderPressed.connect(self.sliderPressed)
    self.slider.sliderReleased.connect(self.sliderReleased)

  def _updateValue(self, position: int) -> None:
    """Updates the value of the slider."""
    self.valueChanged.emit(self.getValue())
    self.indicator.setText('%.2f' % self.getValue())
