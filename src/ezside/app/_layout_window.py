"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QGridLayout
from attribox import AttriBox
from ezside.widgets import BaseWidget, \
  Vertical, \
  Label, \
  LineEdit, \
  Button, \
  VerticalSpacer, EntryForm, HorizontalSpacer, Horizontal, VerticalSlider
from icecream import ic

from ezside.core import LawnGreen, VERTICAL, HORIZONTAL
from ezside.app import BaseWindow

ic.configureOutput(includeContext=True, )


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and implements the layout of
  widgets."""

  baseWidget = AttriBox[BaseWidget]()
  vLayout = AttriBox[Vertical]()
  hLayout = AttriBox[Horizontal]()
  hWidget = AttriBox[BaseWidget]()
  welcomeLabel = AttriBox[Label]('Welcome to EZSide!')
  vSlider1 = AttriBox[VerticalSlider]('low')
  vSlider2 = AttriBox[VerticalSlider]('high')

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.hLayout.addWidget(self.vSlider1)
    self.hLayout.addWidget(self.vSlider2)
    self.hWidget.setLayout(self.hLayout)
    self.vLayout.addWidget(self.welcomeLabel)
    self.vLayout.addWidget(self.hWidget)
    self.baseWidget.setLayout(self.vLayout)
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
