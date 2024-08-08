"""Label provides a property driven alternative to QLabel. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize, QRectF, QSizeF, QPointF, QMarginsF
from PySide6.QtGui import QPainter
from icecream import ic
from worktoy.desc import AttriBox

from ezside.tools import Font, FontFamily, FontCap, emptyPen
from ezside.basewidgets import BoxWidget

ic.configureOutput(includeContext=True)


class Label(BoxWidget):
  """Label provides a property driven alternative to QLabel. """

  margins: QMarginsF
  borders: QMarginsF
  paddings: QMarginsF

  __fallback_text__ = 'LABEL'
  __parsed_object__ = None

  textFont = AttriBox[Font](16, FontFamily.MONTSERRAT, FontCap.MIX)
  text = AttriBox[str]()

  def requiredSize(self) -> QSizeF:
    """The required size to show the current text with the current font."""
    return self.requiredRect().size()

  def requiredRect(self) -> QRectF:
    """The required rectangle to bound the current text."""
    rect = self.textFont.boundRect(self.text) + self.allMargins
    size = rect.size()
    return QRectF(QPointF(0, 0), size)

  def minimumSizeHint(self) -> QSize:
    """The minimum size hint to show the current text with the current
    font."""
    return QSize(0, 0)

  def paintMeLike(self, rect: QRectF, painter: QPainter) -> None:
    """Paints the label with the current text and font."""
    viewRect = rect
    center = viewRect.center()
    marginRect = QRectF.marginsRemoved(viewRect, self.margins)
    borderRect = QRectF.marginsRemoved(marginRect, self.borders)
    paddedRect = QRectF.marginsRemoved(borderRect, self.paddings)
    marginRect.moveCenter(center)
    borderRect.moveCenter(center)
    paddedRect.moveCenter(center)
    painter.setPen(emptyPen())
    painter.setBrush(self.borderBrush)
    painter.drawRect(marginRect)
    painter.setBrush(self.backgroundBrush)
    painter.drawRect(borderRect)
    painter.setPen(self.textFont.asQPen)
    painter.setFont(self.textFont.asQFont)
    textRect = self.textFont.align.fitRectF(self.requiredRect(), paddedRect)
    painter.drawText(textRect, self.textFont.align.qt, self.text)

  def __init__(self, *args) -> None:
    BoxWidget.__init__(self)
    for arg in args:
      if isinstance(arg, str):
        self.text = arg
        break
    else:
      self.text = self.__fallback_text__
    self.paddings = QMarginsF(8, 1, 8, 1)
    self.borders = QMarginsF(2, 2, 2, 2, )
    self.margins = QMarginsF(2, 2, 2, 2, )
