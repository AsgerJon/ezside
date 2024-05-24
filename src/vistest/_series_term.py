"""SeriesTerm module provides math functions mapping from positive
integers to floating point values. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from vistutils.waitaminute import typeMsg

from morevistutils import Element


class SeriesTerm(Element):
  """SeriesTerm provides the base class for series terms. """

  __inner_function__ = None

  def __init__(self, callMeMaybe: Callable = None) -> None:
    """Initializes the SeriesTerm."""
    Element.__init__(self)
    if callMeMaybe is not None:
      if callable(callMeMaybe):
        self.__inner_function__ = callMeMaybe
      else:
        e = typeMsg('callMeMaybe', callMeMaybe, Callable)
        raise TypeError(e)
    else:
      self.__inner_function__ = lambda x: x

  def __call__(self, arg: int) -> float:
    """Calls the inner function with the given index. """
    return self.__inner_function__(arg)
