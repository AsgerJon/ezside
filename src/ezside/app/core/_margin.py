"""Margin provides a data class for managing margins."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, Any

from PySide6.QtCore import QMargins, QMarginsF
from worktoy.desc import AttriBox, THIS, Field
from worktoy.base import BaseObject, overload
from worktoy.meta import DispatchException

from . import Point, Size


class Margin(BaseObject):
  """Dataclass providing left, top, right, and bottom margin values."""

  left = AttriBox[int](0)
  top = AttriBox[int](0)
  right = AttriBox[int](0)
  bottom = AttriBox[int](0)

  Q = Field()
  eccentricity = Field()

  @Q.GET
  def _getQMargins(self) -> QMargins:
    return QMargins(self.left, self.top, self.right, self.bottom)

  @eccentricity.GET
  def _getEccentricity(self) -> Point:
    """Getter-function for how a rectangle will translate when this margin
    is added to it. """
    return Point(self.left - self.right, self.top - self.bottom)

  @overload(int, int, int, int)
  def __init__(self, L: int, T: int, R: int, B: int) -> None:
    self.left = L
    self.top = T
    self.right = R
    self.bottom = B

  @overload(int, int)
  def __init__(self, H: int, V: int) -> None:
    self.left = H
    self.top = V
    self.right = H
    self.bottom = V

  @overload(int)
  def __init__(self, A: int) -> None:
    self.left = A
    self.top = A
    self.right = A
    self.bottom = A

  @overload()
  def __init__(self, **kwargs) -> None:
    self.left = kwargs.get('left', 0)
    self.top = kwargs.get('top', 0)
    self.right = kwargs.get('right', 0)
    self.bottom = kwargs.get('bottom', 0)

  @overload(THIS)
  def __init__(self, other: Margin) -> None:
    self.left = other.left
    self.top = other.top
    self.right = other.right
    self.bottom = other.bottom

  @overload(QMargins)
  def __init__(self, other: QMargins) -> None:
    self.left = other.left()
    self.top = other.top()
    self.right = other.right()
    self.bottom = other.bottom()

  @overload(QMarginsF)
  def __init__(self, other: QMarginsF) -> None:
    intMargins = QMarginsF.toMargins(other)
    self.left = intMargins.left()
    self.top = intMargins.top()
    self.right = intMargins.right()
    self.bottom = intMargins.bottom()

  def _resolveOther(self, other: Any) -> Self:
    cls = type(self)
    try:
      return cls(*other) if isinstance(other, tuple) else cls(other)
    except DispatchException:
      return NotImplemented

  def __add__(self, other: Margin) -> Margin:
    """Adds two Margins by adding each component. """
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    L = self.left + other.left
    T = self.top + other.top
    R = self.right + other.right
    B = self.bottom + other.bottom
    return cls(L, T, R, B)

  def __radd__(self, other: Size) -> Size:
    width = other.width + self.left + self.right
    height = other.height + self.top + self.bottom
    return Size(width, height)

  def __sub__(self, other: Margin) -> Margin:
    """Subtracts two Margins by subtracting each component. """
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    L = self.left - other.left
    T = self.top - other.top
    R = self.right - other.right
    B = self.bottom - other.bottom
    return cls(L, T, R, B)

  def __rsub__(self, other: Size) -> Size:
    width = other.width - self.left - self.right
    height = other.height - self.top - self.bottom
    return Size(width, height)

  def __mul__(self, other: float) -> Margin:
    """Multiplies a Margin by an integer. """
    cls = type(self)
    if isinstance(other, int):
      L = self.left * other
      T = self.top * other
      R = self.right * other
      B = self.bottom * other
    elif isinstance(other, float):
      L = int(self.left * other)
      T = int(self.top * other)
      R = int(self.right * other)
      B = int(self.bottom * other)
    else:
      return NotImplemented
    return cls(L, T, R, B)

  def __truediv__(self, other: int) -> Margin:
    """Divides a Margin by an integer. """
    if not other:
      e = """Division by zero is not allowed. """
      raise ZeroDivisionError(e)
    if isinstance(other, (int, float)):
      return self * (1 / other)
