"""MainWindow subclasses the LayoutWindow and provides the main
application business logic."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QApplication
from icecream import ic
from attribox import AttriBox

from ezside.windows.bars import MenuBar, StatusBar
from ezside.core import Precise
from ezside.widgets import Timer
from ezside.windows import LayoutWindow
from ezside.settings import Default

ic.configureOutput(includeContext=True, )


class MainWindow(LayoutWindow):
  """MainWindow subclasses the LayoutWindow and provides the main
  application business logic."""

  paintTimer = AttriBox[Timer](Default.paintTimer, Precise, False)

  @Slot()
  def stopHandle(self, ) -> None:
    """Handles the stop button"""

  @Slot()
  def startHandle(self, ) -> None:
    """Handles the start button"""

  def applyView(self, ) -> None:
    """Applies the view to the data widget."""
    values = self.plotEnvelope.getValues()

    self.dataWidget.dataView.chart().axisX().setMin(values.get('minH'))
    self.dataWidget.dataView.chart().axisY().setMin(values.get('minV'))
    self.dataWidget.dataView.chart().axisX().setMax(values.get('maxH'))
    self.dataWidget.dataView.chart().axisY().setMax(values.get('maxV'))
    self.dataWidget.dataView.refresh()

  def connectActions(self, ) -> None:
    """Connects the actions to the slots."""
    # self.mainMenuBar.debug.debug1.triggered.connect(self.debug1Func)
    # self.mainMenuBar.debug.debug2.triggered.connect(self.debug2Func)
    # self.mainMenuBar.debug.debug3.triggered.connect(self.debug3Func)
    # self.mainMenuBar.addSeparator()
    # self.mainMenuBar.debug.debug4.triggered.connect(self.debug4Func)
    # self.mainMenuBar.debug.debug5.triggered.connect(self.debug5Func)
    # self.mainMenuBar.debug.debug6.triggered.connect(self.debug6Func)
    # self.mainMenuBar.addSeparator()
    # self.mainMenuBar.debug.debug7.triggered.connect(self.debug7Func)
    # self.mainMenuBar.debug.debug8.triggered.connect(self.debug8Func)
    # self.mainMenuBar.debug.debug9.triggered.connect(self.debug9Func)
    self.mainMenuBar.help.about_qt.triggered.connect(QApplication.aboutQt)
    self.mainMenuBar.files.exit.triggered.connect(self.close)
    self.whiteNoise.noise.connect(self.dataWidget.dataView.append)
    self.dataWidget.start.connect(self.startHandle)
    self.dataWidget.stop.connect(self.stopHandle)
    self.paintTimer.timeout.connect(self.dataWidget.refresh)
    self.plotEnvelope.newValues.connect(self.applyView)
    self.paintTimer.start()

  def show(self) -> None:
    """Show the window."""
    self.initUi()
    self.mainMenuBar = MenuBar(self)
    self.mainMenuBar.initUi()
    self.setMenuBar(self.mainMenuBar)
    ic(self.menuBar())
    self.mainStatusBar = StatusBar(self)
    self.mainStatusBar.initUi()
    self.setStatusBar(self.mainStatusBar)
    self.connectActions()
    QMainWindow.show(self)
