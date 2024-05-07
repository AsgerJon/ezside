"""BaseWidget provides a common base class for all widgets in the
application."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Optional

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QWidget
from attribox import AttriBox
from vistutils.fields import EmptyField
from vistutils.waitaminute import typeMsg

from ezside.core import parseParent
from ezside.app import AppSettings
from ezside.widgets import _AttriWidget

if TYPE_CHECKING:
  from ezside.app import BaseWindow, App


class BaseWidget(_AttriWidget):
  """BaseWidget provides a common base class for all widgets in the
  application."""

  __app_settings__ = None

  styleId = AttriBox[str]('base')
  state = EmptyField()
  prefix = EmptyField()

  @staticmethod
  def _parseStyleId(**kwargs) -> Optional[str]:
    """Parses the styleId from the keyword arguments."""
    for key in ['styleId', 'style', 'id', '__fb']:
      if key in kwargs:
        styleId = kwargs[key]
        if isinstance(styleId, str):
          return styleId
        e = typeMsg('styleId', styleId, str)
        raise TypeError(e)

  def _getStyleFallback(self, key: str) -> dict | None:
    """Getter-function for the style fallback at the given key. Please
    note, that this is the local key not including any prefixes.
    Subclasses may implement this method to provide fallback values for
    styles. This method is expected to remain empty or to return a
    dictionary object. """

  def _getSettings(self) -> AppSettings:
    """Getter-function for the application settings."""
    if self.__app_settings__ is None:
      self.__app_settings__ = AppSettings()
    return self.__app_settings__

  @state.GET
  def _getState(self, ) -> str:
    """This private method provides a default value used when a subclass
    does not implement the 'getState' method."""
    return self.getState() or 'normal'

  @prefix.GET
  def _getPrefix(self, ) -> str:
    """This private method creates the style key for the widget. """
    clsName = self.__class__.__name__.lower()
    return '%s/%s/%s' % (clsName, self.styleId, self.state)

  def getStyle(self, key: str, fb: Any = None) -> Any:
    """Getter-function for the style at the given key for the widget in
    its current state and style id. """
    styleKey = '%s/%s' % (self.prefix, key)
    if fb is None:
      fb = self._getStyleFallback(key)
    if fb is None:
      return self._getSettings().value(styleKey, )
    return self._getSettings().value(styleKey, fb)

  def getState(self, ) -> str:
    """Getter-function for the current state of the widget. Subclasses
    may implement this method to provide the widget with state awareness."""

  def __init__(self: BaseWidget, *args, **kwargs) -> None:
    """Subclasses that wish to allow __init__ to set the value of the
    'styleId' and other subclass specific primitive attributes, must apply
    these before invoking the parent __init__ method. This is because
    the __init__ automatically triggers the rest of the 'init' methods.
    Please note that BaseWidget will look for keyword arguments to set the
    styleId, at the following names:
      - 'styleId'
      - 'style'
      - 'id'
    defaulting to 'base' if none are found. """
    parent = parseParent(args)
    if parent is None:
      QWidget.__init__(self)
    else:
      QWidget.__init__(self, parent)
    self.styleId = self._parseStyleId(**kwargs, __fb='base')
    self.initStyle()
    self._universalInit()
    self.initUi()
    self.initSignalSlot()

  def getStyleFallbacks(self, ) -> dict[str, Any]:
    """Getter-function for style fallbacks. Subclasses are not required to
    reimplement this method, but only styles specified in the schema returned
    by this method can be centrally managed."""

  def getStyleSchema(self, ) -> dict[str, type]:
    """Getter-function for the style types. This method is auto generated
    from the getStyleFallbacks method. Subclasses reimplementing this
    method should leave the parent functionality intact. """
    out = {}
    for key, val in self.getStyleFallbacks().items():
      if key in out:
        e = """Duplicate key: '%s' in style fallbacks.""" % key
        raise KeyError(e)
      out[key] = type(val)
    return out

  def initStyle(self, ) -> None:
    """Initializes the style for the widget. Optional for subclasses to
    implement. """

  def _universalInit(self) -> None:
    """This method applies to all widgets. Subclasses are not permitted to
    reimplement. This prohibition will be enforced in a future update."""
    self.setMinimumSize(32, 32)

  @abstractmethod
  def initUi(self, ) -> None:
    """Initializes the user interface for the widget. Required for subclasses
    to implement. """

  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the widget. Optional for
    subclasses to implement."""

  @staticmethod
  def getMain() -> BaseWindow:
    """Getter-function for the owning main window"""
    app = QCoreApplication.instance()
    if TYPE_CHECKING:
      assert isinstance(app, App)
    return app.mainWindow
