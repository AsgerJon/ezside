"""The DragSwitch uses the slider widget to implement a two state widget.
To change the state, the user must grab and drag the handle to the
opposite side."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from attribox import AttriBox

from ezside.core import Orientation
from ezside.widgets import CanvasWidget, BaseWidget, LayoutDescriptor


class DragSwitch(CanvasWidget):
  """The DragSwitch uses the slider widget to implement a two state widget.
  To change the state, the user must grab and drag the handle to the
  opposite side."""

  orientation = Orientation()
  baseLayout = LayoutDescriptor()
  baseWidget = AttriBox[BaseWidget]()
