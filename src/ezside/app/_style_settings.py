"""StyleSettings subclasses the QSettings class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional, Any, TYPE_CHECKING

from PySide6.QtCore import QSettings
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

if TYPE_CHECKING:
  from ezside.widgets import BaseWidget


class StyleSettings(QSettings):
  """The 'StyleSettings' class provides a convenient interface for
  working with the application's style settings. """

  __active_widget__ = None

  def __init__(self, widget: BaseWidget, *args, **kwargs) -> None:
    QSettings.__init__(self, *args, **kwargs)
    self._setActiveWidget(widget, )

  def _setActiveWidget(self, widget: BaseWidget) -> None:
    """Setter-function for the active widget"""
    if self.__active_widget__ is not None:
      e = """The 'active_widget' attribute is already set. """
      raise AttributeError(e)
    self.__active_widget__ = widget

  def _getActiveWidget(self) -> BaseWidget:
    """Getter-function for the active widget"""
    if self.__active_widget__ is None:
      e = """The 'active_widget' attribute is not set. """
      raise AttributeError(e)
    return self.__active_widget__

  def _getWidgetStyleKey(self, key: str, state: Optional[str]) -> str:
    """The given key should be a key to an entry in the style schema of
    the widget. The key is the replaced with:
    [Widget Class] / [Style Id] / [key]
    """
    clsName = str(self._getActiveWidget().__class__)
    styleId = self._getActiveWidget().styleId
    return '%s/%s/%s' % (clsName, styleId, key)

  def _getWidgetTypeKey(self, key: str) -> type:
    """Getter-function for the type of the active widget"""
    widget = self._getActiveWidget()
    styleType = widget.getStyleSchema().get(key, None)
    if styleType is None:
      clsName = str(widget.__class__)
      e = """For key: '%s', failed to find style type on widget class: 
      '%s'!"""
      raise KeyError(monoSpace(e))
    if isinstance(styleType, type):
      return styleType
    e = typeMsg('styleType', styleType, type)
    raise TypeError(e)

  def _getWidgetFallbackKey(self, key: str, ) -> Any:
    """Getter-function for the fallback value at the given key"""
    fallbackData = self._getActiveWidget().getStyleFallbacks()
    fallback = fallbackData.get(key, None)
    if fallback is None:
      clsName = str(self._getActiveWidget().__class__)
      e = """For key: '%s', failed to find fallback value on widget class: 
      '%s'!""" % (key, clsName)
      raise KeyError(monoSpace(e))
    styleType = self._getWidgetTypeKey(key)
    if isinstance(fallback, styleType):
      return fallback
    e = typeMsg('fallback', fallback, styleType)
    raise TypeError(e)

  def __getitem__(self, key: str) -> Any:
    """Returns the value of the given key."""
    styleKey = self._getWidgetStyleKey(key, None)
    value = QSettings.value(self, styleKey, None)
    if value is None:
      fallback = self._getWidgetFallbackKey(key, )
      QSettings.setValue(self, styleKey, fallback)
      return fallback
    styleType = self._getWidgetTypeKey(key)
    if isinstance(value, styleType):
      return value
    e = typeMsg('value', value, styleType)
    raise TypeError(e)

  def __setitem__(self, key: str | tuple[str, str], value: Any) -> None:
    """Sets the value of the given key."""
    state = None
    if isinstance(key, tuple):
      key, state = key
    styleType = self._getWidgetTypeKey(key, )
    if not isinstance(value, styleType):
      e = typeMsg('value', value, styleType)
      raise TypeError(e)
    styleKey = self._getWidgetStyleKey(key, state)
    QSettings.setValue(self, styleKey, value)
