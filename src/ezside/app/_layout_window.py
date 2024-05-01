"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtGui import QFontDatabase
from attribox import AttriBox
from icecream import ic

from ezside.widgets import BaseWidget, Grid, Vertical, Horizontal, BaseLabel
from ezside.app import BaseWindow

ic.configureOutput(includeContext=True, )


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and implements the layout of
  widgets."""

  baseLayout = AttriBox[Vertical]()
  baseWidget = AttriBox[BaseWidget]()
  welcomeLabel = AttriBox[BaseLabel]('YOLO')

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.baseLayout.addWidget(self.welcomeLabel)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)

  @abstractmethod
  def initActions(self) -> None:
    """The initActions method initializes the actions of the window."""

  def debug2Func(self, ) -> None:
    """Debug2Func prints a debug message to the console."""
    BaseWindow.debug2Func(self)
    fontDatabase = QFontDatabase()
    allFonts = fontDatabase.families()
    for font in allFonts:
      print(font)
