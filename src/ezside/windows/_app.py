"""App subclasses QApplication and provides the main application object. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from PySide6.QtCore import QMargins, QPoint
from PySide6.QtGui import QIcon, QFont, QColor
from PySide6.QtWidgets import QApplication, QMainWindow
from attribox import AttriBox
from icecream import ic
from vistutils.fields import EmptyField
from vistutils.waitaminute import typeMsg

from ezside.app import AppSettings
from ezside.desc import Pen, \
  Black, \
  SolidLine, \
  Brush, \
  Gray, \
  SolidFill, \
  Margins, \
  SpringGreen, \
  Turquoise, \
  SteelBlue, \
  Moccasin, \
  OldLace, \
  FloralWhite, \
  Font, Bold, Normal
from ezside.dialogs import ColorSelection
from ezside.windows import Main, MainWindow
from moreattribox import Wait


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

  def lmao(*args) -> QFont:
    """lmao."""
    family, size, weight = args
    font = QFont()
    font.setFamily(family)
    font.setPointSize(size)
    font.setWeight(weight)
    return font

  pressedEnabledTextFont = Wait('MesloLGS NF', 16, Bold) @ lmao
  hoveredEnabledTextFont = Wait('MesloLGS NF', 16, Bold) @ lmao
  defaultEnabledTextFont = Wait('MesloLGS NF', 12, Normal) @ lmao
  pressedDisabledTextFont = Wait('MesloLGS NF', 12, Normal) @ lmao
  hoveredDisabledTextFont = Wait('MesloLGS NF', 12, Normal) @ lmao
  defaultDisabledTextFont = Wait('MesloLGS NF', 12, Normal) @ lmao

  pressedEnabledTextPen = Pen(Black, 1, SolidLine)
  hoveredEnabledTextPen = Pen(Black, 1, SolidLine)
  defaultEnabledTextPen = Pen(Black, 1, SolidLine)
  pressedDisabledTextPen = Pen(Black.lighter(125), 1, SolidLine)
  hoveredDisabledTextPen = Pen(Black.lighter(125), 1, SolidLine)
  defaultDisabledTextPen = Pen(Black.lighter(125), 1, SolidLine)

  pressedEnabledBackgroundBrush = Brush(SteelBlue, SolidFill)
  hoveredEnabledBackgroundBrush = Brush(Turquoise, SolidFill)
  defaultEnabledBackgroundBrush = Brush(SpringGreen, SolidFill)
  pressedDisabledBackgroundBrush = Brush(Moccasin, SolidFill)
  hoveredDisabledBackgroundBrush = Brush(OldLace, SolidFill)
  defaultDisabledBackgroundBrush = Brush(FloralWhite, SolidFill)

  pressedEnabledMargins = Margins(2, 2, 2, 2, )
  hoveredEnabledMargins = Margins(4, 4, 4, 4, )
  defaultEnabledMargins = Margins(8, 8, 8, 8, )
  pressedDisabledMargins = Margins(4, 4, 4, 4, )
  hoveredDisabledMargins = Margins(4, 4, 4, 4, )
  defaultDisabledMargins = Margins(4, 4, 4, 4, )

  pressedEnabledPadding = Margins(2, 2, 2, 2, )
  hoveredEnabledPadding = Margins(4, 4, 4, 4, )
  defaultEnabledPadding = Margins(8, 8, 8, 8, )
  pressedDisabledPadding = Margins(1, 1, 1, 1, )
  hoveredDisabledPadding = Margins(2, 2, 2, 2, )
  defaultDisabledPadding = Margins(4, 4, 4, 4, )

  pressedEnabledBorders = Margins(16, 16, 16, 16)
  hoveredEnabledBorders = Margins(12, 12, 12, 12, )
  defaultEnabledBorders = Margins(4, 4, 4, 4, )
  pressedDisabledBorders = Margins(3, 3, 3, 3, )
  hoveredDisabledBorders = Margins(2, 2, 2, 2, )
  defaultDisabledBorders = Margins(1, 1, 1, 1, )

  pressedEnabledCornerRadius = QPoint(16, 16)
  hoveredEnabledCornerRadius = QPoint(12, 12)
  defaultEnabledCornerRadius = QPoint(4, 4)
  pressedDisabledCornerRadius = QPoint(8, 8)
  hoveredDisabledCornerRadius = QPoint(6, 6)
  defaultDisabledCornerRadius = QPoint(4, 4)

  def setBackgroundBase(self, color: QColor) -> None:
    """Setter-function for background color"""
    self.pressedEnabledBackgroundBrush.setColor(color.darker(125))
    self.hoveredEnabledBackgroundBrush.setColor(color.darker(110))
    self.defaultEnabledBackgroundBrush.setColor(color)
    self.main.testButton.update()
