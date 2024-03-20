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

  def __init__(self, *args, **kwargs) -> None:
    BaseWindow.__init__(self, *args, **kwargs)

  def connectActions(self, ) -> None:
    """Connects the actions to the slots."""
    BaseWindow.connectActions(self)

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(256, 256)
    # self.wrapView.initUi()
    self.testWidget.initUi()
    self.baseLayout.addWidget(self.testWidget)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)
    BaseWindow.initUi(self, )

  def show(self, ) -> None:
    """Shows the window."""
    self.initUi()
    self.connectActions()
    QMainWindow.show(self)

  def debug1Func(self, ) -> None:
    """Debug function."""
    print('Repaints the window')
    self.testWidget.update()

  def debug2Func(self, ) -> None:
    """Debug function."""
    print('Repaints the window')
    self.update()
    print(self.testWidget.geometry())
