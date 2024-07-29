"""This subclass should implement business logic."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QLayoutItem, QApplication

from ezside.app import LayoutWindow


class MainWindow(LayoutWindow):
  """This subclass should implement business logic."""

  def initSignalSlot(self) -> None:
    """Initialize signals and slots."""
    self.pulse.connect(self.mainStatusBar.digitalClock.refreshTime)
    self.aboutQtAction.triggered.connect(QApplication.aboutQt)
    self.timer.start()
    self.debugAction01.triggered.connect(self.debugSlot01)
    self.debugAction02.triggered.connect(self.debugSlot02)
    self.debugAction03.triggered.connect(self.debugSlot03)

  def show(self) -> None:
    """Reimplementation setting up signals and slots before invoking
    parent method."""
    self.initSignalSlot()
    LayoutWindow.show(self)

  def debugSlot01(self) -> None:
    """Debug slot 01"""
    self.statusBar().showMessage('FUCK YOU!')

  def debugSlot02(self, ) -> None:
    """Debug slot 02"""
    item = self.statusBar().layout().itemAt(0)
    innerItem = item.layout()
    print(innerItem.widget())
    print(innerItem.layout())
    print(innerItem.spacerItem())
    print(innerItem.layout().layout().layout())
    print(innerItem.layout() is innerItem.layout().layout())

  def debugSlot03(self) -> None:
    """Debug slot 03"""
    for (key, val) in QLayoutItem.__dict__.items():
      print("""%s: %20s""" % (key, type(val).__name__))
