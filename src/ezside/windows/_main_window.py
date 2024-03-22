"""MainWindow subclasses the LayoutWindow and provides the main
application business logic."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow
from icecream import ic
from attribox import AttriBox

from ezside.core import Precise
from ezside.widgets import Timer
from ezside.windows import LayoutWindow
from settings import Default

ic.configureOutput(includeContext=True, )


class MainWindow(LayoutWindow):
  """MainWindow subclasses the LayoutWindow and provides the main
  application business logic."""

  paintTimer = AttriBox[Timer](Default.paintTimer, Precise, False)

  def __init__(self, *args, **kwargs) -> None:
    LayoutWindow.__init__(self, *args, **kwargs)
    for arg in args:
      if isinstance(arg, str):
        self.titleBanner.setText(arg)
        break
    else:
      self.titleBanner.setText('EZQt')

  def connectActions(self, ) -> None:
    """Connects the actions to the slots."""
    LayoutWindow.connectActions(self)
    self.whiteNoise.noise.connect(self.dataWidget.dataView.append)
    self.dataWidget.start.connect(self.startHandle)
    self.dataWidget.stop.connect(self.stopHandle)
    self.paintTimer.timeout.connect(self.dataWidget.refresh)
    self.plotEnvelope.newValues.connect(self.applyView)
    self.paintTimer.start()

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

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    LayoutWindow.initUi(self, )

  def show(self, ) -> None:
    """Shows the window."""
    self.initUi()
    self.connectActions()
    QMainWindow.show(self)
