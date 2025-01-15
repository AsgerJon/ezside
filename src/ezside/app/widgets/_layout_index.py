"""LayoutIndex encapsulates the index of an item in a layout. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from worktoy.desc import AttriBox, Field, THIS
from worktoy.base import BaseObject, overload
from worktoy.text import monoSpace, typeMsg


class LayoutIndex(BaseObject):
  """Index encapsulates a connect region of rows and columns in a grid
  layout. """

  __iter_contents__ = None

  firstRow = AttriBox[int](0)
  firstCol = AttriBox[int](0)
  lastRow = AttriBox[int](0)
  lastCol = AttriBox[int](0)

  rowSpan = Field()
  colSpan = Field()

  @overload(int, int, int, int)
  def __init__(self, *args) -> None:
    r, c, R, C = args
    if R < 1 or C < 1:
      e = """The row and column span must be at least 1!"""
      raise ValueError(e)
    self.firstRow = r
    self.firstCol = c
    self.lastRow = r + R - 1
    self.lastCol = c + C - 1

  @overload(int, int)
  def __init__(self, *args) -> None:
    if TYPE_CHECKING:
      assert callable(self.__init__)
    self.__init__(*args, 1, 1)

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.firstRow = other.firstRow
    self.firstCol = other.firstCol
    self.lastRow = other.lastRow
    self.lastCol = other.lastCol

  @overload()
  def __init__(self, *args) -> None:
    if TYPE_CHECKING:
      assert callable(self.__init__)
    self.__init__(0, 0, 1, 1)

  @rowSpan.GET
  def _getRowSpan(self) -> int:
    return self.lastRow - self.firstRow + 1

  @colSpan.GET
  def _getColSpan(self) -> int:
    return self.lastCol - self.firstCol + 1

  def __hash__(self, ) -> int:
    return hash((self.firstRow, self.firstCol, self.lastRow, self.lastCol))

  def __eq__(self, other: Self) -> bool:
    return False if hash(self) - hash(other) else True

  def __contains__(self, item: Any) -> bool:
    cls = type(self)
    if isinstance(item, (list, tuple)):
      other = cls(*item)
    elif isinstance(item, cls):
      other = item
    else:
      return NotImplemented
    if self.firstRow > other.firstRow:
      return False
    if self.firstCol > other.firstCol:
      return False
    if self.lastRow < other.lastRow:
      return False
    if self.lastCol < other.lastCol:
      return False
    return True

  def __str__(self, ) -> str:
    """String representation of the layout index object describing the
    start row and column along with spans. """
    clsName = type(self).__name__
    row, col = self.firstRow, self.firstCol
    if self.rowSpan == 1 and self.colSpan == 1:
      info = """%s object at row: %d and column: %d"""
      return monoSpace(info % (clsName, row, col))
    info = """%s object spanning rows %d to %d and columns %d to %d"""
    return monoSpace(info % (clsName, row, self.lastRow, col, self.lastCol))

  def __repr__(self, ) -> str:
    """String representation of the layout index object. """
    clsName = type(self).__name__
    row, col = self.firstRow, self.firstCol
    if self.rowSpan == 1 and self.colSpan == 1:
      info = """%s(%d, %d, )"""
      return info % (clsName, row, col,)
    info = """%s(%d, %d, %d, %d)"""
    return info % (clsName, row, col, self.rowSpan, self.colSpan)

  def __iter__(self, ) -> Self:
    """Implements the iterator protocol. """
    if TYPE_CHECKING:
      assert isinstance(self.rowSpan, int)
      assert isinstance(self.colSpan, int)
    items = []
    cls = type(self)
    for i in range(self.rowSpan):
      for j in range(self.colSpan):
        if i or j:
          items.append(cls(self.firstRow + i, self.firstCol + j))
        else:
          items.append(self)
    self.__iter_contents__ = items
    return self

  def __next__(self, ) -> Self:
    if self.__iter_contents__ is None:
      e = """The iterator has not been initialized!"""
      raise RuntimeError(e)
    if not isinstance(self.__iter_contents__, list):
      e = typeMsg('__iter_contents__', self.__iter_contents__, list)
      raise TypeError(e)
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def values(self) -> tuple[int, int, int, int]:
    """Returns the values of the index. """
    if TYPE_CHECKING:
      assert isinstance(self.firstRow, int)
      assert isinstance(self.firstCol, int)
      assert isinstance(self.rowSpan, int)
      assert isinstance(self.colSpan, int)
    return self.firstRow, self.firstCol, self.rowSpan, self.colSpan
