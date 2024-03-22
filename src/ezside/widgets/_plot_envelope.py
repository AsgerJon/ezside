"""PlotEnvelope widget module."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGridLayout
from attribox import AttriBox

from ezside.widgets import BaseWidget, SpinBox, PushButton


class PlotEnvelope(BaseWidget):
  """PlotEnvelope widget."""

  __min_horizontal_value__ = 0
  __max_horizontal_value__ = 1
  __min_vertical_value__ = 0
  __max_vertical_value__ = 1

  valueChanged = Signal()
  newValues = Signal()
  cancelled = Signal()

  basePlot = AttriBox[QGridLayout]()
  minHorizontal = AttriBox[SpinBox]('Min. Horizontal')
  maxHorizontal = AttriBox[SpinBox]('Max. Horizontal')
  minVertical = AttriBox[SpinBox]('Min. Vertical')
  maxVertical = AttriBox[SpinBox]('Max. Vertical')
  apply = AttriBox[PushButton]('Apply')
  cancel = AttriBox[PushButton]('Cancel')

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the widget."""
    self.setMinimumSize(96, 96)
    self.minHorizontal.initUi()
    self.minHorizontal.setValue(-1)
    self.basePlot.addWidget(self.apply, 0, 0)
    self.maxHorizontal.initUi()
    self.maxHorizontal.setValue(1)
    self.basePlot.addWidget(self.cancel, 1, 0)
    self.minHorizontal.initUi()
    self.minHorizontal.setValue(-1)
    self.basePlot.addWidget(self.minHorizontal, 0, 1)
    self.maxHorizontal.initUi()
    self.maxHorizontal.setValue(1)
    self.basePlot.addWidget(self.maxHorizontal, 1, 1)
    self.minVertical.initUi()
    self.minVertical.setValue(-1)
    self.basePlot.addWidget(self.minVertical, 0, 2)
    self.maxVertical.initUi()
    self.maxVertical.setValue(1)
    self.basePlot.addWidget(self.maxVertical, 1, 2)
    self.setLayout(self.basePlot)
    self.connectActions()

  def connectActions(self) -> None:
    """The connectActions method connects the widget actions."""
    self.apply.clicked.connect(self.newValues.emit)
    self.cancel.clicked.connect(self.cancelled.emit)
    self.minHorizontal.valueChanged.connect(self.handleValueChanged)
    self.maxHorizontal.valueChanged.connect(self.handleValueChanged)
    self.minVertical.valueChanged.connect(self.handleValueChanged)
    self.maxVertical.valueChanged.connect(self.handleValueChanged)

  def handleApply(self) -> None:
    """Handle the apply button."""
    self.__min_horizontal_value__ = self.minHorizontal.value()
    self.__max_horizontal_value__ = self.maxHorizontal.value()
    self.__min_vertical_value__ = self.minVertical.value()
    self.__max_vertical_value__ = self.maxVertical.value()
    self.apply.setEnabled(False)
    self.newValues.emit()

  def handleCancel(self) -> None:
    """Handle the cancel button."""
    self.minHorizontal.setValue(self.__min_horizontal_value__)
    self.maxHorizontal.setValue(self.__max_horizontal_value__)
    self.minVertical.setValue(self.__min_vertical_value__)
    self.maxVertical.setValue(self.__max_vertical_value__)
    self.cancel.setEnabled(False)
    self.cancelled.emit()

  def handleValueChanged(self) -> None:
    """Handle the value changed signal."""
    self.apply.setEnabled(True)
    self.cancel.setEnabled(True)
    self.valueChanged.emit()

  def getValues(self) -> dict[str, float]:
    """The getValueDict method returns the values of the widget."""
    return {'minH': self.minHorizontal.value(),
            'maxH': self.maxHorizontal.value(),
            'minV': self.minVertical.value(),
            'maxV': self.maxVertical.value()}
