"""SevenSegmentDisplay implements a seven segment display in a widget. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QHBoxLayout
from vistutils.waitaminute import typeMsg

from ezside.widgets import BaseWidget, SevenSegmentDigit


class SevenSegmentDisplay(BaseWidget):
  """SevenSegmentDisplay implements a seven segment display in a widget. """

  __num_digs__ = None
  __digit_widgets__ = None
  __base_layout__ = None
  __inner_value__ = None

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

    self.__num_digs__ = numDigs

    BaseWidget.__init__(self, parent)

  def _getInnerValue(self) -> float:
    """Getter-function for the inner value of the widget"""
    return self.__inner_value__

  def _getDisplayValue(self) -> float:
    """Getter-function for the value currently displayed on the widget"""
    value = 0
    for widget in self._getDigitWidgets():
      value += float(widget)
    return value

  def _setInnerValue(self, value: float) -> None:
    """Setter-function for the inner value of the widget"""
    self.__inner_value__ = value

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
    while getattr(self, 'dig0').getScale() * 10 > value:
      self._dotLeft()
    while getattr(self, 'dig0').getScale() * 10 < value:
      self._dotRight()
    fmtSpec = '%%.%df' % self._getNumDigs()
    lmao = fmtSpec % value
    digValues = [int(d) for d in lmao]
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

  def _getNumDigs(self) -> int:
    """Get the number of digits."""
    if self.__num_digs__ is None:
      e = """The number of digits must be set before the widget is 
      initialized!"""
      raise AttributeError(e)
    if isinstance(self.__num_digs__, int):
      return self.__num_digs__
    e = typeMsg('num_digs', self.__num_digs__, int)
    raise TypeError(e)

  def _setNumDigs(self, numDigs: int) -> None:
    """Set the number of digits."""
    if self.__num_digs__ is not None:
      e = """The number of digits has already been set!"""
      raise AttributeError(e)
    if isinstance(numDigs, int):
      self.__num_digs__ = numDigs
    else:
      e = typeMsg('numDigs', numDigs, int)
      raise TypeError(e)

  def _getDigitWidgets(self) -> list[SevenSegmentDigit]:
    """Get the digit widgets."""
    n = self._getNumDigs()
    if self.__digit_widgets__ is None:
      self.__digit_widgets__ = []
      for i in range(self._getNumDigs()):
        widget = SevenSegmentDigit(self, n - i)
        key = 'dig%d' % i
        setattr(self, key, widget)
        self.__digit_widgets__.append(widget)
    return self.__digit_widgets__

  def _getBaseLayout(self, ) -> QHBoxLayout:
    """Get the base layout."""
    if self.__base_layout__ is None:
      self.__base_layout__ = QHBoxLayout(self)
    return self.__base_layout__

  def initUi(self) -> None:
    """Initialize the user interface."""
    for widget in self._getDigitWidgets():
      self._getBaseLayout().addWidget(widget)
    self.setLayout(self._getBaseLayout())
