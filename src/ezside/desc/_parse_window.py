"""The 'parseWindow' function resolves the positional and keyword arguments
find the class that is a subclass of QMainWindow."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import QMainWindow


def parseWindow(*args, **kwargs) -> tuple[Optional[type], list, dict]:
  """The 'parseWindow' function resolves the positional and keyword arguments
  find the class that is a subclass of QMainWindow."""

  windowKeys = ['window', 'mainWindow', 'main', ]
  for key in windowKeys:
    if key in kwargs:
      val = kwargs[key]
      if isinstance(val, type) and issubclass(val, QMainWindow):
        keyArgs = {k: v for (k, v) in kwargs.items() if k != key}
        return val, [*args, ], keyArgs
      e = f"Expected a subclass of QMainWindow, got {val}!"
      raise TypeError(e)
  else:
    for arg in args:
      if isinstance(arg, type) and issubclass(arg, QMainWindow):
        posArgs = [a for a in args if a != arg]
        return arg, posArgs, {**kwargs, }
    else:
      return None, [*args, ], {**kwargs, }
