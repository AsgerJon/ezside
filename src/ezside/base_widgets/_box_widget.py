"""BoxWidget provides a base class for other base widgets that need to
paint on a background that supports the box model."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Any

from PySide6.QtCore import QRect, QRectF, QMarginsF
from PySide6.QtGui import QPainter, QPaintEvent, QColor, QBrush
from icecream import ic
from worktoy.desc import Field
from worktoy.text import typeMsg

from ezside.base_widgets import LayoutWidget
from ezside.tools import emptyPen
from ezside.style import BoxStyle, Align

Rect: TypeAlias = Union[QRect, QRectF]

ic.configureOutput(includeContext=True)


class BoxWidget(LayoutWidget):
  """BoxWidget provides a base class for other base widgets that need to
  paint on a background that supports the box model."""

  __box_style__ = None

  boxStyle = Field()

  margins = Field()
  borders = Field()
  paddings = Field()
  allMargins = Field()
  align = Field()

  paddingColor = Field()
  borderColor = Field()

  borderBrush = Field()
  paddingBrush = Field()

  @boxStyle.GET
  def _getBoxStyle(self) -> BoxStyle:
    """Getter-function for the boxStyle."""
    if isinstance(self.__box_style__, BoxStyle):
      return self.__box_style__
    if self.__box_style__ is None:
      e = """The boxStyle has not been set. """
      raise AttributeError(e)
    e = typeMsg('boxStyle', self.__box_style__, BoxStyle)
    raise TypeError(e)

  @borderBrush.GET
  def _getBorderBrush(self) -> QBrush:
    """Getter-function for the borderBrush."""
    return self.boxStyle.bordersBrush

  @paddingBrush.GET
  def _getPaddingBrush(self) -> QBrush:
    """Getter-function for the paddingBrush."""
    return self.boxStyle.paddingsBrush

  @margins.GET
  def _getMargins(self) -> QMarginsF:
    """Getter-function for the margins."""
    return self.boxStyle.margins

  @margins.SET
  def _setMargins(self, margins: QMarginsF) -> None:
    """Setter-function for the margins."""
    self.boxStyle.margins = margins

  @borders.GET
  def _getBorders(self) -> QMarginsF:
    """Getter-function for the borders."""
    return self.boxStyle.borders

  @borders.SET
  def _setBorders(self, borders: QMarginsF) -> None:
    """Setter-function for the borders."""
    self.boxStyle.borders = borders

  @paddings.GET
  def _getPaddings(self) -> QMarginsF:
    """Getter-function for the paddings."""
    return self.boxStyle.paddings

  @paddings.SET
  def _setPaddings(self, paddings: QMarginsF) -> None:
    """Setter-function for the paddings."""
    self.boxStyle.paddings = paddings

  @align.GET
  def _getAlign(self) -> Align:
    """Getter-function for the alignment."""
    return self.boxStyle.align

  @align.SET
  def _setAlign(self, value: object) -> None:
    """Setter-function for the alignment."""
    self.boxStyle.align = value

  @allMargins.GET
  def _getAllMargins(self) -> QMarginsF:
    """Getter-function for the allMargins."""
    return QMarginsF() + self.margins + self.borders + self.paddings

  @paddingColor.GET
  def _getPaddingColor(self) -> QColor:
    """Getter-function for the paddingColor."""
    return self.boxStyle.paddingsColor

  @paddingColor.SET
  def _setPaddingColor(self, color: QColor) -> None:
    """Setter-function for the paddingColor."""
    self.boxStyle.paddingsColor = color

  @borderColor.GET
  def _getBorderColor(self) -> QColor:
    """Getter-function for the borderColor."""
    return self.boxStyle.bordersColor

  @borderColor.SET
  def _setBorderColor(self, color: QColor) -> None:
    """Setter-function for the borderColor."""
    self.boxStyle.bordersColor = color

  def paintMeLike(self,
                  rect: Rect,
                  painter: QPainter,
                  event: QPaintEvent) -> Any:
    """Paints the widget with the current style."""
    borderRect = rect - self.margins
    paddedRect = borderRect - self.borders
    contentRect = paddedRect - self.paddings
    borderRect.moveCenter(rect.center())
    paddedRect.moveCenter(rect.center())
    contentRect.moveCenter(rect.center())
    painter.setPen(emptyPen())
    painter.setBrush(self.borderBrush)
    painter.drawRect(borderRect)
    painter.setBrush(self.paddingBrush)
    painter.drawRect(paddedRect)
    return contentRect, painter, event

  def __init__(self, *args, **kwargs) -> None:
    """The constructor method for the BoxWidget."""
    LayoutWidget.__init__(self, *args, **kwargs)
    self.__box_style__ = self.app.loadBox(self.styleId)
