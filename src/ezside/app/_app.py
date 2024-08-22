"""App provides a subclass of QApplication. Please note that this subclass
provides only functionality relating to managing threads. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
from json import loads
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow
from worktoy.desc import Field
from worktoy.text import typeMsg

from ezside.tools import BoxStyle

MenuFlag = Qt.ApplicationAttribute.AA_DontUseNativeMenuBar


class App(QApplication):
  """App provides a subclass of QApplication. Please note that this subclass
  provides only functionality relating to managing threads. """

  __main_window_class__ = None
  __main_window_instance__ = None

  root = Field()
  pythonPath = Field()
  etc = Field()
  icons = Field()
  styles = Field()
  fonts = Field()
  boxes = Field()

  @classmethod
  def _loadFile(cls, filePath: str) -> Any:
    """Loads and validates the file at the given path, which is expected
    to be an absolute path. """
    if not os.path.exists(filePath):
      e = """The file is missing: %s"""
      raise FileNotFoundError(e % filePath)
    if not os.path.isfile(filePath):
      e = """The file is not a file: %s"""
      raise IsADirectoryError(e % filePath)
    with open(filePath, 'r') as file:
      data = file.read()
    return data

  def defaultFont(self, ) -> dict:
    """Returns the default font."""
    fid = os.path.join(self.fonts, 'default.json')
    data = self._loadFile(fid)
    return loads(data)

  def loadFont(self, styleId: str) -> dict:
    """Loads the font at the given style id."""
    out = {}
    fid = os.path.join(self.fonts, f'{styleId}.json')
    data = loads(self._loadFile(fid))
    defaultData = self.defaultFont()
    for key, value in defaultData.items():
      out[key] = data.get(key, value)
    return out

  def defaultBox(self, ) -> dict:
    """Returns the default box."""
    fid = os.path.join(self.boxes, 'default.json')
    data = self._loadFile(fid)
    return loads(data)

  def loadBox(self, styleId: str) -> BoxStyle:
    """Loads the box at the given style id."""
    out = {}
    fid = os.path.join(self.boxes, f'{styleId}.json')
    data = loads(self._loadFile(fid))
    defaultData = self.defaultBox()
    for key, value in defaultData.items():
      out[key] = data.get(key, value)
    return BoxStyle.load(out)

  @boxes.GET
  def _getBoxes(self) -> str:
    """Getter-function for the 'boxes' folder. """
    return os.path.join(self.styles, 'boxes')

  @fonts.GET
  def _getFonts(self) -> str:
    """Getter-function for the 'fonts' folder. """
    return os.path.join(self.styles, 'fonts')

  @styles.GET
  def _getStyles(self) -> str:
    """Getter-function for the 'styles' folder. """
    return os.path.join(self.etc, 'styles')

  @icons.GET
  def _getIcons(self) -> str:
    """Getter-function for the 'icons' folder. """
    return os.path.join(self.etc, 'icons')

  @etc.GET
  def _getEtc(self) -> str:
    """Getter-function for the etc folder. """
    return os.path.join(self.root, 'etc')

  @pythonPath.GET
  def _getPythonPath(self) -> str:
    """Getter-function for the python path. """
    return self.applicationDirPath()

  @root.GET
  def _getRoot(self) -> str:
    """Getter-function for the root folder. """
    here = os.path.dirname(__file__)
    rootDir = os.path.abspath(os.path.join(here, '..', '..', '..'))
    requiredDirectories = ['src', 'etc']
    for directory in requiredDirectories:
      if directory not in os.listdir(rootDir):
        e = """The root folder is missing the required directory: %s"""
        raise FileNotFoundError(e % directory)
    return rootDir

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
    introMsg = """Starting application!"""
    pythonMsg = """Using python located at: %s""" % self.pythonPath
    rootMsg = """Root folder located at: %s""" % self.root
    n = max(len(introMsg), len(pythonMsg), len(rootMsg))

    print('_' * n)
    print(introMsg)
    print(pythonMsg)
    print(rootMsg)
    print('¨' * n)
    window = self._getWindowInstance()
    window.show()
    return QApplication.exec_(self)
