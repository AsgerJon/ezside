"""JSONBoxStyle subclasses AbstractBoxStyle reading the relevant fields
from a JSON file. The JSON file should use the following schema:

"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
import json
from PySide6.QtCore import QPointF, QMarginsF
from PySide6.QtGui import QColor, QBrush, QFont, QPen
from worktoy.parse import maybe
from worktoy.text import typeMsg

from ezside.base_widgets import AbstractBoxStyle
from ezside.style import Align
from ezside.style.font_enums import FontFamily, FontWeight, FontCap


class JSONBoxStyle(AbstractBoxStyle):
  """JsonBoxStyle loads style properties from a JSON file to set the
  visual aspects of widgets following the box model."""

  __resource_loader__ = None

  def __init__(self, *args) -> None:
    """Initializes the JsonBoxStyle class by loading properties from a
    specified JSON file."""
    data, filePath = None, None
    for arg in args:
      if isinstance(arg, str):
        self._loadFile(arg)
        break
      if isinstance(arg, dict):
        self.loadStyleProperties(arg)
        break

  def _loadFile(self, filePath: str) -> None:
    """Loads the JSON file from the specified path."""
    filePath = LoadResource('styles').getFilePath(filePath)
    try:
      with open(filePath, 'r') as file:
        data = json.load(file)
      self.loadStyleProperties(data)
    except FileNotFoundError:
      raise FileNotFoundError("The JSON file was not found.")
    except json.JSONDecodeError:
      raise json.JSONDecodeError("Error decoding the JSON file.")

  def loadStyleProperties(self, data: dict) -> None:
    """Loads style properties from a dictionary, utilizing explicit fields
    for constructing QMarginsF, QPointF, and QColor objects."""
    self.__box_margins__ = QMarginsF(
        data['margins']['left'],
        data['margins']['top'],
        data['margins']['right'],
        data['margins']['bottom']
    )
    self.__box_borders__ = QMarginsF(
        data['borders']['left'],
        data['borders']['top'],
        data['borders']['right'],
        data['borders']['bottom']
    )
    self.__box_paddings__ = QMarginsF(
        data['paddings']['left'],
        data['paddings']['top'],
        data['paddings']['right'],
        data['paddings']['bottom']
    )
    self.__corner_radius__ = QPointF(
        data.get('corner_radius', {'x': 1})['x'],
        data.get('corner_radius', {'y': 1})['y'],
    )
    self.__padded_color__ = self.createQColor(data['padded_color'])
    self.__border_color__ = self.createQColor(data['border_color'])
    penColor = data.get('pen_color', {})
    self.__pen_color__ = self.createQColor(penColor)
    self.__padded_brush__ = QBrush(self.__padded_color__)
    self.__border_brush__ = QBrush(self.__border_color__)

  @staticmethod
  def createQColor(colorData: dict) -> QColor:
    """Creates a QColor object from provided color data with default
    alpha."""
    r = colorData.get('red', 255)
    g = colorData.get('green', 255)
    b = colorData.get('blue', 255)
    a = colorData.get('alpha', 255)  # Default alpha value is 255
    return QColor(r, g, b, a)

  def getFont(self) -> QFont:
    """Getter-function for the font"""
    textFont = QFont()
    if self.__font_family__ is None:
      textFont.setFamily('Courier')
    else:
      textFont.setFamily(self.__font_family__.qt)
    textFont.setPointSize(maybe(self.__font_size__, 18))
    if self.__font_weight__ is None:
      textFont.setWeight(FontWeight.NORMAL.qt)
    else:
      textFont.setWeight(self.__font_weight__.qt)
    if self.__font_cap__ is None:
      textFont.setCapitalization(FontCap.MIX.qt)
    else:
      textFont.setCapitalization(self.__font_cap__.qt)
    return textFont

  def getBoxMargins(self) -> QMarginsF:
    """Getter-function for the box margins"""
    return self.__box_margins__

  def getBoxBorders(self) -> QMarginsF:
    """Getter-function for the box borders"""
    return self.__box_borders__

  def getBoxPaddings(self) -> QMarginsF:
    """Getter-function for the box paddings"""
    return self.__box_paddings__

  def getCornerRadius(self) -> QPointF:
    """Getter-function for the corner radius specification"""
    return self.__corner_radius__

  def getPaddedColor(self) -> QColor:
    """Getter-function for the color of the innermost region"""
    return self.__padded_color__

  def getBorderColor(self) -> QColor:
    """Getter-function for the color of the border"""
    return self.__border_color__

  def getTextColor(self) -> QColor:
    """Getter-function for the text color"""
    return self.__pen_color__

  def getPaddedBrush(self) -> QBrush:
    """Getter-function for the brush of the padded area"""
    return self.__padded_brush__

  def getBorderBrush(self) -> QBrush:
    """Getter-function for the brush of the border area"""
    return self.__border_brush__

  def _getResourceLoader(self, **kwargs) -> LoadResource:
    """Getter-function for the style"""
    if self.__resource_loader__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__resource_loader__ = LoadResource('styles')
      return self._getResourceLoader(_recursion=True)
    if isinstance(self.__resource_loader__, LoadResource):
      return self.__resource_loader__
    e = typeMsg('style', self.__resource_loader__, LoadResource)
    raise TypeError(e)
