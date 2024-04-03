"""Spinbox wraps QSpinBox"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDoubleSpinBox, QGridLayout
from attribox import AttriBox

from ezside.widgets import BaseWidget, TextLabel
from ezside.widgets import HorizontalSpacer, VerticalSpacer


class _Spinbox(QDoubleSpinBox):
  """Spinbox wraps QSpinBox"""

  def __init__(self, *args, **kwargs) -> None:
    minVal, maxVal = [*args, None, None][:2]
    QDoubleSpinBox.__init__(self)
    self.setRange(minVal, maxVal)
    span = maxVal - minVal
    self.setSingleStep(span / 100)
    self.setSuffix(' ~')
    self.setPrefix('~ ')

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the widget."""
    self.setMinimumHeight(32)


class SpinBox(BaseWidget):
  """Wrapper showing the Spinbox widget."""

  __label_font__ = None

  valueChanged = Signal(int)
  innerBox = AttriBox[_Spinbox](-5, 5, )
  label = AttriBox[TextLabel]()
  baseLayout = AttriBox[QGridLayout]()
  vSpacer = AttriBox[VerticalSpacer]()
  hSpacer = AttriBox[HorizontalSpacer]()

  def __init__(self, name: str = None, *args, **kwargs) -> None:
    """The __init__ method initializes the SpinBox widget."""
    BaseWidget.__init__(self, *args, **kwargs)
    self._name = name
    self.label.innerText = name
    self.initUi()
    self.connectActions()

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the widget."""
    self.innerBox.initUi()
    self.baseLayout.addWidget(self.innerBox, 0, 0, )
    self.label.defaultFont.setPointSize(12)
    self.label.initUi()
    self.baseLayout.addWidget(self.label, 1, 0, )
    # self.baseLayout.addWidget(self.hSpacer, 0, 1, 2, 1)

    self.setLayout(self.baseLayout)

  def connectActions(self) -> None:
    """The connectActions method connects the widget actions."""
    self.innerBox.valueChanged.connect(self.valueChanged.emit)

  def setValue(self, value: float) -> None:
    """The setValue method sets the value of the widget."""
    self.innerBox.setValue(value)

  def value(self) -> float:
    """The value method returns the value of the widget."""
    return self.innerBox.value()
