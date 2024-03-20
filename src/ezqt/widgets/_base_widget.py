"""BaseWidget provides a base class for the widgets. Using AttriBox they
provide brushes, pens and fonts as attributes. These widgets are not meant
for composite widgets directly but instead for the constituents. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget
from attribox import AttriBox
from icecream import ic

from ezqt.core import parseParent, NoWrap, Center, Pen, Font, Brush
from ezqt.core import BevelJoin, FlatCap, SolidLine, SolidFill, DashLine
from ezqt.core import DotLine, DashDot

ic.configureOutput(includeContext=True, )


class BaseWidget(QWidget):
  """BaseWidget provides a base class for the widgets. Using AttriBox they
  provide brushes, pens and fonts as attributes. These widgets are not meant
  for composite widgets directly but instead for the constituents. """

  baseSize = AttriBox[QSize](32, 32)
  solidBrush = AttriBox[Brush](SolidFill)
  emptyBrush = AttriBox[Brush](QColor(0, 0, 0, 0))
  solidLine = AttriBox[Pen](SolidLine)
  dashedLine = AttriBox[Pen](DashLine)
  dottedLine = AttriBox[Pen](DotLine)
  dashDotLine = AttriBox[Pen](DashDot)
  fontLine = AttriBox[Pen](SolidLine, 1, FlatCap, BevelJoin)
  emptyLine = AttriBox[Pen](Qt.PenStyle.NoPen)
  defaultFont = AttriBox[Font]('Montserrat', 16, )

  def __init__(self, *args, **kwargs) -> None:
    """BaseWidget provides a base class for the widgets. Using AttriBox they
    provide brushes, pens and fonts as attributes. These widgets are not
    meant for composite widgets directly but instead for the components."""
    # ic('%s' % self.__class__.__name__)
    parent = parseParent(*args, **kwargs)
    QWidget.__init__(self, parent)
    self.setMinimumSize(QSize(64, 64))
    # self.initUi()

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

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(self.baseSize)
    self.connectActions()

  def connectActions(self) -> None:
    """The connectActions method connects the actions to the signals."""
