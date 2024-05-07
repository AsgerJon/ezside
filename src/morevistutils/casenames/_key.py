"""Key subclasses Name which locks down the inner words allowing instances
to be hashable and used as keys in dictionaries. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, Any

from morevistutils.casenames import Name


class Key:
  """Key subclasses Name which locks down the inner words allowing instances
  to be hashable and used as keys in dictionaries. """

  __iter_contents__ = None
  __frozen_state__ = False
  __inner_names__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the Key instance."""
    self.__inner_names__ = []
    for arg in args:
      if isinstance(arg, str):
        self.__inner_names__.append(Name(arg))
      elif isinstance(arg, Name):
        self.__inner_names__.append(arg)
      elif isinstance(arg, Key):
        for name in arg:
          self.__inner_names__.append(name)
    if kwargs.get('freeze', True):
      self.__frozen_state__ = True

  def _getInnerNames(self) -> list[Name]:
    """Return the inner names."""
    if self.__inner_names__ is None:
      self.__inner_names__ = []
    return self.__inner_names__

  def __setattr__(self, key, value) -> None:
    """Set the attribute."""
    if self.__frozen_state__ and key == '__inner_names__':
      e = """The Key instance is frozen and cannot be modified."""
      raise AttributeError(e)
    object.__setattr__(self, key, value)

  def __hash__(self, ) -> int:
    """Return the hash of the Key instance."""
    return hash(str(self))

  def __str__(self, ) -> str:
    """String representation"""
    out = '/'.join([str(name) for name in self])
    return out.replace('(', '').replace(')', '')

  def __repr__(self, ) -> str:
    """Code representation"""
    words = ', '.join(["'%s'" % word for word in self._getInnerNames()])
    return '%s(%s)' % (self.__class__.__name__, words)

  def __eq__(self, other: Any) -> bool:
    """Return True if the other Key is equal to this Key."""
    if isinstance(other, Key):
      if len(other) != len(self):
        return False
      for this, that in zip(self, other):
        if this != that:
          return False
      return True
    if isinstance(other, str):
      return self == Key(other)
    if isinstance(other, Name):
      if len(self) == 1 and self[0] == other:
        return True
    return NotImplemented

  def __getitem__(self, index: int) -> Name:
    """Retrieves the Name at given instance. The index must be in range
    from range(-len(self), len(self)). """
    if -len(self) <= index < len(self):
      return self._getInnerNames()[index]
    raise IndexError

  def __len__(self, ) -> int:
    """Return the number of words in the Key."""
    return len(self._getInnerNames())

  def __iter__(self) -> Self:
    """Implementation of iteration"""
    self.__iter_contents__ = [*self._getInnerNames(), ]
    return self

  def __next__(self, ) -> str:
    """Implementation of iteration"""
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __contains__(self, other: Any) -> bool:
    """Return True if the other Key is contained in this Key."""
    if isinstance(other, Name):
      for name in self:
        if name == other:
          return True
      return False
    if isinstance(other, Key):
      for name in other:
        if name not in self:
          return False
      return True
    if isinstance(other, str):
      if Name(other) in self:
        return True
      return False

  def __add__(self, other: Any) -> Self:
    """Returns a new Key with a new hash concatenating the inner names of
    self and other. """
    if isinstance(other, Key):
      return Key(*self._getInnerNames(), *other._getInnerNames())
    if isinstance(other, Name):
      return Key(*self._getInnerNames(), other)
    if isinstance(other, str):
      return Key(*self._getInnerNames(), Name(other))
    return NotImplemented
