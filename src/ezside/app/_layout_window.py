"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QSize
from attribox import AttriBox
from icecream import ic

from ezside.app import BaseWindow
from ezside.widgets import Label, DigitalClock
from ezside.widgets.layouts import VerticalLayout
from morevistutils import Bag

ic.configureOutput(includeContext=True, )


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and implements the layout of
  widgets."""

  baseLayout = AttriBox[VerticalLayout]()
  welcomeLabel = Label @ Bag('YOLO!')

  def initStyle(self) -> None:
    """The initStyle method initializes the style of the window and the
    widgets on it, before 'initUi' sets up the layout. """

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(QSize(640, 480))
    self.baseLayout.addWidget(self.welcomeLabel)
    self.baseLayout.initUi()

  @abstractmethod  # MainWindow
  def initSignalSlot(self) -> None:
    """The initActions method initializes the actions of the window."""
