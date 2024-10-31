"""The parseParent function receives positional arguments and returns the
first argument of type 'QObject' or None, followed by a list of the
remaining arguments. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QObject


def parseParent(*args: object) -> tuple[object, list[object]]:
  """The parseParent function receives positional arguments and returns the
  first argument of type 'QObject' or None, followed by a list of the
  remaining arguments. """
  otherArgs = []
  posArgs = [*args, ]
  while posArgs:
    arg = posArgs.pop(0)
    if isinstance(arg, QObject):
      return (arg, [*otherArgs, *posArgs, ])
    otherArgs.append(arg)
  return (None, otherArgs)
