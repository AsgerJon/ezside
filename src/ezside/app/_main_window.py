"""This subclass should implement business logic."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

from PySide6.QtCore import QMargins, QRectF, QPointF, QSizeF
from PySide6.QtGui import QColor, QFont, QFontDatabase
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from icecream import ic
from pyperclip import copy

from ezside.app import LayoutWindow
from ezside.tools import SizeRule, MarginsBox

ic.configureOutput(includeContext=True)


class MainWindow(LayoutWindow):
  """This subclass should implement business logic."""

  def initSignalSlot(self) -> None:
    """Initialize signals and slots."""
    LayoutWindow.initSignalSlot(self)
    self.mainMenuBar.debugMenu.debugAction02.triggered.connect(
        self.debug02)
    self.mainMenuBar.debugMenu.debugAction03.triggered.connect(
        self.debug03)
    self.mainMenuBar.debugMenu.debugAction04.triggered.connect(
        self.debug04)
    self.mainMenuBar.debugMenu.debugAction05.triggered.connect(
        self.debug05)
    self.mainMenuBar.debugMenu.debugAction06.triggered.connect(
        self.debug06)
    self.mainMenuBar.debugMenu.debugAction07.triggered.connect(
        self.debug07)

  def show(self) -> None:
    """Reimplementation setting up signals and slots before invoking
    parent method."""
    self.initLayout()
    self.initSignalSlot()
    self.adjustSize()
    QMainWindow.show(self)

  def about(self) -> None:
    """Displays information about Python."""
    title = """About Python"""
    v = sys.version_info
    msg = """Python version: %d.%d.%d""" % (v.major, v.minor, v.micro)
    QMessageBox.about(self, title, msg)

  def updateLabelColor(self, color: QColor) -> None:
    """Updates the color of the label."""
    self.headerLabel.backgroundColor = color
    self.headerLabel.update()

  def debug02(self) -> None:
    """Testing label size change"""
    self.headerLabel.fontSize -= 1
    self.headerLabel.adjustSize()
    self.headerLabel.update()

  def debug03(self) -> None:
    """Testing label size change"""
    self.headerLabel.fontSize += 1
    self.headerLabel.adjustSize()
    self.headerLabel.update()

  def debug04(self) -> None:
    """Testing label size change"""
    innerMargins = QMargins(5, 5, 5, 5)
    self.mainStatusBar.showMessage(str(innerMargins))

  def debug05(self) -> None:
    """Testing label size change"""
    outerMargins = QMargins(7, 7, 7, 7, )
    self.mainStatusBar.showMessage(str(outerMargins))

  def debug06(self) -> None:
    """Testing label size change"""
    innerMargins = QMargins(5, 5, 5, 5)
    outerMargins = QMargins(7, 7, 7, 7, )
    sumOfMargins = innerMargins + outerMargins
    self.mainStatusBar.showMessage(str(sumOfMargins))

  def debug07(self) -> None:
    """Testing SizeRule"""

    class LMAO:
      margins = MarginsBox(1)

      def __str__(self) -> str:
        left = self.margins.left()
        top = self.margins.top()
        right = self.margins.right()
        bottom = self.margins.bottom()
        out = """Left: %d, Top: %d, Right: %d, Bottom: %d"""
        return out % (left, top, right, bottom)

    rect = QRectF(QPointF(0, 0), QSizeF(100, 100))
    print(rect.size())
    rect += LMAO().margins
    print(rect.size())
