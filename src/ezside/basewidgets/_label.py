"""Label provides a property driven alternative to QLabel. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Any

from PySide6.QtCore import QSize, QRectF, QSizeF, QPointF, QMarginsF, QRect
from PySide6.QtGui import QPainter, QPaintEvent
from icecream import ic
from worktoy.desc import AttriBox

from ezside.tools import Font, FontFamily, FontCap, emptyPen
from ezside.basewidgets import BoxWidget

ic.configureOutput(includeContext=True)

Rect: TypeAlias = Union[QRect, QRectF]


class Label(BoxWidget):
  """Label provides a property driven alternative to QLabel. """

  __fallback_text__ = 'LABEL'
  __parsed_object__ = None

  textFont = AttriBox[Font](16, FontFamily.MONTSERRAT, FontCap.MIX)
  text = AttriBox[str]()

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
    rect, painter, event = BoxWidget.paintMeLike(self, rect, painter, event)
    textRect = self.textFont.boundRect(self.text)
    targetRect = rect - self.allMargins
    alignRect = self.textFont.align.fitRectF(textRect, targetRect)
    self.textFont @= painter
    ic(self.textFont)
    painter.drawText(alignRect, self.text)
    return alignRect, painter, event

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
    self.paddings = QMarginsF(1, 1, 1, 1, )
    self.borders = QMarginsF(2, 2, 2, 2, )
    self.margins = QMarginsF(2, 2, 2, 2, )
