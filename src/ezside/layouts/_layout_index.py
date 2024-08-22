"""LayoutIndex class encapsulates an integer valued, two-element tuple for
use as the key to the layout dictionary."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from worktoy.desc import AttriBox
from worktoy.meta import BaseObject


class LayoutIndex(BaseObject):
  """LayoutIndex class encapsulates an integer valued, two-element tuple for
  use as the key to the layout dictionary."""

  row = AttriBox[int]()
  col = AttriBox[int]()
  rowSpan = AttriBox[int](1)
  colSpan = AttriBox[int](1)

  def __init__(self, row, col, *args) -> None:
    """Constructor for the LayoutIndex class."""
    BaseObject.__init__(self)
    self.row = row
    self.col = col
    if args:
      self.rowSpan = args[0]
      self.colSpan = args[1]

  def __hash__(self) -> int:
    """Hash function for the LayoutIndex class."""
    values = [self.row, self.col, self.rowSpan, self.colSpan]
    primes = [2, 3, 5, 7]
    return sum([value * prime for value, prime in zip(values, primes)])

  def __str__(self) -> str:
    """String representation"""
    return """(%d, %d)""" % (self.row, self.col)

  def __repr__(self) -> str:
    """String representation"""
    return """(%d, %d)""" % (self.row, self.col)
