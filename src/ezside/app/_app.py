"""App subclasses QApplication providing the custom application. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import subprocess

from PySide6.QtWidgets import QApplication, QMainWindow

from worktoy.text import typeMsg, monoSpace


def allowXServerAccess() -> None:
  """Allow the application to access the X server."""
  try:
    subprocess.run(['xhost', '+'])
  except subprocess.CalledProcessError as exception:
    e = """Failed to allow the application to access the X server, when
    encountering the following error: '%s'""" % str(exception)
    raise RuntimeError(monoSpace(e))


def disallowXServerAccess() -> None:
  """Disallow the application to access the X server."""
  try:
    subprocess.run(['xhost', '-'])
  except subprocess.CalledProcessError as exception:
    e = """Failed to disallow the application to access the X server, when
    encountering the following error: '%s'""" % str(exception)
    raise RuntimeError(monoSpace(e))


class App(QApplication):
  """App subclasses QApplication providing the custom application. """
  __window_class__ = None
  __window_instance__ = None

  def __init__(self, cls: type, *args, **kwargs) -> None:
    self.__window_class__ = cls
    QApplication.__init__(self, *args, **kwargs)

  def _getWindowClass(self) -> type:
    if self.__window_class__ is None:
      e = """The window class has not been set. """
      raise RuntimeError(e)
    if not isinstance(self.__window_class__, type):
      e = typeMsg('self.__window_class__', self.__window_class__, type)
      raise TypeError(e)
    if issubclass(self.__window_class__, QMainWindow):
      return self.__window_class__
    e1 = """The window class must be a subclass of QMainWindow, 
    but received class: '%s' with mro: """ % self.__window_class__.__name__
    mroNames = [cls.__name__ for cls in self.__window_class__.__mro__]
    e2 = '<br><tab>'.join(mroNames)
    e = """%s<br><tab>%s""" % (e1, e2)
    raise TypeError(e)

  def _createWindowInstance(self, ) -> None:
    if self.__window_instance__ is not None:
      e = """The window instance has already been created. """
      raise RuntimeError(e)
    cls = self._getWindowClass()
    self.__window_instance__ = cls()

  def _getWindowInstance(self, **kwargs) -> QMainWindow:
    if self.__window_instance__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError()
      self._createWindowInstance()
      return self._getWindowInstance(_recursion=True)
    cls = self._getWindowClass()
    if issubclass(cls, QMainWindow):
      if isinstance(self.__window_instance__, cls):
        return self.__window_instance__
    e = typeMsg('self.__window_instance__', self.__window_instance__, cls)
    raise TypeError(e)

  def exec_(self) -> int:
    """Start the application event loop."""
    main = self._getWindowInstance()
    main.show()
    return QApplication.exec_(self)
