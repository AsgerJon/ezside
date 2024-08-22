"""StateBoxStyle further subclasses JSONBoxStyle providing multiple
instances of different states. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QMarginsF, QPointF, Qt
from PySide6.QtGui import QBrush, QColor, QPen
from worktoy.text import typeMsg

from ezside.base_widgets import JSONBoxStyle
from ezside.tools import LoadResource, ButtonState


class StateBoxStyle(JSONBoxStyle):
  """StateBoxStyle further subclasses JSONBoxStyle providing multiple
  instances of different states. """

  __fallback_filename__ = 'button_style.json'
  __fallback_style__ = 'styles'
  __resource_loader__ = None
  __style_data__ = None
  __file_name__ = None
  __owning_widget__ = None

  def __init__(self, *args) -> None:
    self.__file_name__ = None
    for arg in args:
      if isinstance(arg, str):
        self.__file_name__ = arg
        break
    else:
      self.__file_name__ = self.__fallback_filename__

  def _createStyleData(self, ) -> None:
    """Creator-function for the style data"""
    cls = type(self)
    fid = self.__file_name__
    data = LoadResource.getData('styles', fid)
    self.__style_data__ = {}
    for state in ButtonState:
      name = state.name.lower()
      for key, val in data.items():
        if name == key.lower():
          if isinstance(val, dict):
            stateData = cls()
            stateData.loadStyleProperties(val)
            self.__style_data__[state] = stateData
      else:
        e = """Unable to recognize state: %s""" % state
        raise ValueError(e)

  def _getStyleData(self, **kwargs) -> dict:
    """Getter-function for the full style data"""
    if self.__style_data__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createStyleData()
      return self._getStyleData(_recursion=True)
    if isinstance(self.__style_data__, dict):
      return self.__style_data__
    e = typeMsg('__style_data__', self.__style_data__, dict)
    raise TypeError(e)

  def _getStyle(self) -> dict:
    """Getter-function for the style"""
    return self._getStyleData()[self.getState()]

  def getState(self) -> ButtonState:
    """Returns the current state of the button."""
    return self.__owning_widget__.getState()

  def getBoxMargins(self) -> QMarginsF:
    """Getter-function for the box margins"""
    return self._getStyle()['margins']

  def getBoxBorders(self) -> QMarginsF:
    """Getter-function for the box borders"""
    return self._getStyle()['borders']

  def getBoxPaddings(self) -> QMarginsF:
    """Getter-function for the box paddings"""
    return self._getStyle()['paddings']

  def getCornerRadius(self) -> QPointF:
    """Getter-function for the corner radius specification"""
    return self._getStyle()['radius']

  def getPaddedColor(self) -> QColor:
    """Getter-function for the color of the innermost region"""
    return self._getStyle()['padded_color']

  def getBorderColor(self) -> QColor:
    """Getter-function for the color of the border"""
    return self._getStyle()['border_color']

  def getPenColor(self) -> QColor:
    """Getter-function for the color of the pen"""
    return self._getStyle()['pen_color']

  def getPaddedBrush(self) -> QBrush:
    """Getter-function for the brush of the padded area"""
    brush = QBrush()
    brush.setColor(self.getPaddedColor())
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    return brush

  def getBorderBrush(self) -> QBrush:
    """Getter-function for the brush of the border area"""
    brush = QBrush()
    brush.setColor(self.getBorderColor())
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    return brush

  def getTextPen(self, ) -> QPen:
    """Getter-function for the pen of the text"""
    pen = QPen()
    pen.setStyle(Qt.PenStyle.SolidLine)
    pen.setColor(self.getTextColor())
    pen.setWidth(1)
    return pen
