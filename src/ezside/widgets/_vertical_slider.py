"""VerticalSlider provides a vertical slider."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Self

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QSlider
from vistutils.parse import maybe
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from ezside.core import Expand
from settings import Default


class VerticalSlider(QSlider):
  """VerticalSlider provides a vertical slider."""

  __value_map__ = None

  @classmethod
  def defaultInstance(cls) -> VerticalSlider:
    """Return the default instance."""
    return cls()

  @classmethod
  def clone(cls, slider: VerticalSlider = None) -> VerticalSlider:
    """Clone the given slider."""
    if slider is None:
      return cls.defaultInstance()
    if isinstance(slider, (cls, QSlider)):
      return cls(slider.minimum(), slider.maximum(), slider.singleStep(),
                 slider.pageStep(), slider.value())
    e = typeMsg('slider', slider, cls)
    raise TypeError(e)

  def __init__(self, *args, **kwargs) -> None:
    minVal, maxVal, singleStep, pageStep, initVal = [None] * 5
    minValKeys = stringList("""min, minVal, minimum, minVal""")
    maxValKeys = stringList("""max, maxVal, maximum, maxVal""")
    singleStepKeys = stringList("""singleStep, step, single, stepSize""")
    pageStepKeys = stringList("""pageStep, page, pageStepSize""")
    initValKeys = stringList("""initVal, value, init, val""")
    Keys = [minValKeys, maxValKeys, singleStepKeys, pageStepKeys,
            initValKeys]
    for keys in Keys:
      for key in keys:
        if key in kwargs:
          val = kwargs.get(key)
          if key in minValKeys:
            if isinstance(val, int):
              minVal = val
              break
          elif key in maxValKeys:
            if isinstance(val, int):
              maxVal = val
              break
          elif key in singleStepKeys:
            if isinstance(val, int):
              singleStep = val
              break
          elif key in pageStepKeys:
            if isinstance(val, int):
              pageStep = val
              break
          elif key in initValKeys:
            if isinstance(val, int):
              initVal = val
              break
    else:
      for arg in args:
        if isinstance(arg, int):
          if minVal is None:
            minVal = arg
          elif maxVal is None:
            maxVal = arg
          elif singleStep is None:
            singleStep = arg
          elif pageStep is None:
            pageStep = arg
          elif initVal is None:
            initVal = arg
    minVal = maybe(minVal, Default.sliderMin)
    maxVal = maybe(maxVal, Default.sliderMax)
    singleStep = maybe(singleStep, Default.sliderSingleStep)
    pageStep = maybe(pageStep, Default.sliderPageStep)
    QSlider.__init__(self, Qt.Orientation.Vertical)
    self.setRange(minVal, maxVal)
    self.setSingleStep(singleStep)
    self.setPageStep(pageStep)
    self.setTickInterval(pageStep)
    self.setValue(maybe(initVal, minVal))
    self.applyStyleSheet()

  def applyStyleSheet(self) -> None:
    """
    Applies the stylesheet to the slider to make the handle larger
    and potentially apply other custom styles.
    """
    self.setStyleSheet("""
      QSlider::handle:horizontal {
        background: #5c5c5c;
        border: 1px solid #5c5c5c;
        width: 20px;
        margin: -10px 0; /* expand outside the container */
      }

      QSlider::handle:vertical {
        background: #5c5c5c;
        border: 1px solid #5c5c5c;
        height: 20px;
        margin: 0 -10px; /* expand outside the container */
      }
    """)

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setSizePolicy(Expand, Expand)
    self.setMinimumSize(QSize(Default.sliderWidth, Default.sliderHeight))

  def __abs__(self) -> int:
    """Return the absolute value of the slider."""
    return self.maximum() - self.minimum()

  def __float__(self) -> float:
    """Return the float value of the slider."""
    baseValue = float(self.value()) / abs(self)
    if self.__value_map__ is None:
      return baseValue
    if callable(self.__value_map__):
      return self.__value_map__(baseValue)
    try:
      f = float(self.__value_map__)
    except Exception as exception:
      e = typeMsg('value_map', self.__value_map__, Callable)
      raise TypeError(e) from exception
    return f * baseValue

  def __int__(self) -> int:
    """Return the integer value of the slider."""
    return self.value()

  def __neg__(self) -> int:
    """Return the negated value of the slider."""
    return self.maximum() - self.value()

  def __pos__(self) -> int:
    """Return the positive value of the slider."""
    return self.value() - self.minimum()

  def __imul__(self, value: float) -> Self:
    """Set value map to float."""
    if not isinstance(value, (int, float)):
      e = typeMsg('value', value, float)
      raise TypeError(e)
    self.__value_map__ = value
    return self

  def __imatmul__(self, callMeMaybe: Callable) -> Self:
    """Set value map to callable"""
    if not callable(callMeMaybe):
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)
    self.__value_map__ = callMeMaybe
    return self
