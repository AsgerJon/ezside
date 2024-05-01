"""Tester class"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Self

from vistutils.ezdata import EZData


class Point(EZData):
  """Tester class"""

  x: float = 0.
  y: float = 0.
  z: float = 0.

  def __add__(self, other: Any) -> Self:
    """Addition"""
    if isinstance(other, Point):
      return Point(self.x + other.x,
                   self.y + other.y,
                   self.z + other.z)
    return NotImplemented

  def __sub__(self, other: Any) -> Self:
    """Subtraction"""
    if isinstance(other, Point):
      return Point(self.x - other.x,
                   self.y - other.y,
                   self.z - other.z)
    return NotImplemented

  def __mul__(self, other: Any) -> Any:
    """Multiplication"""
    if isinstance(other, Point):
      return sum([self.x * other.x,
                  self.y * other.y,
                  self.z * other.z])
    if isinstance(other, int):
      return self * float(other)
    if isinstance(other, float):
      return Point(self.x * other,
                   self.y * other,
                   self.z * other)
    return NotImplemented

  def __str__(self, ) -> str:
    """String representation"""
    x, y, z = 'nan', 'nan', 'nan'
    if isinstance(self.x, float):
      x = '%.3f' % self.x
    if isinstance(self.y, float):
      y = '%.3f' % self.y
    if isinstance(self.z, float):
      z = '%.3f' % self.z
    return 'Point: x=%.3f, y=%.3f, z=%.3f' % (self.x, self.y, self.z)

  def __repr__(self) -> str:
    """Code representation"""
    return 'Point(%.3f, %.3f, %.3f)' % (self.x, self.y, self.z)
