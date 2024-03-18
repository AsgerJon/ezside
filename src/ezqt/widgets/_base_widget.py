"""BaseWidget provides a base class for the widgets. Using AttriBox they
provide brushes, pens and fonts as attributes. These widgets are not meant
for composite widgets directly but instead for the constituents. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QBrush, QPen, QColor, QFont, QPainter
from PySide6.QtWidgets import QWidget

from attribox import AttriBox
from ezqt.core import parseParent, NoWrap, Center, Pen, Font, Brush


class BaseWidget(QWidget):
  """BaseWidget provides a base class for the widgets. Using AttriBox they
  provide brushes, pens and fonts as attributes. These widgets are not meant
  for composite widgets directly but instead for the constituents. """

  solidBrush = AttriBox[Brush](Qt.BrushStyle.SolidPattern)
  emptyBrush = AttriBox[Brush](QColor(0, 0, 0, 0))
  solidLine = AttriBox[Pen](Qt.PenStyle.SolidLine)
  dashedLine = AttriBox[Pen](Qt.PenStyle.DashLine)
  dottedLine = AttriBox[Pen](Qt.PenStyle.DotLine)
  dashDotLine = AttriBox[Pen](Qt.PenStyle.DashDotLine)
  fontLine = AttriBox[Pen](Qt.PenStyle.SolidLine, 1, Qt.PenCapStyle.FlatCap,
                           Qt.PenJoinStyle.BevelJoin)
  emptyLine = AttriBox[Pen](Qt.PenStyle.NoPen)
  defaultFont = AttriBox[Font]('Montserrat', 16, )

  def __init__(self, *args, **kwargs) -> None:
    """BaseWidget provides a base class for the widgets. Using AttriBox they
    provide brushes, pens and fonts as attributes. These widgets are not
    meant for composite widgets directly but instead for the components."""
    parent = parseParent(*args, **kwargs)
    QWidget.__init__(self, parent)
    self.setMinimumSize(QSize(32, 32))

  def painterPrint(self, painter: QPainter) -> QPainter:
    """The painterPrint method adjusts the given painter to print text."""
    painter.setPen(self.fontLine)
    painter.setFont(self.defaultFont)
    return painter

  def painterFill(self, painter: QPainter) -> QPainter:
    """The painterFill method adjusts the given painter to fill shapes."""
    painter.setPen(self.emptyLine)
    painter.setBrush(self.solidBrush)
    return painter

  def painterLine(self, painter: QPainter) -> QPainter:
    """The painterLine method adjusts the given painter to draw lines."""
    painter.setPen(self.solidLine)
    painter.setBrush(self.emptyBrush)
    return painter

  def boundSize(self, text: str, ) -> None:
    """The boundSize method returns the bounding rectangle of the given
    text."""
    rect, flags = self.geometry(), NoWrap | Center
    self.defaultFont.metrics().boundingRect(flags, flags, text)
    return rect.size()
