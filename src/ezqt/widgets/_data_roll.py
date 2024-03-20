"""The DataEcho class provides a way to echo data from one object to
another."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time

import numpy as np
from attribox import AttriBox
from icecream import ic
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

ic.configureOutput(includeContext=True, )


class DataRoll:
  """The DataEcho class provides a way to echo data from one object to
  another."""

  def __init__(self, *args, **kwargs) -> None:
    self.__zero_index__ = 0
    self.__zero_time__ = time.time()
    self.__num_points__ = None
    if args:
      attriName = getattr(AttriBox, '__qualname__', None)
      if attriName is not None:
        if isinstance(attriName, str):
          boxName = '__boxes_%s__' % attriName
          if getattr(args[0].__class__, boxName, None) is not None:
            numPoints = getattr(args[0], 'getNumPoints', None)
            if numPoints is not None:
              if callable(numPoints):
                self.__num_points__ = numPoints()
    if self.__num_points__ is None:
      numKeys = stringList("""n, num, num_points, numPoints""")
      for key in numKeys:
        if key in kwargs:
          val = kwargs.get(key)
          if isinstance(val, int):
            self.__num_points__ = val
            break
          else:
            e = typeMsg(key, val, int)
            raise TypeError(e)
      else:
        for arg in args:
          if isinstance(arg, int):
            self.__num_points__ = arg
            break
        else:
          self.__num_points__ = 256
    self.__inner_array__ = None
    self.createArray()

  def createArray(self, ) -> None:
    """Creates the array."""
    n = self.__num_points__
    t = np.linspace(0, n - 1, n, dtype=np.complex64) / (n - 1)
    y = np.zeros(n, dtype=np.complex64)
    self.__inner_array__ = t + y * 1j

  def append(self, value: float = None) -> None:
    """Append a value to the DataEcho object."""
    if not value == value:
      value = 0
    entry = time.time() + value * 1j - self.__zero_time__
    self.__inner_array__[self.__zero_index__] = entry
    self.__zero_index__ = (self.__zero_index__ + 1) % len(self)

  def __len__(self, ) -> int:
    """Returns the length of the array."""
    return len(self.__inner_array__)

  def snapShot(self, ) -> np.ndarray:
    """Returns the array."""
    out = self.__inner_array__.copy()
    out = np.roll(out, -self.__zero_index__)
    zeroTime = out.real.min()
    return out - zeroTime
