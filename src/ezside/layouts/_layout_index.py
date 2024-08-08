"""LayoutIndex class encapsulates an integer valued, two-element tuple for
use as the key to the layout dictionary."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.desc import AttriBox, NODEF, DEFAULT
from worktoy.meta import BaseObject, overload
from worktoy.text import monoSpace


class LayoutIndex(BaseObject):
  """LayoutIndex class encapsulates an integer valued, two-element tuple for
  use as the key to the layout dictionary."""

  row: int
  col: int
  rowSpan: int
  colSpan: int

  row = AttriBox[int]()
  col = AttriBox[int]()
  rowSpan = AttriBox[int](1)
  colSpan = AttriBox[int](1)

  @overload(int, int, int, int)
  def __init__(self, row: int, col: int, rowSpan: int, colSpan: int) -> None:
    """Constructor for the LayoutIndex class."""
    self.row = row
    self.col = col
    self.rowSpan = rowSpan
    self.colSpan = colSpan

  @overload(int, int)
  def __init__(self, row: int, col: int) -> None:
    """Constructor for the LayoutIndex class."""
    self.row = row
    self.col = col

  @overload(tuple)
  def __init__(self, *args) -> None:
    """Constructor for the LayoutIndex class."""
    index = args[0]
    if len(index) == 1:
      self.__init__(index[0])
    elif len(index) == 2:
      self.row = index[0]
      self.col = index[1]
    elif len(index) == 3:
      e = """Layout constructor requires two or four elements, 
      but received 3!"""
      raise ValueError(monoSpace(e))
    elif len(index) == 4:
      self.row = index[0]
      self.col = index[1]
      self.rowSpan = index[2]
      self.colSpan = index[3]
    else:
      e = """Layout constructor requires two or four elements, 
      but received: '%s' of length: %d!"""
      raise ValueError(monoSpace(e % (index, len(index))))

  @overload(list)
  def __init__(self, index: list) -> None:
    """Constructor for the LayoutIndex class."""
    self.__init__((*index,))

  @overload(complex)
  def __init__(self, value: complex) -> None:
    """Constructor for the LayoutIndex class."""
    if value.imag.is_integer() and value.real.is_integer():
      self.col = int(value.real)
      self.row = int(value.imag)
    else:
      e = """Complex values must have integer components, but received: 
      '%s'!"""
      raise ValueError(monoSpace(e % value))

  def __hash__(self) -> int:
    """Hash function for the LayoutIndex class."""
    return 2 ** self.row * 3 ** self.col

  def __eq__(self, other: LayoutIndex) -> bool:
    """Equality function for the LayoutIndex class."""
    if isinstance(other, LayoutIndex):
      if (self.row - other.row) ** 2 + (self.col - other.col) ** 2:
        return False
      return True
    try:
      return self == LayoutIndex(other)
    except TypeError:
      return NotImplemented

  def __str__(self) -> str:
    """String representation"""
    return """(%d, %d)""" % (self.row, self.col)
