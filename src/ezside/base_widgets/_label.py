"""Label provides a property driven alternative to QLabel. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Any

from PySide6.QtCore import QRectF, QSizeF, QRect
from PySide6.QtGui import QPainter, QPaintEvent
from icecream import ic
from worktoy.desc import Field, AttriBox
from worktoy.text import typeMsg

from ezside.base_widgets import BoxWidget
from ezside.tools import FontStyle

ic.configureOutput(includeContext=True)

Rect: TypeAlias = Union[QRect, QRectF]


class Label(BoxWidget):
  """Label provides a property driven alternative to QLabel. """

  __fallback_text__ = 'LABEL'
  __font_style__ = None

  fontStyle = Field()

  text = AttriBox[str]()

  @fontStyle.GET
  def _getFontStyle(self) -> Any:
    """Getter-function for the fontStyle."""
    if isinstance(self.__font_style__, FontStyle):
      return self.__font_style__
    if self.__font_style__ is None:
      e = """The fontStyle has not been set. """
      raise AttributeError(e)
    e = typeMsg('fontStyle', self.__font_style__, FontStyle)
    raise TypeError(e)

  def requiredSize(self) -> QSizeF:
    """Returns the size required to display the current text with the
    current font."""
    return self.fontStyle.boundSize(self.text)

  def paintMeLike(self,
                  rect: Rect,
                  painter: QPainter,
                  event: QPaintEvent) -> Any:
    """Paints the label with the current text and font."""
    rect, painter, event = BoxWidget.paintMeLike(self, rect, painter, event)
    textRect = self.fontStyle.boundRect(self.text)
    alignedRect = self.align.fitRect(textRect, rect)
    painter = self.fontStyle @ painter
    painter.drawText(alignedRect, self.align.qt, self.text)
    return alignedRect, painter, event

  def __init__(self, *args, **kwargs) -> None:
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
    BoxWidget.__init__(self, *unusedArgs, **kwargs)
    self.__font_style__ = self.app.loadFont(self.styleId)
