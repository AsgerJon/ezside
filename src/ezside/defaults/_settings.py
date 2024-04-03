"""The defaults class provides a base class for all defaults classes in the
application. During development values are placed in the class body. Once
deployed values that should be configurable by the user are loaded from a
file. When the users make defaults changes, this file is updated."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

from PySide6.QtCore import QMargins
from PySide6.QtGui import QFont, QColor, QPainter, QPen
from ezside.core import DashLine


class Settings:
  """The defaults class provides a base class for all defaults classes in the
  application. During development values are placed in the class body. Once
  deployed values that should be configurable by the user are loaded from a
  file. When the users make defaults changes, this file is updated."""

  @staticmethod
  def getButtonStyle() -> str:
    """Get the button style."""
    cornerRadius = 4
    borderWidth = 2
    borderColor = '#000000'
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, '_button_style.qss')) as file:
      print(file.read())
      return file.read()

  labelBackgroundColor = (255, 255, 192, 255)
  labelBorderColor = (0, 0, 0, 255)
  labelTextColor = (0, 0, 0, 255)
  labelBorderWidth = 2
  labelTopMargin = 2
  labelBottomMargin = 2
  labelLeftMargin = 4
  labelRightMargin = 4

  fontFamily = 'Montserrat'
  buttonFontSize = 12
  labelFontSize = 14
  headerFontSize = 16

  numPoints = 256

  spacerVisibility = True

  horizontalSeperatorColor = (192, 225, 255, 255)
  horizontalSeperatorWidth = 2
  horizontalSeperatorStyle = DashLine
  verticalSeperatorColor = (192, 225, 255, 255)
  verticalSeperatorWidth = 2
  verticalSeperatorStyle = DashLine

  layoutMargins = dict(left=2, top=2, right=2, bottom=2)

  @classmethod
  def getLayoutMargins(cls) -> QMargins:
    """Get the layout margins."""
    return QMargins(cls.layoutMargins['left'],
                    cls.layoutMargins['top'],
                    cls.layoutMargins['right'],
                    cls.layoutMargins['bottom'], )

  @classmethod
  def applyHorizontalSeperator(cls, painter: QPainter) -> QPainter:
    """Apply the horizontal seperator."""
    color = QColor(*cls.horizontalSeperatorColor)
    pen = QPen()
    pen.setColor(color)
    pen.setWidth(cls.horizontalSeperatorWidth)
    pen.setStyle(cls.horizontalSeperatorStyle)
    painter.setPen(pen)
    return painter

  @classmethod
  def applyVerticalSeperator(cls, painter: QPainter) -> QPainter:
    """Apply the vertical seperator."""
    color = QColor(*cls.verticalSeperatorColor)
    pen = QPen()
    pen.setColor(color)
    pen.setWidth(cls.verticalSeperatorWidth)
    pen.setStyle(cls.verticalSeperatorStyle)
    painter.setPen(pen)
    return painter

  @classmethod
  def getButtonFont(cls) -> QFont:
    """Get the button font."""
    font = QFont()
    font.setFamily(cls.fontFamily)
    font.setPointSize(cls.buttonFontSize)
    return font

  @classmethod
  def getLabelMargins(cls, ) -> QMargins:
    """Returns the margins of the label."""
    return QMargins(cls.labelLeftMargin,
                    cls.labelTopMargin,
                    cls.labelRightMargin,
                    cls.labelBottomMargin, )

  @classmethod
  def getHeaderFont(cls) -> QFont:
    """Get the header font."""
    font = QFont()
    font.setFamily(cls.fontFamily)
    font.setPointSize(cls.headerFontSize)
    return font

  @classmethod
  def getLabelBackgroundColor(cls) -> QColor:
    """Get the label background color."""
    return QColor(*cls.labelBackgroundColor)

  @classmethod
  def getLabelBorderColor(cls) -> QColor:
    """Get the label border color."""
    return QColor(*cls.labelBorderColor)

  @classmethod
  def getLabelTextColor(cls) -> QColor:
    """Get the label text color."""
    return QColor(*cls.labelTextColor)
