"""SevenSegmentDisplay implements a seven segment display in a widget. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget
from attribox import AttriBox
from icecream import ic

from ezside.widgets import BaseWidget, SevenSegmentDigit
from ezside.widgets.layouts import HorizontalLayout
from morevistutils import Bag


class SevenSegmentDisplay(BaseWidget):
  """SevenSegmentDisplay implements a seven segment display in a widget. """

  __digit_widgets__ = None
  __base_layout__ = None
  __inner_value__ = None

  numDigs = AttriBox[int]()
  baseLayout = AttriBox[HorizontalLayout](spacing=4)
  digWidgets = SevenSegmentDigit @ Bag()

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
    return [*self.baseLayout]

  def _getDisplayValue(self) -> float:
    """Getter-function for the value currently displayed on the widget"""
    value = 0
    for widget in self._getDigitWidgets():
      value += float(widget)
    return value

  def _setInnerValue(self, value: float) -> None:
    """Setter-function for the inner value of the widget"""
    self.__inner_value__ = value
    self.update()

  @Slot(float)
  def setValue(self, value: float) -> None:
    """Setter-function for the value to be displayed on the widget"""
    ic(value)
    self._setInnerValue(value)

  def _dotLeft(self) -> None:
    """Shifts all digits left"""
    for widget in self._getDigitWidgets():
      widget.dotLeft()

  def _dotRight(self) -> None:
    """Shifts all digits right"""
    for widget in self._getDigitWidgets():
      widget.dotRight()

  def _setDisplayValue(self, value: float) -> None:
    """Setter-function for the value currently displayed on the widget"""
    while 10 ** self.baseLayout[0].getScale() > 10 * value:
      self._dotLeft()
    while 10 ** self.baseLayout[0].getScale() < 10 * value:
      self._dotRight()
    for widget in self.baseLayout:
      ic(widget.getScale())
    fmtSpec = '%%.%df' % len(self.baseLayout)
    lmao = fmtSpec % value
    dotLeft, dotRight = [*[len(i) for i in lmao.split('.')], None][:2]
    digChars = [c for c in lmao if c in '0123456789']
    digValues = [int(d) for d in digChars]
    for widget, value in zip(self._getDigitWidgets(), digValues):
      widget.setInnerValue(value)

  def update(self) -> None:
    """Checks if the inner value of the widget is different from the
    displayed value and changes before applying parent update."""
    if self._getDisplayValue() != self._getInnerValue():
      self._setDisplayValue(self._getInnerValue())
    else:
      for widget in self._getDigitWidgets():
        widget.update()
    super().update()

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    n = 0
    for i in range(self.numDigs):
      n = self.numDigs - i - 1
      self.baseLayout.addWidget(self.digWidgets(scale=n, key='%d' % n))
    n -= 1
    self.baseLayout.addWidget(
      self.digWidgets(dot=True, scale=n, key='%d' % n))
    self.baseLayout.initUi()
