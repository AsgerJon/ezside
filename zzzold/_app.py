"""App subclasses the QApplication class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, Signal, Slot, QRect
from PySide6.QtWidgets import QApplication
from icecream import ic

from ezside.app import Settings
from ezside.core import EZTimer, Precise
from ezside.windows import MainDesc, MainWindow

ic.configureOutput(includeContext=True, )

MenuFlag = Qt.ApplicationAttribute.AA_DontUseNativeMenuBar

if TYPE_CHECKING:
  pass


class App(QApplication):
  """App is a subclass of QApplication."""

  __fallback_geometry__ = QRect(100, 100, 800, 600)
  __pulse_count__ = 0

  settings = Settings()
  main = MainDesc(MainWindow)

  pulseTimer = EZTimer(125, Precise, singleShot=False)

  pulse8Hz = Signal()
  pulse4Hz = Signal()
  pulse2Hz = Signal()
  pulse1Hz = Signal()

  stopThreads = Signal()
  threadsStopped = Signal()

  def _handlePulse(self, ) -> None:
    """Handle the pulse."""
    self.pulse8Hz.emit()
    if not self.__pulse_count__ % 2:
      self.pulse4Hz.emit()
    if not self.__pulse_count__ % 4:
      self.pulse2Hz.emit()
    if not self.__pulse_count__ % 8:
      self.pulse1Hz.emit()
    self.__pulse_count__ += 1
    self.__pulse_count__ %= 8

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the App instance."""
    strArgs = [arg for arg in args if isinstance(arg, str)]
    QApplication.__init__(self, strArgs)
    self.setStyle('Fusion')
    self.setAttribute(MenuFlag, True)
    self.setOrganizationName('EZ')
    self.setApplicationName('EZSide')

  def initUi(self, ) -> None:
    """Initialize the user interface."""

  def initSignalSlot(self, ) -> None:
    """This method connects signals and slots internal to the application
    instance enabling the external signals and slots. """
    self.pulseTimer.timeout.connect(self._handlePulse)

  def exec(self) -> int:
    """Executes the application."""
    fb = self.__fallback_geometry__
    try:
      winGeometry = self.settings.value('window/geometry', fb=fb)
    except KeyError:
      self.settings.setValue('window/geometry', fb)
      winGeometry = fb
    if isinstance(winGeometry, QRect):
      self.main.setGeometry(winGeometry)
    self.main.setWindowIcon(self.settings.value('icon/pogchamp'))
    self.main.show()
    retCode = super().exec()
    if not retCode:
      self.settings.setValue('window/geometry', self.main.geometry())
    return retCode
