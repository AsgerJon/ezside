"""VerticalPanel provide a filled panel of fixed width spanning the height
available."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QColor
from vistutils.parse import maybe

from ezqt.core import Fixed, Expand, LawnGreen
from ezqt.widgets import FilledRect


class VerticalPanel(FilledRect):
  """VerticalPanel provide a filled panel of fixed width spanning the height
  available."""

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
    self.setFixedWidth(32)
    self.setMaximumHeight(1024)
    self.setSizePolicy(Expand, Fixed, )
