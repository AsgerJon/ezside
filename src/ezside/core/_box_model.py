"""BoxModel class for handling box model calculations."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from worktoy.base import BaseObject, overload
from worktoy.desc import AttriBox

from . import Margin, RGBA

if TYPE_CHECKING:
  from . import Rect, Size


class BoxModel(BaseObject):
  """BoxModel class for handling box model calculations."""

  marginShape = AttriBox[Margin](1, 1, 1, 1, )
  borderShape = AttriBox[Margin](1, 1, 1, 1, )
  paddingShape = AttriBox[Margin](2, 2, 2, 2, )

  marginColor = AttriBox[RGBA](0, 0, 0, 0, )
  borderColor = AttriBox[RGBA](0, 0, 0, 255, )
  paddingColor = AttriBox[RGBA](255, 255, 255, 255)

  cornerRadiusX = AttriBox[int](1)
  cornerRadiusY = AttriBox[int](1)

  @staticmethod
  def _parseShape(shape: Any) -> Margin:
    """Attempts to create an instance of Margin based on the given shape. """
    if isinstance(shape, (list, tuple)):
      return Margin(*shape)
    elif isinstance(shape, dict):
      return Margin(**shape)
    return Margin(shape)

  @staticmethod
  def _parseColor(color: Any) -> RGBA:
    """Attempts to create an instance of RGBA based on the given color. """
    if isinstance(color, (list, tuple)):
      return RGBA(*color)
    elif isinstance(color, dict):
      return RGBA(**color)
    return RGBA(color)

  def _parseKwargs(self, **kwargs) -> None:
    """Parse kwargs for this object."""
    cls = type(self)
    if 'marginShape' in kwargs and 'marginColor' in kwargs:
      self.marginShape = self._parseShape(kwargs['marginShape'])
      self.marginColor = self._parseColor(kwargs['marginColor'])
    elif 'margin' in kwargs:
      val = kwargs['margin']
      if isinstance(val, dict):
        if 'shape' in val and 'color' in val:
          self.marginShape = self._parseShape(val['shape'])
          self.marginColor = self._parseColor(val['color'])
        else:
          e = """Expected 'shape' and 'color' keys in 'margin' dict."""
          raise KeyError(e)
      elif isinstance(val, cls):
        self.marginShape = val.marginShape
        self.marginColor = val.marginColor
    if 'borderShape' in kwargs and 'borderColor' in kwargs:
      self.borderShape = self._parseShape(kwargs['borderShape'])
      self.borderColor = self._parseColor(kwargs['borderColor'])
    elif 'border' in kwargs:
      val = kwargs['border']
      if isinstance(val, dict):
        if 'shape' in val and 'color' in val:
          self.borderShape = self._parseShape(val['shape'])
          self.borderColor = self._parseColor(val['color'])
        else:
          e = """Expected 'shape' and 'color' keys in 'border' dict."""
          raise KeyError(e)
      elif isinstance(val, cls):
        self.borderShape = val.borderShape
        self.borderColor = val.borderColor
    if 'paddingShape' in kwargs and 'paddingColor' in kwargs:
      self.paddingShape = self._parseShape(kwargs['paddingShape'])
      self.paddingColor = self._parseColor(kwargs['paddingColor'])
    elif 'padding' in kwargs:
      val = kwargs['padding']
      if isinstance(val, dict):
        if 'shape' in val and 'color' in val:
          self.paddingShape = self._parseShape(val['shape'])
          self.paddingColor = self._parseColor(val['color'])
        else:
          e = """Expected 'shape' and 'color' keys in 'padding' dict."""
          raise KeyError(e)
      elif isinstance(val, cls):
        self.paddingShape = val.paddingShape
        self.paddingColor = val.paddingColor

  @overload()
  def __init__(self, **kwargs) -> None:
    self._parseKwargs(**kwargs)

  @overload(Margin, Margin, Margin, RGBA, RGBA, RGBA)
  def __init__(self, *args) -> None:
    self.marginShape = args[0]
    self.borderShape = args[1]
    self.paddingShape = args[2]
    self.marginColor = args[3]
    self.borderColor = args[4]
    self.paddingColor = args[5]

  @overload(Margin, RGBA)
  def __init__(self, margin: Margin, color: RGBA) -> None:
    self.marginShape = margin
    self.borderShape = margin
    self.paddingShape = margin
    self.marginColor = color
    self.borderColor = color
    self.paddingColor = color

  def fitRect(self, rect: Rect) -> Rect:
    """Calculate the required size of the box model to fit the given rect.
    """
    out = rect + self.marginShape
    out += self.borderShape
    out += self.paddingShape
    return out

  def fitSize(self, size: Size) -> Size:
    """Calculate the required size of the box model to fit the given size.
    """
    if TYPE_CHECKING:
      assert isinstance(self.marginShape, Margin)
      assert isinstance(self.borderShape, Margin)
      assert isinstance(self.paddingShape, Margin)
    out = size + self.marginShape
    out += self.borderShape
    out += self.paddingShape
    return out
