"""ButtonStyle provides a data loading class for state aware buttons."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import json
import os.path

from worktoy.desc import Field
from worktoy.meta import BaseObject
from PySide6.QtCore import QMarginsF, Qt
from PySide6.QtGui import QColor, QBrush
from icecream import ic

ic.configureOutput(includeContext=True)


class ButtonStyle(BaseObject):
  """ButtonStyle provides a data loading class for state aware buttons."""

  __file_name__ = 'button_style.json'
  __style_data__ = None
  __able_key__ = None
  __mouse_key__ = None

  paddings = Field()
  margins = Field()
  borders = Field()
  allMargins = Field()
  backgroundColor = Field()
  borderColor = Field()
  backgroundBrush = Field()
  borderBrush = Field()

  def __init__(self, ableKey: str, mouseKey: str) -> None:
    """Initializes the button style."""
    BaseObject.__init__(self)
    self.__able_key__ = ableKey
    self.__mouse_key__ = mouseKey

  @classmethod
  def loadStyle(cls) -> dict:
    """Loads the style for the push button."""
    here = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
    fid = os.path.join(here, cls.__file_name__)
    with open(fid, 'r') as file:
      return json.loads(file.read())

  def getStyleData(self, **kwargs) -> dict:
    """Returns the style data for the push button."""
    if self.__style_data__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__style_data__ = self.loadStyle()
      return self.getStyleData(_recursion=True)
    return self.__style_data__

  def getStateStyle(self, ) -> dict[str, dict]:
    """Returns the padding for the button state."""
    ableKey = self.__able_key__
    mouseKey = self.__mouse_key__
    data = self.getStyleData()
    if ableKey not in data:
      e = """Key must be one of: 'able', 'disable'!"""
      raise KeyError(e)
    if mouseKey not in data[ableKey]:
      e = """Key must be one of: 'mouseOver', 'mousePress'!"""
      raise KeyError(e)
    return data[ableKey][mouseKey]

  @staticmethod
  def _loadFloats(*values) -> list[float]:
    """Loads a float from the value."""
    out = []
    for val in values:
      if isinstance(val, (str, int, float)):
        val = float(val)
      if not isinstance(val, float):
        e = """Values must be floats, but received: %s!"""
        raise TypeError(e % val)
      out.append(val)
    return out

  @staticmethod
  def _loadInts(*values) -> list[int]:
    """Loads a float from the value."""
    out = []
    for val in values:
      if isinstance(val, (str, int, float)):
        val = int(val)
      if not isinstance(val, int):
        e = """Values must be integers, but received: %s!"""
        raise TypeError(e % val)
      out.append(val)
    return out

  def _loadMargins(self, key: str) -> QMarginsF:
    """Returns the margins for the button state."""
    data = self.getStateStyle().get(key, None)
    if data is None:
      raise KeyError(key)
    if key not in ['margins', 'borders', 'paddings']:
      e = """Key must be one of: 'margins', 'borders', 'paddings'!"""
      raise KeyError(e)
    values = [data.get(k) for k in ['left', 'top', 'right', 'bottom']]
    return QMarginsF(*self._loadFloats(*values), )

  def _loadColors(self, key: str) -> QColor:
    """Loads the color matching the key"""
    data = self.getStateStyle().get(key, None)
    if data is None:
      raise KeyError(key)
    if key not in ['backgroundColor', 'borderColor']:
      e = """Key must be one of: 'margins', 'borders', 'paddings'!"""
      raise KeyError(e)
    values = [data.get(k, None) for k in ['r', 'g', 'b', ]]
    values = self._loadInts(*values, data.get('a', 255))
    return QColor(*values, )

  @margins.GET
  def getStateMargins(self) -> QMarginsF:
    """Returns the margins for the button state."""
    return self._loadMargins('margins')

  @borders.GET
  def getStateBorders(self) -> QMarginsF:
    """Returns the borders for the button state."""
    return self._loadMargins('borders')

  @paddings.GET
  def getStatePaddings(self) -> QMarginsF:
    """Returns the paddings for the button state."""
    return self._loadMargins('paddings')

  @backgroundColor.GET
  def getStateBackgroundColor(self) -> QColor:
    """Returns the background color for the button state."""
    return self._loadColors('backgroundColor')

  @borderColor.GET
  def getStateBorderColor(self) -> QColor:
    """Returns the border color for the button state."""
    return self._loadColors('borderColor')

  @borderBrush.GET
  def getBorderBrush(self) -> QBrush:
    """Returns the border brush for the button state."""
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    brush.setColor(self.borderColor)
    return brush

  @backgroundBrush.GET
  def getBackgroundBrush(self) -> QBrush:
    """Returns the background brush for the button state."""
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    brush.setColor(self.backgroundColor)
    return brush
