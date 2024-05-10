"""SevenSegmentDisplay implements a seven segment display in a widget. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout
from attribox import AttriBox
from icecream import ic

from ezside.widgets import BaseWidget, SevenSegmentDigit

ic.configureOutput(includeContext=True)


class SevenSegmentDisplay(BaseWidget):
  """SevenSegmentDisplay implements a seven segment display in a widget. """

  baseLayout: QHBoxLayout

  __dig_widgets__ = None

  @classmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """Dynamic fields"""
    return {}

  def detectState(self) -> str:
    """State detector"""
    return 'base'

  @classmethod
  def registerStates(cls) -> list[str]:
    """State register"""
    return ['base', ]

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
    """Style Fields"""
    return {}

  def initSignalSlot(self) -> None:
    """Connects signals and slots"""

  __digit_widgets__ = None
  __base_layout__ = None
  __inner_value__ = None

  numDigs = AttriBox[int]()

  def __init__(self, *args) -> None:
    parent, numDigs = None, None
    for arg in args:
      if isinstance(arg, QWidget) and parent is None:
        parent = arg
      elif isinstance(arg, int) and numDigs is None:
        numDigs = arg
      if parent is not None and numDigs is not None:
        break
    else:
      numDigs = 4 if numDigs is None else numDigs
    self.numDigs = numDigs
    BaseWidget.__init__(self, parent)

  def _getInnerValue(self) -> float:
    """Getter-function for the inner value of the widget"""
    return self.__inner_value__

  def _getDigitWidgets(self) -> list[SevenSegmentDigit]:
    """Getter-function for the digit widgets"""
    return self.__digit_widgets__

  def _getDisplayValue(self) -> float:
    """Getter-function for the value currently displayed on the widget"""
    values = [int(widget) for widget in self._getDigitWidgets()]
    c = 0
    out = 0
    while values:
      out += (values.pop() * 10 ** c)
      c += 1
    return out

  def _setInnerValue(self, value: float) -> None:
    """Setter-function for the inner value of the widget"""
    self.__inner_value__ = value
    self.update()

  @Slot(float)
  def setValue(self, value: float) -> None:
    """Setter-function for the value to be displayed on the widget"""
    widgets = reversed(self._getDigitWidgets())
    for widget in widgets:
      widget.setInnerValue(value % 10)
      value = int(value / 10)

  def update(self) -> None:
    """Checks if the inner value of the widget is different from the
    displayed value and changes before applying parent update."""
    if self._getDisplayValue() != self._getInnerValue():
      self.setValue(self._getInnerValue())
    else:
      for widget in self._getDigitWidgets():
        widget.update()
    super().update()

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    self.baseLayout = QHBoxLayout()
    for i in range(self.numDigs):
      digit = SevenSegmentDigit(self)
      digit.initUi()
      self.baseLayout.addWidget(digit)
      self._getDigitWidgets().append(digit)
    self.setLayout(self.baseLayout)
