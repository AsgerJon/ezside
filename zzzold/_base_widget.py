"""BaseWidget provides a common base class for all widgets in the
application."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QPoint, QMargins
from PySide6.QtGui import QColor
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget
from icecream import ic
from vistutils.parse import maybe

from ezside.core import parseBrush, SolidFill, AlignVCenter, AlignHCenter
from ezside.core import parsePen, SolidLine, parseParent, parseStyleId
from ezside.core import parseFont, Normal, NoPolicy
from ezside.app import EZObject

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class BaseWidget(QWidget, EZObject):
  """BaseWidget provides a common base class for all widgets in the
  application."""

  @classmethod
  def getFallbackSettings(cls, **kwargs) -> dict[str, Any]:
    """This function provides fallback settings. Subclasses that require
    settings other than these should provide them by reimplementing this
    method. This method will then add them using the __init_subclass__
    protocol. Please note, that subclasses cannot replace the fallback
    settings provided here. """
    White = QColor(255, 255, 255, 255)
    Black = QColor(0, 0, 0, 255)
    return {
      'horizontalAlignment': AlignHCenter,
      'verticalAlignment'  : AlignVCenter,
      'margins'            : QMargins(0, 0, 0, 0),
      'borders'            : QMargins(0, 0, 0, 0),
      'paddings'           : QMargins(0, 0, 0, 0),
      'radius'             : QPoint(0, 0),
      'backgroundBrush'    : parseBrush(White, SolidFill),
      'borderBrush'        : parseBrush(Black, SolidFill),
      'borderPen'          : parsePen(Black, 1, SolidLine),
      'textPen'            : parsePen(Black, 1, SolidLine),
      'font'               : parseFont('Montserrat', 12, Normal),
      'focusPolicy'        : NoPolicy,
    }

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the BaseWidget.
    Please note that BaseWidget will look for keyword arguments to set the
    styleId, at the following names:
      - 'styleId'
      - 'style'
      - 'id'
    The default styleId is 'normal'. """
    parent = parseParent(*args, **kwargs)
    QWidget.__init__(self, parent)
    self.__style_id__ = parseStyleId(*args, **kwargs)

  @Slot()
  def aboutToClose(self) -> None:
    """The aboutToClose method is called just before the widget is closed.
    Subclasses that implement threads or timers should implement a
    graceful shutdown here. """

  def getId(self) -> str:
    """Getter-function for the style ID."""
    return maybe(self.__style_id__, 'normal')

  def initUi(self) -> None:
    """The initUi method initializes the user interface."""

  def initSignalSlot(self) -> None:
    """The initSignalSlot method connects signals and slots."""

  def customPaint(self, painter) -> None:
    """The customPaint method paints the custom content of the widget."""
