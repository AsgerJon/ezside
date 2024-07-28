"""This file provides various convenient font related functions."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont
from worktoy.parse import maybe


def parseFont(*args) -> QFont:
  """The 'parseFont' function returns a QFont instance based on the
  arguments"""
  family, size, weight = None, None, None
  for arg in args:
    if isinstance(arg, str) and family is None:
      family = arg
    elif isinstance(arg, int) and size is None:
      size = arg
    elif isinstance(arg, int) and weight is None:
      weight = arg
    if weight is not None and size is not None and family is not None:
      break
  else:
    family = maybe(family, 'Courier')
    size = maybe(size, 12)
    weight = maybe(weight, QFont.Normal)
  out = QFont()
  out.setFamily(family)
  out.setPointSize(size)
  out.setWeight(weight)
  return out
