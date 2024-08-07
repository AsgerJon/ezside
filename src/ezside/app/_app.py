"""App provides a subclass of QApplication. Please note that this subclass
provides only functionality relating to managing threads. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow
from worktoy.text import typeMsg

MenuFlag = Qt.ApplicationAttribute.AA_DontUseNativeMenuBar


class App(QApplication):
  """App provides a subclass of QApplication. Please note that this subclass
  provides only functionality relating to managing threads. """

  __main_window_class__ = None
  __main_window_instance__ = None

  def __init__(self, cls: type, ) -> None:
    """Initializes the application"""
    QApplication.__init__(self, )
    self.setAttribute(MenuFlag)
    self._setWindowClass(cls)
    self.setApplicationName('EZSide')
    self.setOrganizationName('EZSide')

  def _getWindowClass(self) -> type:
    """Returns the main window class"""
    if isinstance(self.__main_window_class__, type):
      if issubclass(self.__main_window_class__, QMainWindow):
        return self.__main_window_class__
      e = """Expected window class to be a subclass of QMainWindow!"""
      raise TypeError(e)
    e = typeMsg('mainWindow', self.__main_window_class__, type)
    raise TypeError(e)

  def _setWindowClass(self, cls: type) -> None:
    """Sets the main window class"""
    if self.__main_window_class__ is not None:
      e = """The window class is already set!"""
      raise AttributeError(e)
    if not isinstance(cls, type):
      e = typeMsg('mainWindow', cls, type)
      raise TypeError(e)
    if not issubclass(cls, QMainWindow):
      e = """Expected window class to be a subclass of QMainWindow!"""
      raise TypeError(e)
    self.__main_window_class__ = cls

  def _createWindowInstance(self, ) -> None:
    """Creates the main window instance"""
    cls = self._getWindowClass()
    self.__main_window_instance__ = cls()

  def _getWindowInstance(self, **kwargs) -> QMainWindow:
    """Returns the main window instance"""
    if self.__main_window_instance__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createWindowInstance()
      return self._getWindowInstance(_recursion=True)
    cls = self._getWindowClass()
    if isinstance(self.__main_window_instance__, QMainWindow):
      return self.__main_window_instance__
    e = typeMsg('mainWindow', self.__main_window_instance__, cls)
    raise TypeError(e)

  def exec_(self, ) -> int:
    """Executes the application"""
    window = self._getWindowInstance()
    window.show()
    return QApplication.exec_(self)
