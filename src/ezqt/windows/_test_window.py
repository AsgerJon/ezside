"""TestWindow tests widgets one at a time"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QMainWindow
from attribox import AttriBox

from ezqt.windows import BaseWindow
from ezqt.widgets import BaseWidget, DataWidget, Equalizer


# Example usage


class TestWindow(BaseWindow):
  """TestWindow tests widgets one at a time"""

  baseWidget = AttriBox[BaseWidget]()
  baseLayout = AttriBox[QVBoxLayout]()
  wrapView = AttriBox[DataWidget]()
  testWidget = AttriBox[Equalizer]()

  # button = AttriBox[RadioButton]()

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(256, 256)
    # self.wrapView.initUi()
    BaseWindow.initUi(self, )
    self.testWidget.initUi()
    self.baseLayout.addWidget(self.testWidget)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)

  def show(self, ) -> None:
    """Shows the window."""
    self.initUi()
    self.connectActions()
    QMainWindow.show(self)
