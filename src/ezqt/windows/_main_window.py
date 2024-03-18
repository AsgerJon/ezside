"""MainWindow subclasses the LayoutWindow and provides the main
application business logic."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication
from icecream import ic

from attribox import AttriBox
from ezqt.core import Precise
from ezqt.widgets import Timer
from ezqt.windows import LayoutWindow

ic.configureOutput(includeContext=True, )


class MainWindow(LayoutWindow):
  """MainWindow subclasses the LayoutWindow and provides the main
  application business logic."""

  paintTimer = AttriBox[Timer](20, Precise, False)

  def __init__(self, *args, **kwargs) -> None:
    LayoutWindow.__init__(self, *args, **kwargs)
    self.setWindowTitle('EZQt')
    for arg in args:
      if isinstance(arg, str):
        self.titleBanner.setText(arg)
        break
    else:
      self.titleBanner.setText('EZQt')

  def initUi(self) -> None:
    """Initializes the user interface for the main window."""
    LayoutWindow.initUi(self)
    self.connectActions()
    self.setMenuBar(self.mainMenuBar)

  def connectActions(self, ) -> None:
    """Connects the actions to the slots."""
    LayoutWindow.connectActions(self)
    self.mainMenuBar.help.about_qt.triggered.connect(QApplication.aboutQt)
    self.mainMenuBar.files.exit.triggered.connect(self.close)
    self.noise.startButton.clicked.connect(self.startHandle)
    self.noise.stopButton.clicked.connect(self.stopHandle)
    self.noise.timer.timeout.connect(self.noise.emitNoise)
    self.noise.noise.connect(self.dataWidget.dataView.data.append)
    self.paintTimer.timeout.connect(self.dataWidget.dataView.refresh)
    self.paintTimer.start()

  def stopHandle(self, ) -> None:
    """Handles the stop button"""
    self.noise.timer.stop()
    self.noise.startButton.setEnabled(True)
    self.noise.stopButton.setEnabled(False)

  def startHandle(self, ) -> None:
    """Handles the start button"""
    self.noise.timer.start()
    self.noise.startButton.setEnabled(False)
    self.noise.stopButton.setEnabled(True)

  def debug1Func(self, ) -> None:
    """Debug function 1"""
    self.dataWidget.dataView.dataChart.axes()[1].setRange(-2, 2)

  def debug2Func(self, ) -> None:
    """Debug function 2"""
    self.dataWidget.dataView.dataChart.axes()[0].setRange(-1, 1)

  def debug3Func(self, ) -> None:
    """Debug function 3"""
    for a in self.dataWidget.dataView.dataChart.axes():
      self.dataWidget.dataView.dataChart.removeAxis(a)

  def debug4Func(self, ) -> None:
    """Debug function 4"""
    self.dataWidget.dataView.dataChart.createDefaultAxes()
