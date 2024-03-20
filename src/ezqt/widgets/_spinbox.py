"""Spinbox wraps QSpinBox"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGridLayout, QDoubleSpinBox
from attribox import AttriBox

from ezqt.widgets import BaseWidget


class _Spinbox(QDoubleSpinBox):
  """Spinbox wraps QSpinBox"""

  def __init__(self, *args, **kwargs) -> None:
    minVal, maxVal = [*args, None, None][:2]
    if minVal is None or maxVal is None:
      raise ValueError('min and max are required!')
    QDoubleSpinBox.__init__(self)
    self.setRange(minVal, maxVal)
    span = maxVal - minVal
    self.setSingleStep(span / 100)
    self.setSuffix('float')

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the widget."""


class SpinBox(BaseWidget):
  """Wrapper showing the Spinbox widget."""

  valueChanged = Signal(int)

  baseLayout = AttriBox[QGridLayout]()
  innerBox = AttriBox[_Spinbox](0, 1)

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the widget."""
    self.innerBox.initUi()
    self.baseLayout.addWidget(self.innerBox)
    self.setLayout(self.baseLayout)

  def connectActions(self) -> None:
    """The connectActions method connects the widget actions."""
    self.innerBox.valueChanged.connect(self.valueChanged.emit)
