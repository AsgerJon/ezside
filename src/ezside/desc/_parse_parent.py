"""The 'parseParent' parses arguments for parent widget."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import QWidget


def parseParent(*args, **kwargs) -> Optional[QWidget]:
  """The 'parseParent' parses arguments for parent widget."""
  for arg in args:
    if isinstance(arg, QWidget):
      return arg
