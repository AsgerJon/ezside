"""Size provides a dataclass representation of a size given as absolute
values for width and height. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, Any

from PySide6.QtCore import QSize, QSizeF
from worktoy.desc import AttriBox, THIS, Field
from worktoy.base import BaseObject, overload
from worktoy.meta import DispatchException


class Size(BaseObject):
  """Size provides a dataclass representation of a size given as absolute
  values for width and height. """

  __iter_contents__ = None

  width = AttriBox[int](0)
  height = AttriBox[int](0)

  Q = Field()

  @Q.GET
  def _getQSize(self) -> QSize:
    return QSize(self.width, self.height)

  @overload(int, int)
  def __init__(self, W: int, H: int) -> None:
    self.width = W
    self.height = H

  @overload()
  def __init__(self) -> None:
    self.width = 0
    self.height = 0

  @overload(THIS)
  def __init__(self, other: Size) -> None:
    self.width = other.width
    self.height = other.height

  @overload(QSize)
  def __init__(self, size: QSize) -> None:
    self.width = size.width()
    self.height = size.height()

  @overload(QSizeF)
  def __init__(self, size: QSizeF) -> None:
    size = size.toSize()
    self.width = size.width()
    self.height = size.height()

  def _resolveOther(self, other: Any) -> Self:
    cls = type(self)
    if isinstance(other, cls):
      return other
    if isinstance(other, int):
      return cls(other, other)
    if isinstance(other, float):
      return cls(int(other), int(other))
    try:
      return cls(other)
    except DispatchException as dispatchException:
      return NotImplemented

  def __add__(self, other: Any) -> Self:
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    return cls(self.width + other.width, self.height + other.height)

  def __sub__(self, other: Any) -> Self:
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    return cls(self.width - other.width, self.height - other.height)

  def __mul__(self, other: Any) -> Self:
    cls = type(self)
    if isinstance(other, int):
      return cls(self.width * other, self.height * other)
    if isinstance(other, float):
      return cls(int(self.width * other), int(self.height * other))
    return NotImplemented

  def __rmul__(self, other: Any) -> Self:
    return self * other

  def __truediv__(self, other: Any) -> Self:
    if not isinstance(other, (int, float)):
      return NotImplemented
    if other:
      return self * (1 / other)
    e = """Division by zero!"""
    raise ZeroDivisionError(e)

  def __iter__(self, ) -> Self:
    self.__iter_contents__ = [self.width, self.height]
    return self

  def __next__(self, ) -> int:
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def __getitem__(self, index: Any) -> int:
    if isinstance(index, int):
      if index not in [0, 1]:
        e = """Index must be 0 or 1!"""
        raise IndexError(e)
      if not index:
        return self.width
      if index == 1:
        return self.height
    if isinstance(index, str):
      if index.lower() == 'width':
        return self.width
      if index.lower() == 'height':
        return self.height
      if index.lower() == 'w':
        return self.width
      if index.lower() == 'h':
        return self.height
    e = """Index must be an integer or a string!"""
    raise TypeError(e)
