"""Word provides the lowest abstraction in the Typographinator
abstraction."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Self

from attribox import AttriBox
from vistutils.fields import EmptyField
from vistutils.text import monoSpace


class Word:
  """Word provides the lowest abstraction in the Typographinator
  abstraction."""

  __inner_chars__ = None

  innerChars = EmptyField()

  def __init__(self, innerChars: str = None) -> None:
    self.innerChars = innerChars

  @innerChars.GET
  def _getInnerChars(self) -> str:
    """Returns the inner characters of the word."""
    if self.__inner_chars__ is None:
      e = """Instance of %s has not yet been initialized!"""
      raise RuntimeError(monoSpace(e % self.__class__.__name__))
    return self.__inner_chars__

  @innerChars.SET
  def _setInnerChars(self, innerChars: str) -> None:
    """Sets the inner characters of the word."""
    if self.__inner_chars__ is not None:
      e = """Instances of %s are immutable! """
      raise AttributeError(monoSpace(e % self.__class__.__name__))
    self.__inner_chars__ = innerChars

  def __len__(self, ) -> int:
    return len(self.innerChars)

  def __str__(self, ) -> str:
    return self.innerChars

  def __repr__(self, ) -> str:
    if TYPE_CHECKING:
      assert isinstance(self.innerChars, str)
    return '%s(%s)' % (self.__class__.__name__, self.innerChars)

  def __pos__(self, ) -> Self:
    """Capitalizes inner characters."""
    self.__inner_chars__ = self.__inner_chars__.capitalize()
    return self

  def __neg__(self, ) -> Self:
    """Changes inner characters to lower case"""
    self.__inner_chars__ = self.__inner_chars__.lower()
    return self

  def __invert__(self, ) -> Self:
    """Returns a copy of self"""
    return self.__class__(self.__inner_chars__)
