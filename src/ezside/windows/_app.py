"""App subclasses QApplication and provides the main application object. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from attribox import AttriBox
from vistutils.fields import EmptyField
from vistutils.waitaminute import typeMsg

from ezside.app import AppSettings
from ezside.windows import Main, MainWindow


class App(QApplication):
  """App subclasses QApplication and provides the main application
  object. """

  main = Main(MainWindow)
  settings = EmptyField()
  root = EmptyField()
  iconDir = EmptyField()
  appDir = EmptyField()
  appName = AttriBox[str]()
  orgName = AttriBox[str]()

  @settings.GET
  def getSettings(self) -> AppSettings:
    """Get the application settings."""
    return AppSettings(self)

  @staticmethod
  def getSysArg() -> list:
    """Get the system arguments."""
    return [*sys.argv, ]

  @root.GET
  def _getRoot(self) -> str:
    """Get the root directory."""
    sysDir = self.getSysArg()[0]
    if os.path.isabs(sysDir):
      rootDir = os.path.dirname(os.path.abspath(sysDir))
    else:
      e = """Unable to determine the root directory. """
      raise FileNotFoundError(e)
    return str(os.path.normpath(rootDir))

  @iconDir.GET
  def _getIconDir(self) -> str:
    """Get the icon directory."""
    if isinstance(self.root, str):
      return os.path.join(self.root, 'src', 'ezside', 'app', 'iconfiles')

  @appDir.GET
  def _getAppDir(self) -> str:
    """Get the application directory."""
    if isinstance(self.root, str):
      return os.path.join(self.root, 'src', 'ezside', 'app')

  def getIcon(self, iconName: str) -> QIcon:
    """Get an icon."""
    if isinstance(self.iconDir, str):
      fileName = '%s.png' % iconName
      iconPath = os.path.join(self.iconDir, fileName)
      return QIcon(iconPath)
    e = typeMsg('iconDir', self.iconDir, str)
    raise TypeError(e)

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the App."""
    strArgs = []
    self.__main_window_class__ = None
    for arg in args:
      if isinstance(arg, str):
        strArgs.append(arg)
      elif isinstance(arg, type) and self.__main_window_class__ is None:
        if issubclass(arg, QMainWindow):
          self.__main_window_class__ = arg
    QApplication.__init__(self, )
    self.orgName, self.appName = [*strArgs, None, None][:2]
    self.setOrganizationName(self.orgName)
    self.setApplicationName(self.appName)
    self.setWindowIcon(self.getIcon('pogchamp'))

  def exec(self, ) -> int:
    """Execute the application."""
    if isinstance(self.main, QMainWindow):
      self.main.show()
      return QApplication.exec()
    e = typeMsg('main', self.main, QMainWindow)
    sys.stderr.write(e)
    return 1
