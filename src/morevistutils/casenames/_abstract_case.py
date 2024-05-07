"""AbstractCase provides an abstract baseclass for creation of custom name
cases beyond the common snake case or camel case. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from types import MethodType
from typing import Any

from vistutils.waitaminute import typeMsg


class MetaCase(type):
  """Metaclass improving the __str__ and nothing else"""

  def __str__(cls) -> str:
    """String representation"""
    return cls.__name__

  def __rmatmul__(cls, other: Any) -> Any:
    """Return the result of the joinWords method."""
    joinWords = getattr(cls, 'joinWords', None)
    if joinWords is None:
      return NotImplemented
    if callable(joinWords):
      return joinWords(*other)
    e = typeMsg('joinWords', joinWords, Callable)
    raise TypeError(e)


class AbstractCase(metaclass=MetaCase):
  """AbstractCase provides an abstract baseclass for creation of custom name
  cases beyond the common snake case or camel case. """

  @classmethod
  @abstractmethod
  def joinWords(cls, *words: str) -> str:
    """Join the words together using the rules of the case."""

  @classmethod
  @abstractmethod
  def resolveName(cls, name: str) -> list[str]:
    """Assuming the name is of this case, this method is expected to
    return a list of lower case versions of the constituent words. """

  @classmethod
  def recognizeName(cls, *testNames: str) -> bool:
    """This method uses the two subclass provided methods joinWords and
    resolveName to verify if a name is of the case. Please note that a
    name may very well"""
    if len([*testNames, ]) == 1:
      testWords = cls.resolveName(testNames[0])
      testName = cls.joinWords(*testWords)
      return True if testName == testNames[0] else False
    testName = cls.joinWords(*testNames)
    testWords = cls.resolveName(testName)
    for name, word in zip(testNames, testWords):
      if name != word:
        return False
    return True
