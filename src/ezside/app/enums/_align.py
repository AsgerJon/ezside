"""Align enumerates the horizontal and vertical alignment options for the
QOL app."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from enum import EnumType
from typing import Self

from PySide6.QtCore import Qt
from worktoy.desc import Field
from worktoy.keenum import auto

from . import AbstractEnum, HorizontalAlign, VerticalAlign
from ..core import Rect, Size

_Q_LEFT = Qt.AlignmentFlag.AlignLeft
_Q_CENTER = Qt.AlignmentFlag.AlignCenter
_Q_RIGHT = Qt.AlignmentFlag.AlignRight
_Q_TOP = Qt.AlignmentFlag.AlignTop
_Q_BOTTOM = Qt.AlignmentFlag.AlignBottom

_Q_LEFT_TOP = _Q_LEFT | _Q_TOP
_Q_LEFT_CENTER = _Q_LEFT | _Q_CENTER
_Q_LEFT_BOTTOM = _Q_LEFT | _Q_BOTTOM
_Q_CENTER_TOP = _Q_CENTER | _Q_TOP
_Q_CENTER_BOTTOM = _Q_CENTER | _Q_BOTTOM
_Q_RIGHT_TOP = _Q_RIGHT | _Q_TOP
_Q_RIGHT_CENTER = _Q_RIGHT | _Q_CENTER
_Q_RIGHT_BOTTOM = _Q_RIGHT | _Q_BOTTOM


class Align(AbstractEnum):
  """Enumerates the horizontal and vertical alignment options for the QOL
  app."""

  @classmethod
  def getQClass(cls) -> EnumType:
    """Returns the Qt version of this enumeration."""
    return Qt.AlignmentFlag

  @classmethod
  def getLeft(cls) -> tuple[Self, Self, Self]:
    """Returns the left alignment."""
    return cls.LEFT_TOP, cls.LEFT_CENTER, cls.LEFT_BOTTOM

  @classmethod
  def getHCenter(cls) -> tuple[Self, Self, Self]:
    """Returns the center alignment."""
    return cls.CENTER_TOP, cls.CENTER, cls.CENTER_BOTTOM

  @classmethod
  def getRight(cls) -> tuple[Self, Self, Self]:
    """Returns the right alignment."""
    return cls.RIGHT_TOP, cls.RIGHT_CENTER, cls.RIGHT_BOTTOM

  @classmethod
  def getTop(cls) -> tuple[Self, Self, Self]:
    """Returns the top alignment."""
    return cls.LEFT_TOP, cls.CENTER_TOP, cls.RIGHT_TOP

  @classmethod
  def getVCenter(cls) -> tuple[Self, Self, Self]:
    """Returns the middle alignment."""
    return cls.LEFT_CENTER, cls.CENTER, cls.RIGHT_CENTER

  @classmethod
  def getBottom(cls) -> tuple[Self, Self, Self]:
    """Returns the bottom alignment."""
    return cls.LEFT_BOTTOM, cls.CENTER_BOTTOM, cls.RIGHT_BOTTOM

  horizontal = Field()
  vertical = Field()

  LEFT_TOP = auto(_Q_LEFT_TOP)
  LEFT_CENTER = auto(_Q_LEFT_CENTER)
  LEFT_BOTTOM = auto(_Q_LEFT_BOTTOM)
  CENTER_TOP = auto(_Q_CENTER_TOP)
  CENTER = auto(_Q_CENTER)
  CENTER_BOTTOM = auto(_Q_CENTER_BOTTOM)
  RIGHT_TOP = auto(_Q_RIGHT_TOP)
  RIGHT_CENTER = auto(_Q_RIGHT_CENTER)
  RIGHT_BOTTOM = auto(_Q_RIGHT_BOTTOM)

  @horizontal.GET
  def _getHorizontal(self) -> HorizontalAlign:
    """Returns the horizontal alignment."""
    if self in self.getLeft():
      return HorizontalAlign.LEFT
    if self in self.getHCenter():
      return HorizontalAlign.CENTER
    if self in self.getRight():
      return HorizontalAlign.RIGHT
    e = """Unable to resolve horizontal alignment"""
    raise ValueError(e)

  @vertical.GET
  def _getVertical(self) -> VerticalAlign:
    """Returns the vertical alignment."""
    if self in self.getTop():
      return VerticalAlign.TOP
    if self in self.getVCenter():
      return VerticalAlign.CENTER
    if self in self.getBottom():
      return VerticalAlign.BOTTOM
    e = """Unable to resolve vertical alignment"""
    raise ValueError(e)

  def apply(self, rect: Rect, size: Size) -> Rect:
    """Applies this alignment to the given rectangle and size."""
    if self.horizontal is HorizontalAlign.LEFT:
      L = rect.left
    elif self.horizontal is HorizontalAlign.CENTER:
      L = rect.left + (rect.width - size.width) // 2
    elif self.horizontal is HorizontalAlign.RIGHT:
      L = rect.right - size.width
    else:
      e = """Unable to resolve horizontal alignment"""
      raise ValueError(e)
    if self.vertical is VerticalAlign.TOP:
      T = rect.top
    elif self.vertical is VerticalAlign.CENTER:
      T = rect.top + (rect.height - size.height) // 2
    elif self.vertical is VerticalAlign.BOTTOM:
      T = rect.bottom - size.height
    else:
      e = """Unable to resolve vertical alignment"""
      raise ValueError(e)
    return Rect(L, T, size)
