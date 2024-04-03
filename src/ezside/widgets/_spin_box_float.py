"""SpinBox widget. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDoubleSpinBox, QVBoxLayout, QHBoxLayout
from attribox import AttriBox
from ezside.core import Tight, AlignCenter
from ezside.widgets import BaseWidget
from icecream import ic
from vistutils.parse import maybe

from ezros.rosutils import EmptyField
from ezros.widgets import TightLabel, Label

ic.configureOutput(includeContext=True, )


class SpinBoxFloat(BaseWidget):
  """SpinBox widget. """

  __label_title__ = None
  __min_value__ = None
  __spin_value__ = None
  __max_value__ = None

  value = EmptyField()

  inner = AttriBox[QDoubleSpinBox]()
  baseLayout = AttriBox[QVBoxLayout]()
  verticalLayout = AttriBox[QVBoxLayout]()
  horizontalLayout = AttriBox[QHBoxLayout]()
  label = AttriBox[Label]()

  valueChanged = Signal(float)
  newValue = Signal(float)
  update = Signal()

  def __init__(self, *args, ) -> None:
    """Initialize the widget."""
    BaseWidget.__init__(self, *args, )
    if not args:
      e = """Received no positional arguments"""
      raise ValueError(e)
    strArgs = [arg for arg in args if isinstance(arg, str)]
    label, _orientation = [*strArgs, None, None][:2]
    self.__label_title__ = maybe(label, 'label title')
    self.__orientation__ = maybe(_orientation, 'vertical')
    floatArgs = [arg for arg in args if isinstance(arg, (int, float))]
    self.__label_title__ = strArgs[0]
    min_, val, max_ = [*floatArgs, None, None, None][:3]
    if any([min_ is None, val is None, max_ is None]):
      e = """The minimum, initial value and maximum value are required!"""
      raise ValueError(e)
    self.__min_value__ = min_
    self.__spin_value__ = val
    self.__max_value__ = max_

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.inner.setMinimumHeight(32)
    self.inner.setRange(self.__min_value__, self.__max_value__)
    self.inner.setValue(self.__spin_value__)
    self.label.setText(self.__label_title__)
    self.label.setSizePolicy(Tight, Tight)
    self.label.setAlignment(AlignCenter)
    if self.__orientation__ == 'vertical':
      self.verticalLayout.addWidget(self.label)
      self.verticalLayout.addWidget(self.inner)
      return self.setLayout(self.verticalLayout)
    elif self.__orientation__ == 'horizontal':
      self.horizontalLayout.addWidget(self.label)
      self.horizontalLayout.addWidget(self.inner)
      return self.setLayout(self.horizontalLayout)
    e = """Failed to recognize orientation: %s""" % self.__orientation__
    raise ValueError(e)

  def connectActions(self) -> None:
    """Connect actions to slots."""
    self.inner.valueChanged.connect(self.newValue.emit)
    self.inner.valueChanged.connect(self.valueChanged.emit)
    self.inner.editingFinished.connect(self.update.emit)

  def __str__(self, ) -> str:
    """Return a string representation of the widget."""
    clsName = self.__class__.__name__
    title = self.label.getText()
    return '%s: %s' % (clsName, title)

  def __repr__(self, ) -> str:
    """Return a string representation of the widget."""
    title = self.__label_title__
    min_, max_ = self.__min_value__, self.__max_value__
    value = self.__spin_value__
    clsName = self.__class__.__qualname__
    return '%s(%s, %s, %s, %s)' % (clsName, title, min_, value, max_)

  @value.GET
  def getValue(self, ) -> float:
    """Return the value of the spin box."""
    return self.inner.value()
