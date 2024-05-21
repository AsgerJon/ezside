"""AbstractSpacer provides the base class for all spacers and separators.
"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from PySide6.QtCore import QPoint, QMargins
from PySide6.QtGui import QColor

from ezside.core import Fixed, Expand, AlignHCenter, AlignVCenter, DashLine
from ezside.core import parseBrush, SolidFill, SolidLine, parsePen
from ezside.widgets import CanvasWidget
from moreattribox import Flag


class AbstractSpacer(CanvasWidget):
  """AbstractSpacer provides the base class for all spacers and
  separators."""

  @abstractmethod
  def _getHorizontalFlag(self) -> Flag:
    """Returns the horizontal flag. True indicates that the spacer should
    occupy horizontal space."""

  @abstractmethod
  def _getVerticalFlag(self) -> Flag:
    """Returns the vertical flag. True indicates that the spacer should
    occupy vertical space."""

  def initUi(self, ) -> None:
    """Initializes the UI."""
    hPol = Expand if self._getHorizontalFlag() else Fixed
    vPol = Expand if self._getVerticalFlag() else Fixed
    self.setSizePolicy(hPol, vPol)

  @classmethod
  def getFallbackSettings(cls) -> dict[str, Any]:
    """Fallback styles"""
    separatorPen = parsePen(QColor(0, 0, 0, 255), 2, DashLine)
    return {
      'margins'        : QMargins(0, 0, 0, 0, ),
      'borders'        : QMargins(0, 0, 0, 0, ),
      'paddings'       : QMargins(0, 0, 0, 0, ),
      'borderBrush'    : parseBrush(QColor(0, 0, 0, 0), SolidFill, ),
      'backgroundBrush': parseBrush(QColor(0, 0, 0, 0), SolidFill, ),
      'radius'         : QPoint(0, 0),
      'vAlign'         : AlignVCenter,
      'hAlign'         : AlignHCenter,
      'separatorPen'   : separatorPen,
    }
  #
  # def getDefaultStyles(self, name: str) -> Any:
  #   """The defaultStyles method provides the default values for the
  #   styles."""
  #
  #   visibleBrush = parseBrush(QColor(255, 255, 0, 255), SolidFill)
  #   hiddenBrush = parseBrush(QColor(255, 255, 0, 0), SolidFill)
  #   visiblePen = parsePen(QColor(0, 0, 0, 255), 1, SolidLine)
  #   hiddenPen = parsePen(QColor(0, 0, 0, 0), 1, SolidLine)
  #
  #   if self.getId() == 'visible':
  #     return {
  #       'backgroundBrush': visibleBrush,
  #       'borderBrush'    : visiblePen,
  #     }
  #
  #   if self.getId() in ['hidden', 'normal']:
  #     return {
  #       'backgroundBrush': hiddenBrush,
  #       'borderBrush'    : hiddenPen,
  #     }
