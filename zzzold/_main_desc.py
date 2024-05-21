"""MainDesc implements retrieval of the main window on the running
application instance using the descriptor protocol. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from PySide6.QtCore import QCoreApplication, QObject
from attribox import AbstractDescriptor
from vistutils.waitaminute import typeMsg

from ezside.windows import BaseWindow
from morevistutils import SubClassError

if TYPE_CHECKING:
  pass

Shiboken = type(QObject)


class MainDesc(AbstractDescriptor):
  """MainDesc implements retrieval of the main window on the running
  application instance using the descriptor protocol. """

  __main_window_class__ = None
  __main_window_constructor__ = None
  __fallback_main_window__ = BaseWindow

  def __init__(self, Main: Shiboken = None) -> None:
    """Initialize the descriptor with the main window class."""
    if Main is not None:
      if isinstance(Main, type):
        if not issubclass(Main, BaseWindow):
          raise SubClassError(BaseWindow, Main)
        self.__main_window_class__ = Main
      elif callable(Main):
        self.__main_window_constructor__ = Main
      else:
        e = typeMsg('Main', Main, BaseWindow)
        raise TypeError(e)

  def MAIN(self, callMeMaybe: Callable) -> Callable:
    """Decorator for setting the main window class."""
    if isinstance(callMeMaybe, type):
      return self.setMainClass(callMeMaybe)
    if callable(callMeMaybe):
      return self.setMainConstructor(callMeMaybe)

  def setMainClass(self, Main: Shiboken) -> type:
    """Set the main window class."""
    if isinstance(Main, type):
      if issubclass(Main, BaseWindow):
        self.__main_window_class__ = Main
        return Main
      raise SubClassError(BaseWindow, Main)
    e = typeMsg('Main', Main, BaseWindow)
    raise TypeError(e)

  def setMainConstructor(self, callMeMaybe: Callable) -> Callable:
    """Set the main window constructor."""
    if callable(callMeMaybe):
      self.__main_window_constructor__ = callMeMaybe
      return callMeMaybe
    e = typeMsg('callMeMaybe', callMeMaybe, Callable)
    raise TypeError(e)

  def _createInstance(self, ) -> BaseWindow:
    """Create the main window instance."""
    if self.__main_window_constructor__ is not None:
      if callable(self.__main_window_constructor__):
        return self.__main_window_constructor__()
      e = typeMsg('Main', self.__main_window_constructor__, BaseWindow)
      raise TypeError(e)
    if self.__main_window_class__ is not None:
      if isinstance(self.__main_window_class__, type):
        if issubclass(self.__main_window_class__, BaseWindow):
          return self.__main_window_class__()
        raise SubClassError(BaseWindow, self.__main_window_class__)
      e = typeMsg('Main', self.__main_window_class__, BaseWindow)
      raise TypeError(e)
    if self.__fallback_main_window__ is not None:
      if isinstance(self.__fallback_main_window__, type):
        if issubclass(self.__fallback_main_window__, BaseWindow):
          return self.__fallback_main_window__()
        raise SubClassError(BaseWindow, self.__fallback_main_window__)
      e = typeMsg('Main', self.__fallback_main_window__, BaseWindow)
      raise TypeError(e)
    e = """No main window class or constructor was provided! """
    raise AttributeError(e)

  def __instance_get__(self,
                       instance: object,
                       owner: type,
                       **kwargs) -> Any:
    """Implementation of the getter. The remaining functionality required
    by the descriptor protocol is implemented in the AbstractDescriptor
    class. """
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    window = getattr(instance, pvtName, None)
    if window is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      if QCoreApplication.instance() is None:
        e = """No running application instance found! """
        raise RuntimeError(e)
      window = self._createInstance()
      setattr(instance, pvtName, window)
      return self.__instance_get__(instance, owner, _recursion=True)
    if isinstance(window, BaseWindow):
      return window
    e = typeMsg('window', window, BaseWindow)
    raise TypeError(e)
