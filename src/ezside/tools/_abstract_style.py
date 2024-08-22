"""AbstractStyle provides a base class for style settings. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Self, TypeAlias, Union

from PySide6.QtCore import QMargins, QMarginsF
from PySide6.QtGui import QColor
from worktoy.parse import maybe
from worktoy.meta import BaseObject

Margins: TypeAlias = tuple[float, float, float, float]
Color: TypeAlias = tuple[int, int, int, int]
Data: TypeAlias = dict[str, Union[str, dict]]


class AbstractStyle(BaseObject):
  """AbstractStyle provides a base class for style settings. """

  @classmethod
  @abstractmethod
  def load(cls, data: dict[str, str]) -> Self:
    """Load the style data from the given dictionary into a new instance. """

  @classmethod
  def _parseColor(cls, *args, **kwargs) -> Color:
    """Parses the color from the given arguments. """
    intArgs = []
    if kwargs:
      if not kwargs.get('_recursion', False):
        red = kwargs.get('red', None)
        r = kwargs.get('r', None)
        R = maybe(red, r, 0)
        green = kwargs.get('green', 0)
        g = kwargs.get('g', 0)
        G = maybe(green, g, 0)
        blue = kwargs.get('blue', 0)
        b = kwargs.get('b', 0)
        B = maybe(blue, b, 0)
        alpha = kwargs.get('alpha', 255)
        a = kwargs.get('a', 255)
        A = maybe(alpha, a, 255)
        return (R, G, B, A)
    for arg in args:
      if isinstance(arg, str):
        if arg.isnumeric():
          intArgs.append(int(arg))
        elif arg.startswith('#'):
          raise NotImplementedError
        else:
          e = """Received invalid color string: %s!"""
          raise ValueError(e % arg)
      elif isinstance(arg, int):
        intArgs.append(arg)
      elif isinstance(arg, float):
        if arg < 1:
          intArgs.append(int(arg * 255))
        elif arg.is_integer():
          intArgs.append(int(arg))
        else:
          e = """Received invalid float color value: %s!"""
          raise ValueError(e % str(arg))
      elif isinstance(arg, QColor):
        return (arg.red(), arg.green(), arg.blue(), arg.alpha())
      elif isinstance(arg, dict):
        return cls._parseColor(**arg)
      else:
        e = """Received invalid color value: %s!"""
        raise ValueError(e % str(arg))

  @classmethod
  def _parseMargins(cls, *args, **kwargs) -> Margins:
    """Parse the margins from the given arguments."""
    floatArgs = []
    if kwargs:
      if not kwargs.get('_recursion', False):
        left = kwargs.get('left', 0)
        top = kwargs.get('top', 0)
        right = kwargs.get('right', 0)
        bottom = kwargs.get('bottom', 0)
        return (left, top, right, bottom)
    for arg in args:
      if isinstance(arg, str):
        if arg.isnumeric():
          floatArgs.append(float(arg))
        else:
          e = """Received invalid margin string: %s!"""
          raise ValueError(e % arg)
      elif isinstance(arg, float):
        floatArgs.append(arg)
      elif isinstance(arg, int):
        floatArgs.append(float(arg))
      elif isinstance(arg, QMargins):
        return arg.left(), arg.top(), arg.right(), arg.bottom()
      elif isinstance(arg, QMarginsF):
        if kwargs.get('_recursion', False):
          raise RecursionError
        return cls._parseMargins(QMarginsF.toMargins(arg), _recursion=True)
      elif isinstance(arg, dict):
        return cls._parseMargins(**arg)
    if not floatArgs:
      return (0, 0, 0, 0)
    if len(floatArgs) == 1:
      return (floatArgs[0], floatArgs[0], floatArgs[0], floatArgs[0])
    if len(floatArgs) == 2:
      return (floatArgs[0], floatArgs[1], floatArgs[0], floatArgs[1])
    if len(floatArgs) == 3:
      return (floatArgs[0], floatArgs[1], floatArgs[2], floatArgs[1])
    if len(floatArgs) == 4:
      return (floatArgs[0], floatArgs[1], floatArgs[2], floatArgs[3])
    e = """Received too many arguments for margins: %s!"""
    raise ValueError(e % str(args))
