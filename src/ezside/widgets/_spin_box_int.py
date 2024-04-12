"""SpinBoxInt provides an integer valued spin box widget."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QSpinBox
from attribox import AttriBox

from ezside.widgets import SpinBoxFloat


class SpinBoxInt(SpinBoxFloat):
  """SpinBoxInt provides an integer valued spin box widget."""

  inner = AttriBox[QSpinBox]()
