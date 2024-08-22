"""App provides a subclass of QApplication. Please note that this subclass
provides only functionality relating to managing threads. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
from json import loads, JSONDecodeError
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow
from worktoy.desc import Field
from worktoy.text import typeMsg, monoSpace

from ezside.style import ControlStyle, BoxStyle, FontStyle

MenuFlag = Qt.ApplicationAttribute.AA_DontUseNativeMenuBar


class App(QApplication):
  """App provides a subclass of QApplication. Please note that this subclass
  provides only functionality relating to managing threads. """

  __ezside_app__ = True

  __main_window_class__ = None
  __main_window_instance__ = None
  __style_classes__ = dict(font=FontStyle,
                           box=BoxStyle,
                           control=ControlStyle)
  __named_icons__ = dict(aboutConda='about_conda.png',
                         aboutPySide6='about_pyside6.png',
                         aboutPython='about_python.png',
                         aboutQt='about_qt.png',
                         add='add.png',
                         copy='copy.png',
                         cut='cut.png',
                         debug='debug.png',
                         documentation='documentation.png',
                         editMenu='edit_menu.png',
                         exit='exit.png',
                         exitImg='exit_img.png',
                         files='files.png',
                         filesMenu='files_menu.png',
                         help='help.png',
                         helpMenu='help_menu.png',
                         locked='locked.png',
                         microphone='microphone.png',
                         new='new.png',
                         open='open.png',
                         paste='paste.png',
                         preferences='preferences.png',
                         redo='redo.png',
                         save='save.png',
                         saveAs='save_as.png',
                         screenShot='screen_shot.png',
                         selectAll='select_all.png',
                         undo='undo.png',
                         unlocked='unlocked.png')

  root = Field()
  pythonPath = Field()
  etc = Field()
  icons = Field()
  styles = Field()
  fonts = Field()
  boxes = Field()

  def getIconFile(self, iconName: str, **kwargs) -> str:
    """Getter-function for the path to the named icon. """
    if iconName not in self.__named_icons__:
      if kwargs.get('strict', False):
        e = """The icon name is not in the named icons!"""
        raise ValueError(e)
      return os.path.join(self.icons, 'risitas.png')
    iconFid = os.path.join(self.icons, self.__named_icons__[iconName])
    if not os.path.exists(iconFid):
      e = """The icon file is missing: %s"""
      raise FileNotFoundError(e % iconFid)
    if not os.path.isfile(iconFid):
      e = """The icon file is not a file: %s"""
      raise IsADirectoryError(e % iconFid)
    return str(iconFid)

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

  def _loadStyle(self,
                 type_: str,
                 styleId: str,
                 stateId: str = None) -> Any:
    """Loads the style type at the given style id."""
    fid = os.path.join(self.styles, type_, f'{styleId}.json')
    defaultFid = os.path.join(self.styles, type_, 'default.json')
    rawData = self._loadFile(fid)
    try:
      data = loads(rawData)
    except JSONDecodeError as jsonDecodeError:
      e = """The style file: '%s' could not be decoded: %s"""
      raise KeyError(e % (fid, str(rawData))) from jsonDecodeError
    defaultData = loads(self._loadFile(defaultFid))
    if stateId is not None:
      if stateId not in data:
        e = """The state id is not in the font data!"""
        raise ValueError(e)
      data = data[stateId]
    out = {}
    for key, value in defaultData.items():
      out[key] = data.get(key, value)
    return self.__style_classes__[type_].load(out)

  def loadBox(self, styleId: str, stateId: str = None) -> BoxStyle:
    """Loads the box style at the given style id."""
    return self._loadStyle('box', styleId, stateId)

  def loadFont(self, styleId: str, stateId: str = None) -> FontStyle:
    """Loads the font style at the given style id."""
    return self._loadStyle('font', styleId, stateId)

  def loadControl(self, styleId: str, stateId: str = None) -> ControlStyle:
    """Loads the control style at the given style id."""
    return self._loadStyle('control', styleId, stateId)

  @boxes.GET
  def _getBoxes(self) -> str:
    """Getter-function for the 'box' folder. """
    return os.path.join(self.styles, 'box')

  @fonts.GET
  def _getFonts(self) -> str:
    """Getter-function for the 'font' folder. """
    return os.path.join(self.styles, 'font')

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
