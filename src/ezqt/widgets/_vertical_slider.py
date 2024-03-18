"""VerticalSlider provides a vertical slider."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider
from vistutils.parse import maybe
from vistutils.text import stringList

from settings import Default


class VerticalSlider(QSlider):
  """VerticalSlider provides a vertical slider."""

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
