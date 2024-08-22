"""BoxStyle provides settings for widgets implementing the box model. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TypeAlias, Union

from PySide6.QtCore import QMarginsF, Qt
from PySide6.QtGui import QColor, QBrush
from icecream import ic

from worktoy.desc import Field, AttriBox, DEFAULT
from ezside.style import Align, AbstractStyle

ic.configureOutput(includeContext=True)

Margins: TypeAlias = tuple[float, float, float, float]
Color: TypeAlias = tuple[int, int, int, int]
Data: TypeAlias = dict[str, Union[str, dict]]


class BoxStyle(AbstractStyle):
  """BoxStyle provides settings for widgets implementing the box model. """

  marginsLeft = AttriBox[float](0)
  marginsTop = AttriBox[float](0)
  marginsRight = AttriBox[float](0)
  marginsBottom = AttriBox[float](0)
  marginsRed = AttriBox[int](0)
  marginsGreen = AttriBox[int](0)
  marginsBlue = AttriBox[int](0)
  marginsAlpha = AttriBox[int](0)

  bordersLeft = AttriBox[float](0)
  bordersTop = AttriBox[float](0)
  bordersRight = AttriBox[float](0)
  bordersBottom = AttriBox[float](0)
  bordersRed = AttriBox[int](0)
  bordersGreen = AttriBox[int](0)
  bordersBlue = AttriBox[int](0)
  bordersAlpha = AttriBox[int](255)

  paddingsLeft = AttriBox[float](0)
  paddingsTop = AttriBox[float](0)
  paddingsRight = AttriBox[float](0)
  paddingsBottom = AttriBox[float](0)
  paddingsRed = AttriBox[int](255)
  paddingsGreen = AttriBox[int](255)
  paddingsBlue = AttriBox[int](255)
  paddingsAlpha = AttriBox[int](255)

  align = AttriBox[Align](DEFAULT(Align.CENTER))

  margins = Field()
  borders = Field()
  paddings = Field()
  marginsColor = Field()
  bordersColor = Field()
  paddingsColor = Field()
  marginsBrush = Field()
  bordersBrush = Field()
  paddingsBrush = Field()

  @classmethod
  def load(cls, data: Data) -> BoxStyle:
    """Load the style data from the given dictionary into a new instance. """
    newBox = cls()
    newBox.margins = data.get('margins', {})
    newBox.borders = data.get('borders', {})
    newBox.paddings = data.get('paddings', {})
    newBox.marginsColor = data.get('marginsColor', {})
    newBox.bordersColor = data.get('bordersColor', {})
    newBox.paddingsColor = data.get('paddingsColor', {})
    newBox.align = data.get('align', Align.CENTER)
    return newBox

  @margins.GET
  def _getMargins(self, **kwargs) -> QMarginsF:
    """Getter-function for the margins. """
    return QMarginsF(self.marginsLeft,
                     self.marginsTop,
                     self.marginsRight,
                     self.marginsBottom)

  @margins.SET
  def _setMargins(self, value: Any) -> None:
    """Setter-function for the margins. """
    left, top, right, bottom = self._parseMargins(value)
    self.marginsLeft = left
    self.marginsTop = top
    self.marginsRight = right
    self.marginsBottom = bottom

  @borders.GET
  def _getBorders(self, **kwargs) -> QMarginsF:
    """Getter-function for the borders. """
    return QMarginsF(self.bordersLeft,
                     self.bordersTop,
                     self.bordersRight,
                     self.bordersBottom)

  @borders.SET
  def _setBorders(self, value: Any) -> None:
    """Setter-function for the borders. """
    left, top, right, bottom = self._parseMargins(value)
    self.bordersLeft = left
    self.bordersTop = top
    self.bordersRight = right
    self.bordersBottom = bottom

  @paddings.GET
  def _getPaddings(self, **kwargs) -> QMarginsF:
    """Getter-function for the paddings. """
    return QMarginsF(self.paddingsLeft,
                     self.paddingsTop,
                     self.paddingsRight,
                     self.paddingsBottom)

  @paddings.SET
  def _setPaddings(self, value: Any) -> None:
    """Setter-function for the paddings. """
    left, top, right, bottom = self._parseMargins(value)
    self.paddingsLeft = left
    self.paddingsTop = top
    self.paddingsRight = right
    self.paddingsBottom = bottom

  @marginsColor.GET
  def _getMarginsColor(self, **kwargs) -> QColor:
    """Getter-function for the marginsColor. """
    return QColor(self.marginsRed,
                  self.marginsGreen,
                  self.marginsBlue,
                  self.marginsAlpha)

  @marginsColor.SET
  def _setMarginsColor(self, value: Any) -> None:
    """Setter-function for the marginsColor. """
    red, green, blue, alpha = self._parseColor(value)
    self.marginsRed = red
    self.marginsGreen = green
    self.marginsBlue = blue
    self.marginsAlpha = alpha

  @marginsBrush.GET
  def _getMarginsBrush(self) -> QBrush:
    """Getter-function for the marginsBrush."""
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    brush.setColor(self.marginsColor)
    return brush

  @bordersColor.GET
  def _getBordersColor(self, **kwargs) -> QColor:
    """Getter-function for the bordersColor. """
    return QColor(self.bordersRed,
                  self.bordersGreen,
                  self.bordersBlue,
                  self.bordersAlpha)

  @bordersColor.SET
  def _setBordersColor(self, value: Any) -> None:
    """Setter-function for the bordersColor. """
    red, green, blue, alpha = self._parseColor(value)
    self.bordersRed = red
    self.bordersGreen = green
    self.bordersBlue = blue
    self.bordersAlpha = alpha

  @bordersBrush.GET
  def _getBordersBrush(self) -> QBrush:
    """Getter-function for the bordersBrush."""
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    brush.setColor(self.bordersColor)
    return brush

  @paddingsColor.GET
  def _getPaddingsColor(self, **kwargs) -> QColor:
    """Getter-function for the paddingsColor. """
    return QColor(self.paddingsRed,
                  self.paddingsGreen,
                  self.paddingsBlue,
                  self.paddingsAlpha)

  @paddingsColor.SET
  def _setPaddingsColor(self, value: Any) -> None:
    """Setter-function for the paddingsColor. """
    red, green, blue, alpha = self._parseColor(value)
    self.paddingsRed = red
    self.paddingsGreen = green
    self.paddingsBlue = blue
    self.paddingsAlpha = alpha

  @paddingsBrush.GET
  def _getPaddingsBrush(self) -> QBrush:
    """Getter-function for the paddingsBrush."""
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    brush.setColor(self.paddingsColor)
    return brush
