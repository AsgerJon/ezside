"""ArgRoulette encapsulates stochastic variable sampling. Instances may be
concatenated to form array like instances."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import choice, random
from string import ascii_letters, digits, punctuation
from typing import Callable

from attribox import AttriBox

from moreattribox import Wait


class ArgRoulette:
  """ArgRoulette encapsulates stochastic variable sampling. Instances may be
  concatenated to form array like instances."""

  __inner_type__ = None


class IntRoulette:
  """IntRoulette encapsulates stochastic integer sampling. Instances may be
  concatenated to form array like instances."""

  __inner_type__ = int


class CharacterRoulette:
  """CharRoulette encapsulates stochastic character sampling. Instances
  may be concatenated to form array like instances."""
  __inner_type__ = str

  chars = '%s%s%s ' % (ascii_letters, digits, punctuation)
  __value_space__ = [char for char in chars]

  def getSingle(self, ) -> str:
    """Returns a single character from the value space."""


class ArrayRoulette(ArgRoulette):
  """ArrayRoulette encapsulates stochastic array sampling. Instances may be
  concatenated to form array like instances."""
  __inner_type__ = object

  __value_space__ = None

  def __init__(self, *args: ArgRoulette) -> None:
    self.__value_space__ = [*args, ]

  def getSingle(self, ) -> object:
    """Returns a single character from the value space."""
    return choice(self.__value_space__)


class UnitRoulette(ArgRoulette):
  """FloatRoulette encapsulates stochastic float sampling. Instances may be
  concatenated to form array like instances."""
  __inner_type__ = float
  __min_value__ = None
  __max_value__ = None
  __fallback_min__ = 0.0
  __fallback_max__ = 1.0

  minVal = AttriBox[float](0.0)
  maxVal = AttriBox[float](1.0)

  def __init__(self, *args: ArgRoulette) -> None:
    floatArgs = []
    for arg in args:
      if isinstance(arg, (int, float)):
        floatArgs.append(float(arg))
    self.minVal, self.maxVal = [*floatArgs, None, None][:2]

  def getSingle(self, ) -> float:
    """Returns a single character from the value space. """


class NormalRoulette(ArgRoulette):
  """NormalRoulette encapsulates stochastic normal float sampling. Instances
  may be concatenated to form array like instances."""

  mean = AttriBox[float](0.0)
  std = AttriBox[float](1.0)  # Standard deviation.
  pi = Wait()

  def __init__(self, *args: ArgRoulette) -> None:
    UnitRoulette.__init__(self, )
    floatArgs = []
    for arg in args:
      if isinstance(arg, (int, float)):
        floatArgs.append(float(arg))
    m, s = [*floatArgs, None, None][:2]
    self.mean = m if m is not None else self.mean
    self.std = s if s is not None else self.std
