"""The 'parseFont' function creates instances of QFont. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont


def parseFont(*args, **kwargs) -> QFont:
  """The 'parseFont' function creates instances of QFont. """
  return QFont(*args)
