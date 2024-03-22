"""Equalizer provides a collection of vertical sliders."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time
from math import sin
from typing import Any, Self

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from attribox import AttriBox
from vistutils.text import stringList, monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import Tight, Center
from ezside.widgets import VerticalSlider, BaseWidget, TextLabel, FilledRect, \
  HSpacer
from settings import Default


class Equalizer(BaseWidget):
  """Equalizer provides a collection of vertical sliders."""

  __vertical_sliders__ = None
  __iter_contents__ = None

  baseWidget = AttriBox[BaseWidget]()
  baseLayout = AttriBox[QHBoxLayout]()
  horizontalSpacer = AttriBox[HSpacer]()

  def __init__(self, *args, **kwargs) -> None:
    numSlidersKeys = stringList("""numSliders, num, sliders, numSliders""")
    templateKeys = stringList("""template, sliderTemplate, template""")
    Keys = [numSlidersKeys, templateKeys]
    names = stringList("""numSliders, templateSlider""")
    types = [int, QWidget]
    defaultValues = {
      names[0]: Default.numSliders,
      names[1]: VerticalSlider.defaultInstance()
    }
    data = {}
    for (name, type_, keys) in zip(names, types, Keys):
      for key in keys:
        if key in kwargs:
          val = kwargs.get(key)
          if isinstance(val, type_):
            data[name] = val
            break
      else:
        for arg in args:
          if isinstance(arg, type_):
            data[name] = arg
            break
        else:
          data[name] = defaultValues[name]
    self.numSliders = data.get(names[0])
    self._refSlider = data.get(names[1])
    BaseWidget.__init__(self, *args, **kwargs)

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(QSize(256, 256))
    self.setSizePolicy(Tight, Tight)
    for i in range(self.numSliders):
      vLayout = QVBoxLayout()
      vLayout.setContentsMargins(0, 0, 0, 0, )
      vWidget = FilledRect()
      sliderName = '__slider_%02d__' % i
      widgetName = '__widget_%02d__' % i
      layoutName = '__layout_%02d__' % i
      labelName = '__label_%02d__' % i
      slider = VerticalSlider.clone(self._refSlider)
      slider @= lambda val: val * sin(time.time() * 2 ** i)
      slider.initUi()
      label = TextLabel('%d' % 2 ** i)
      label.setSizePolicy(Tight, Tight)
      label.setMinimumSize(QSize(32, 32))
      vWidget = BaseWidget()
      setattr(self, sliderName, slider)
      setattr(self, labelName, label)
      setattr(self, widgetName, vWidget)
      setattr(self, layoutName, vLayout)
      vLayout.addWidget(label, alignment=Center)
      vLayout.addWidget(slider, alignment=Center)
      vWidget.setLayout(vLayout)
      self.baseLayout.addWidget(vWidget)

    self.baseLayout.addWidget(self.horizontalSpacer)
    self.setLayout(self.baseLayout)

  def __setitem__(self, index: int, title: str) -> None:
    """Set the title of the slider."""
    sliderName = '__slider_%02d__' % index
    labelName = '__label_%02d__' % index
    try:
      slider = getattr(self, sliderName)
      label = getattr(self, labelName)
      if not isinstance(slider, VerticalSlider):
        e = typeMsg(sliderName, slider, VerticalSlider)
        raise TypeError(e)
      if not isinstance(label, TextLabel):
        e = typeMsg(labelName, label, TextLabel)
        raise TypeError(e)
      label.setText(title)
      label.update()
      slider.update()
    except AttributeError as attributeError:
      e = """No slider at given index: '%d'""" % index
      raise IndexError(e) from attributeError
    except TypeError as typeError:
      e = """Unexpected type encountered at index: '%d'""" % index
      raise TypeError(e) from typeError

  def __getitem__(self, index: int) -> VerticalSlider:
    """Get the slider at the given index."""
    sliderName = '__slider_%02d__' % index
    try:
      return getattr(self, sliderName)
    except AttributeError as attributeError:
      e = """No slider at given index: '%d'""" % index
      raise IndexError(e) from attributeError

  def __matmul__(self, other: Any) -> Any:
    """Connect the signals of the two equalizers."""

    if isinstance(other, Equalizer):
      return self @ [float(slider) for slider in other]

    try:
      values = [val for val in other]
    except TypeError as typeError:
      if 'iterate' in str(typeError):
        return NotImplemented
      raise typeError
    if len(values) != self.numSliders:
      e = """Dimensional mismatch! Expected array of '%d' elements, but 
       received array of '%d' elements.""" % (self.numSliders, len(values))
      raise ValueError(monoSpace(e))
    if not isinstance(values, list):
      e = typeMsg('values', values, list)
      raise TypeError(e)
    out = 0j
    for (slider, value) in zip(self, values):
      out += complex(value) * float(slider)
    return out

  def __iter__(self) -> Self:
    """Iterate the sliders."""
    self.__iter_contents__ = [getattr(self, '__slider_%02d__' % i)
                              for i in range(self.numSliders)]
    return self

  def __next__(self, ) -> VerticalSlider:
    """Get the next slider."""
    if self.__iter_contents__ is None:
      e = """The iterator has not been initialized!"""
      raise RuntimeError(monoSpace(e))
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __abs__(self) -> float:
    """Return the absolute value of the equalizer."""
    return self @ [1. for _ in range(self.numSliders)]
