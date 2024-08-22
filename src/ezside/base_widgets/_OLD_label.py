"""Label provides a property driven alternative to QLabel. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Any

from PySide6.QtCore import QRectF, QSizeF, QPointF, QMarginsF, QRect
from PySide6.QtGui import QPainter, QPaintEvent, QColor
from icecream import ic
from worktoy.desc import AttriBox

from ezside.tools import Font, FontFamily, FontCap, LoadResource
from ezside.base_widgets import BoxWidget, AbstractBoxStyle

ic.configureOutput(includeContext=True)

Rect: TypeAlias = Union[QRect, QRectF]


class Label(BoxWidget):
  """Label provides a property driven alternative to QLabel. """

  __fallback_text__ = 'LABEL'
  __resource_loader__ = None
  __style_data__ = None

  def getStyle(self, **kwargs) -> AbstractBoxStyle:
    """Returns the style object for the widget."""
    if self.__style_data__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      labelStyle = self.__resource_loader__['label_style.json']

  def requiredSize(self) -> QSizeF:
    """Returns the size required to display the current text with the
    current font."""
    rect = self.textFont.boundRect(self.text)
    return (rect + self.allMargins).size()

  def paintMeLike(self,
                  rect: Rect,
                  painter: QPainter,
                  event: QPaintEvent) -> Any:
    """Paints the label with the current text and font."""

  def __init__(self, *args) -> None:
    unusedArgs = []
    tempArgs = [*args, ]
    while tempArgs:
      arg = tempArgs.pop(0)
      if isinstance(arg, str):
        self.text = arg
        unusedArgs.extend(tempArgs)
        break
    else:
      self.text = self.__fallback_text__
    BoxWidget.__init__(self, *unusedArgs)
    self.__resource_loader__ = LoadResource('styles')
