"""BaseButton subclasses AbstractButton implementing the state sensitive
painting. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TypeAlias, Union, Any

from PySide6.QtCore import QRect, QSizeF, QMarginsF, QSize
from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter, QPaintEvent, QBrush
from icecream import ic
from worktoy.desc import Field, AttriBox
from worktoy.text import typeMsg

from ezside.style import ButtonState, Align
from ezside.base_widgets import AbstractButton
from ezside.tools import emptyPen

ic.configureOutput(includeContext=True)

Rect: TypeAlias = Union[QRect, QRectF]


class BaseButton(AbstractButton):
  """BaseButton subclasses AbstractButton implementing the state sensitive
  painting. """

  __fallback_text__ = 'Click Me!'
  __button_text__ = None

  text = AttriBox[str]()

  #  Dynamic styles
  __box_styles__ = None
  __font_styles__ = None

  boxStyle = Field()
  bordersBrush = Field()
  paddingsBrush = Field()
  fontStyle = Field()
  allMargins = Field()

  #  Box Styles
  def _createBoxStyle(self) -> None:
    """Creates the box style"""
    self.__box_styles__ = {
        ButtonState.DISABLED_HOVER   : self.app.loadBox(
            self.styleId, 'disabled_hover'),
        ButtonState.DISABLED_RELEASED: self.app.loadBox(
            self.styleId, 'disabled_released'),
        ButtonState.DISABLED_PRESSED : self.app.loadBox(
            self.styleId, 'disabled_pressed'),
        ButtonState.ENABLED_HOVER    : self.app.loadBox(
            self.styleId, 'enabled_hover'),
        ButtonState.ENABLED_RELEASED : self.app.loadBox(
            self.styleId, 'enabled_released'),
        ButtonState.ENABLED_PRESSED  : self.app.loadBox(
            self.styleId, 'enabled_pressed'),
    }

  @boxStyle.GET
  def _getBoxStyle(self, **kwargs) -> dict:
    """Getter-function for the box style"""
    if self.__box_styles__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createBoxStyle()
      return self._getBoxStyle(_recursion=True)
    return self.__box_styles__[self.buttonState]

  #  Font Styles
  def _createFontStyle(self) -> None:
    """Creator function for the state sensitive font styles."""
    self.__font_styles__ = {
        ButtonState.DISABLED_HOVER   : self.app.loadFont(
            self.styleId, 'disabled_hover'),
        ButtonState.DISABLED_RELEASED: self.app.loadFont(
            self.styleId, 'disabled_released'),
        ButtonState.DISABLED_PRESSED : self.app.loadFont(
            self.styleId, 'disabled_pressed'),
        ButtonState.ENABLED_HOVER    : self.app.loadFont(
            self.styleId, 'enabled_hover'),
        ButtonState.ENABLED_RELEASED : self.app.loadFont(
            self.styleId, 'enabled_released'),
        ButtonState.ENABLED_PRESSED  : self.app.loadFont(
            self.styleId, 'enabled_pressed'),
    }

  @fontStyle.GET
  def _getFontStyle(self, **kwargs) -> dict:
    """Getter-function for the font style"""
    if self.__font_styles__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createFontStyle()
      return self._getFontStyle(_recursion=True)
    return self.__font_styles__[self.buttonState]

  @bordersBrush.GET
  def _getBordersBrush(self) -> QBrush:
    """Getter-function for the border brush"""
    return self.boxStyle.bordersBrush

  @paddingsBrush.GET
  def _getPaddingsBrush(self) -> QBrush:
    """Getter-function for the padding brush"""
    return self.boxStyle.paddingsBrush

  @allMargins.GET
  def _getAllMargins(self) -> QMarginsF:
    """Getter-function for the margins"""
    out = QMarginsF()
    out += self.boxStyle.margins
    out += self.boxStyle.borders
    out += self.boxStyle.paddings
    return out

  def requiredSize(self) -> QSizeF:
    """This method informs the parent layout of the size this widget at
    minimum requires to render. """
    textRect = self.requiredRect()
    if isinstance(textRect, QRectF):
      return textRect.size()
    if isinstance(textRect, QRect):
      return QSize.toSizeF(textRect.size())
    e = typeMsg('requiredRect', textRect, QRectF)
    raise TypeError(e)

  def requiredRect(self, ) -> QRectF:
    """Rectangle required to bound the current text"""
    textRect = self.fontStyle.metrics.boundingRect(self.text)
    return textRect + self.allMargins

  def getMouseRegion(self) -> QRectF:
    """This method returns the region of this widget that is sensitive to
    pointer events. """

  def getAlignment(self) -> Align:
    """Getter-function for the alignment setting"""
    return Align.CENTER

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the BaseButton"""
    unusedArgs = []
    tempArgs = [*args, ]
    while tempArgs:
      arg = tempArgs.pop(0)
      if isinstance(arg, str):
        self.text = arg
        unusedArgs = [*unusedArgs, *tempArgs]
        break
    else:
      self.text = self.__fallback_text__
    AbstractButton.__init__(self, *unusedArgs, **kwargs)
    self.setMouseTracking(True)

  def paintMeLike(self,
                  rect: Rect,
                  painter: QPainter,
                  event: QPaintEvent) -> Any:
    """Paints the BaseButton"""
    borderRect = rect - self.boxStyle.margins
    paddedRect = borderRect - self.boxStyle.borders
    contentRect = paddedRect - self.boxStyle.paddings
    borderRect.moveCenter(rect.center())
    paddedRect.moveCenter(rect.center())
    contentRect.moveCenter(rect.center())
    #  Paint the box model
    painter.setPen(emptyPen())
    painter.setBrush(self.bordersBrush)
    painter.drawRect(borderRect)
    painter.setBrush(self.paddingsBrush)
    painter.drawRect(paddedRect)
    #  Paint the text
    painter.setPen(self.fontStyle.asQPen)
    painter.setFont(self.fontStyle.asQFont)
    textRect = self.requiredRect()
    alignFlag = self.getAlignment()
    paintRect = alignFlag.fitRect(textRect, contentRect)
    painter.drawText(paintRect, alignFlag.qt, self.text)
    return paintRect, painter, event
