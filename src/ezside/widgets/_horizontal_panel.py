"""HorizontalPanel provides the same as VerticalPanel, but in a horizontal
direction."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QColor
from vistutils.parse import maybe

from ezside.core import Fixed, Expand, LawnGreen
from ezside.widgets import FilledRect


class HorizontalPanel(FilledRect):
  """HorizontalPanel provides the same as VerticalPanel, but in a horizontal
  direction."""

  def __init__(self, *args, **kwargs) -> None:
    colorArgs, intArgs, width = [], [], None
    color = None
    for arg in args:
      if isinstance(arg, int):
        intArgs.append(arg)
      elif isinstance(arg, QColor):
        colorArgs.append(arg)
    if colorArgs:
      color = None
    if color is None:
      if len(intArgs) == 3:
        color = QColor(*intArgs, 255)
      elif len(intArgs) > 3:
        color = QColor(*intArgs[:4])
    color = maybe(color, LawnGreen)
    self.fillColor.setRed(color.red())
    self.fillColor.setGreen(color.green())
    self.fillColor.setBlue(color.blue())
    FilledRect.__init__(self, *args, **kwargs)
    self.setFixedHeight(32)
    self.setMaximumWidth(1024)
    self.setSizePolicy(Fixed, Expand)
