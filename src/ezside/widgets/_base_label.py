"""BaseLabel provides a widget holding a label"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont
from attribox import AttriBox

from ezside.widgets import BaseWidget


class BaseLabel(BaseWidget):
  """BaseLabel provides a widget holding a label"""

  text = AttriBox[str]()
  font = AttriBox[QFont]()
  styleId = AttriBox[str]()
