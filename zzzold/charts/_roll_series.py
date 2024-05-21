"""RollSeries subclasses the QXYSeries class and provides a FIFO buffered
data series. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from math import sin
import time

from PySide6.QtCharts import QScatterSeries
from PySide6.QtCore import QPointF
from icecream import ic
from torch import zeros, complex64, Tensor, ones
from vistutils.waitaminute import typeMsg

from ezside.torchcuts import f32, C128, C64

ic.configureOutput(includeContext=True, )


class RollSeries(QScatterSeries):
  """RollData provides a pythonic data structure for a FIFO buffered data."""

  __num_points__ = None
  __fallback_points__ = 128

  __inner_data__ = []
  __circular_buffer__ = None
  __last_time__ = None

  def __init__(self, *args, **kwargs) -> None:
    QScatterSeries.__init__(self)
    for arg in args:
      if isinstance(arg, int):
        self.__num_points__ = arg
        break
    else:
      self.__num_points__ = self.__fallback_points__

  def _createCircularBuffer(self, ) -> None:
    """Creates the circular buffer"""
    shape = (self.__num_points__,)
    self.__circular_buffer__ = zeros(shape, dtype=C64)

  def _getCircularBuffer(self, **kwargs) -> Tensor:
    """Getter-function for circular buffer"""
    if self.__circular_buffer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createCircularBuffer()
      return self._getCircularBuffer(_recursion=True)
    if isinstance(self.__circular_buffer__, Tensor):
      return self.__circular_buffer__
    e = typeMsg('self.__circular_buffer__', self.__circular_buffer__, Tensor)
    raise TypeError(e)

  def _rollCircularBuffer(self, ) -> None:
    """Rolls the circular buffer"""
    if self.__circular_buffer__ is not None:
      self.__circular_buffer__.copy_(self.__circular_buffer__.roll(-1))

  def addValue(self, value: float = None) -> None:
    """Buffers the value with a time stamp"""
    rightNow = time.perf_counter()
    value = sin(rightNow) if value is None else value
    n = len(self._getCircularBuffer())
    self._getCircularBuffer()[n - 1] = (rightNow + value * 1j) * ones(1)
    self._rollCircularBuffer()

  def updateValues(self) -> None:
    """Updates the values in the circular buffer"""
    self.clear()
    rightNow = time.perf_counter()
    data = self._getCircularBuffer()
    P = [QPointF(t - rightNow, s) for (t, s) in zip(data.real, data.imag)]
    self.append(P)
