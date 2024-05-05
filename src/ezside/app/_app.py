"""App subclasses the QApplication class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import Any, Callable, TYPE_CHECKING

from PySide6.QtCore import Qt, Signal, QSettings
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from attribox import AttriBox
from icecream import ic
from vistutils.text import monoSpace, stringList
from vistutils.waitaminute import typeMsg

from ezside.app import StyleSettings

ic.configureOutput(includeContext=True, )

MenuFlag = Qt.ApplicationAttribute.AA_DontUseNativeMenuBar

if TYPE_CHECKING:
  from ezside.widgets import BaseWidget


class App(QApplication):
  """App is a subclass of QApplication."""

  __main_app__ = True

  __missing_names__ = None
  __main_window_class__ = None
  __main_window_instance__ = None
  __icon_path__ = None

  @classmethod
  def getSettings(cls) -> QSettings:
    """Getter-function for settings."""
    appName = cls.applicationName()
    orgName = cls.organizationName()
    return QSettings(orgName, appName)

  @classmethod
  def getStyle(cls, widget: BaseWidget) -> Any:
    """Applies style changes to the widget received based on its class and
    style ID from the application settings."""
    clsName = str(type(widget))
    styleId = widget.styleId
    styleDict = {}
    fallbacks = widget.getStyleFallbacks()
    schema = widget.getStyleSchema()
    settings = cls.getSettings()
    for (key, fallback) in widget.getStyleFallbacks():
      styleKey = '%s/%s/%s' % (clsName, styleId, key)
      styleType = schema[key]
      styleValue = settings.value(styleKey, fallback)
      if not isinstance(styleValue, styleType):
        e = typeMsg('styleValue', styleValue, styleType)
        raise TypeError(e)
      styleDict[key] = styleValue
    return styleDict

  @classmethod
  def _getIconPath(cls) -> str:
    """Getter-function for path to icon folder"""
    if cls.__icon_path__ is None:
      here = os.path.dirname(os.path.abspath(__file__))
      cls.__icon_path__ = os.path.join(here, 'icons')
    return cls.__icon_path__

  @classmethod
  def getIcon(cls, name: str) -> QIcon:
    """Getter-function for path to icon"""

    def cleanName(name2: str) -> str:
      """Removes spaces and .png from the given name and returns in lower
      case."""
      return str(name2).replace('.png', '').replace(' ', '').lower()

    iconPath = cls._getIconPath()
    icons = os.listdir(iconPath)
    for fileName in icons:
      if cleanName(fileName) == cleanName(name):
        return QIcon(QPixmap(os.path.join(iconPath, fileName)))
    else:
      return QIcon(QPixmap(os.path.join(iconPath, 'risitas.png')))

  styleSettings = AttriBox[StyleSettings]()
  quitRequested = Signal()

  @staticmethod
  def _validateNameSpace(cls: type, *names) -> type:
    """The given type must have an attribute, possibly equal to None,
    for each name given. """
    if not isinstance(cls, type):
      e = typeMsg('cls', cls, type)
      raise TypeError(e)
    for name in names:
      if not hasattr(cls, name):
        e = """Given class '%s' is missing attribute: '%s'!"""
        raise AttributeError(monoSpace(e % (cls, name)))
    return cls

  @staticmethod
  def _validateCallableSpace(cls, *hereIsMyNumber) -> type:
    """The given type must have a callable attribute at each given name"""
    if not isinstance(cls, type):
      e = typeMsg('cls', cls, type)
      raise TypeError(e)
    cls = App._validateNameSpace(cls, *hereIsMyNumber)
    for name in hereIsMyNumber:
      callMeMaybe = getattr(cls, name, )
      if not callable(callMeMaybe):
        e = typeMsg(name, callMeMaybe, Callable)
        raise TypeError(e)
    return cls

  def __init__(self, mainWindowClass: type) -> None:
    """Initializes the App instance."""
    QApplication.__init__(self, )
    self.setApplicationName('EZSide')
    self.setOrganizationName('EZ')
    self.setAttribute(MenuFlag, True)
    if isinstance(mainWindowClass, type):
      self._setMainWindowClass(mainWindowClass)
    else:
      e = typeMsg('mainWindowClass', mainWindowClass, type)
      raise TypeError(e)

  def appendMissingName(self, name: str) -> None:
    """Appends a missing name."""
    self.__missing_names__ = [self.getMissingNames(), name]

  def getMissingNames(self, **kwargs) -> list[str]:
    """Getter-function for missing names."""
    if self.__missing_names__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__missing_names__ = []
      return self.getMissingNames(_recursion=True)
    if isinstance(self.__missing_names__, list):
      for name in self.__missing_names__:
        if not isinstance(name, str):
          e = typeMsg('name', name, str)
          raise TypeError(e)
      return self.__missing_names__
    e = typeMsg('__missing_names__', self.__missing_names__, list)
    raise TypeError(e)

  @staticmethod
  def _validateMainWindowClass(cls: type) -> type:
    """Validates the main window class, returns it, or raises an error.
    Any class returned cannot be validated any further except by
    instantiation. """
    if not issubclass(cls, QMainWindow):
      e = typeMsg('cls', cls, QMainWindow)
      raise TypeError(e)
    propNames = stringList("""__running_app__, requestQuit""")
    cls = App._validateNameSpace(cls, *propNames)
    callNames = stringList("""getApp""")
    return App._validateCallableSpace(cls, *callNames)

  def _setMainWindowClass(self, cls: type) -> None:
    """Set the main window class."""
    if self.__main_window_class__ is not None:
      e = """The main window class has already been set!"""
      raise RuntimeError(e)
    self.__main_window_class__ = self._validateMainWindowClass(cls)
    self.__main_window_class__ = cls

  def _getMainWindowClass(self) -> type:
    """Get the main window class."""
    if self.__main_window_class__ is None:
      e = """The main window class has not been set!"""
      raise RuntimeError(e)
    return self.__main_window_class__

  def _createMainWindowInstance(self) -> None:
    """Create the main window."""
    mainWindow = self._getMainWindowClass()()
    setattr(mainWindow, '__running_app__', self)
    if not mainWindow.getApp() is self:
      e = """The main window instance is unable to recognize the running 
      application!"""
      raise RuntimeError(e)
    mainWindow.requestQuit.connect(self.quitRequested)
    setattr(self, '__main_window_instance__', mainWindow)

  def getMainWindowInstance(self, **kwargs) -> Any:
    """Getter-function for the main window instance."""

    if self.__main_window_instance__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createMainWindowInstance()
      return self.getMainWindowInstance(_recursion=True)
    mainWindowClass = self._getMainWindowClass()
    setattr(self.__main_window_instance__, '__running_app__', self)
    if isinstance(self.__main_window_instance__, mainWindowClass):
      return self.__main_window_instance__
    e = typeMsg('mainWindowInstance',
                self.__main_window_instance__,
                mainWindowClass)
    raise TypeError(e)

  def getMain(self, **kwargs) -> Any:
    """Getter-function for the main window instance."""
    return self.getMainWindowInstance(**kwargs)

  def exec(self) -> int:
    """Executes the application."""
    mainWindow = self.getMainWindowInstance()
    setattr(mainWindow, '__running_app__', self)
    mainWindow.show()
    return QApplication.exec_(self)
