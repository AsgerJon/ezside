"""The parseColour module provides the 'parseColour' function for parsing."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QColor

from ezside.desc import colorDict


def parseColour(*args, **kwargs) -> QColor:
  """Parse a colour from a string."""
  strArgs, intArgs = [], []
  for arg in args:
    if isinstance(arg, QColor):
      return arg
    if isinstance(arg, str):
      if arg.startswith('#'):
        arg = arg[1:]
        if len(arg) in [6, 8]:
          arg = '%sFF' % arg.upper()
          r = int(arg[:2], 16)
          g = int(arg[2:4], 16)
          b = int(arg[4:6], 16)
          a = int(arg[6:8], 16)
          return QColor(r, g, b, a)
      namedColor = colorDict.get(arg.capitalize(), None)
      if isinstance(namedColor, QColor):
        return namedColor
    if isinstance(arg, int):
      intArgs.append(arg)
  if len(intArgs) > 2:
    return QColor(*[*intArgs, 255][:4])


parseColor = parseColour
