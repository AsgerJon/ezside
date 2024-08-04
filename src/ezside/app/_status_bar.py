"""StatusBar subclasses QStatusBar providing the status bar for the main
window application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QStatusBar, QMainWindow, QHBoxLayout, QLabel
from icecream import ic
from worktoy.desc import AttriBox, THIS

from ezside.widgets import DigitalClock

ic.configureOutput(includeContext=True)


class StatusBar(QStatusBar):
  """StatusBar subclasses QStatusBar providing the status bar for the main
  window application."""

  digitalClock = AttriBox[DigitalClock](THIS, )

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, QMainWindow):
        QStatusBar.__init__(self, arg)
        break
    else:
      QStatusBar.__init__(self)
    self.addPermanentWidget(self.digitalClock)
    self.digitalClock.refreshTime()
    self.setStyleSheet(
        """
        QStatusBar {
          background-color: #AAAAAA;
          color: #FF0000;
          font-size: 14px;
        }  
        """
    )

  def showEvent(self, event: QShowEvent) -> None:
    """Show the main window."""
    QMainWindow.showEvent(self, event)
    print('%s - Show event' % self.__class__.__name__)

  @Slot()
  def refreshTime(self) -> None:
    """This slot refreshes the time on the clock"""
    self.digitalClock.refreshTime()

  @Slot(str)
  def echo(self, msg: str) -> None:
    """This slot shows the message on the status bar."""
    self.showMessage(msg, 5000)

  def echoFactory(self, msg: str) -> Callable:
    """This method creates a slot that shows the message on the status
    bar."""

    @Slot()
    def _echo() -> None:
      self.showMessage(msg, 5000)

    return _echo
