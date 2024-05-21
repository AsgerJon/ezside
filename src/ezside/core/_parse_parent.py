"""The parseParent function parses positional arguments and returns the
first instance of QWidget encountered if any."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg


def parseParent(*args, **kwargs) -> Any:
  """The parseParent function parses positional arguments and returns the
  first instance of QWidget encountered if any."""
  parentKeys = stringList("""parent, main, window""")
  parentType = None
  if args:
    if isinstance(args[0], type):
      if issubclass(args[0], QObject):
        parentType = args[0]
  parentType = QWidget if parentType is None else parentType
  parent = None
  parentKey = None
  remainingArgs = []
  for key in parentKeys:
    if key in kwargs:
      val = kwargs.get(key)
      if isinstance(val, parentType):
        parent = val
        parentKey = key
        break
      e = typeMsg('parent', parent, parentType)
      raise TypeError
  else:
    for arg in args:
      if isinstance(arg, parentType):
        parent = arg
        break
    else:
      return None
  if parentKey is None:
    remainingArgs = [arg for arg in args if arg is not parent]
    remainingKwarg = {**kwargs, }
  else:
    remainingArgs = [*args, ]
    remainingKwarg = {k: v for (k, v) in kwargs.items() if k != parentKey}
  return parent
