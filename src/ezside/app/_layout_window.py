"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QVBoxLayout
from attribox import AttriBox
from icecream import ic

from ezside.app import BaseWindow
from ezside.widgets import BaseWidget, Label

ic.configureOutput(includeContext=True, )


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and implements the layout of
  widgets."""

  baseLayout = AttriBox[QVBoxLayout]()
  baseWidget = AttriBox[BaseWidget]()
  welcomeLabel = AttriBox[Label]('YOLO')

  def initStyle(self) -> None:
    """The initStyle method initializes the style of the window and the
    widgets on it, before 'initUi' sets up the layout. """

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(QSize(320, 240))
    self.baseLayout.addWidget(self.welcomeLabel)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)

  @abstractmethod  # MainWindow
  def initSignalSlot(self) -> None:
    """The initActions method initializes the actions of the window."""
