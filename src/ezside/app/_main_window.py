"""This subclass should implement business logic."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize, QEvent
from PySide6.QtGui import QPointerEvent, QMouseEvent
from icecream import ic

from ezside.app import LayoutWindow

ic.configureOutput(includeContext=True)


class MainWindow(LayoutWindow):
  """This subclass should implement business logic."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the object"""
    LayoutWindow.__init__(self, *args, **kwargs)
    self.setMinimumSize(QSize(480, 240))

  def initSignalSlot(self, ) -> None:
    """Initializes the signal-slot connections"""
    print('MainWindow.initSignalSlot')
    LayoutWindow.initSignalSlot(self)
    self.mainMenuBar.debugMenu.debugAction02.triggered.connect(self.debug02)
    self.mainMenuBar.debugMenu.debugAction03.triggered.connect(self.debug03)
    self.mainMenuBar.debugMenu.debugAction04.triggered.connect(self.debug04)
    self.mainMenuBar.debugMenu.debugAction05.triggered.connect(self.debug05)
    self.mainMenuBar.debugMenu.debugAction06.triggered.connect(self.debug06)
    self.mainMenuBar.debugMenu.debugAction07.triggered.connect(self.debug07)
    self.mainMenuBar.debugMenu.debugAction08.triggered.connect(self.debug08)
    self.clickMe.singleClick.connect(self.singleClick)
    self.clickMe.doubleClick.connect(self.doubleClick)
    self.clickMe.tripleClick.connect(self.tripleClick)
    self.clickMe.singleHold.connect(self.singleHold)
    self.clickMe.doubleHold.connect(self.doubleHold)
    self.clickMe.tripleHold.connect(self.tripleHold)

  def singleClick(self, pointerEvent: QPointerEvent) -> None:
    """Single click event"""
    if isinstance(pointerEvent, QMouseEvent):
      button = pointerEvent.buttons()
      return self.statusBar().showMessage('Single click: %s' % str(button))
    e = 'The pointerEvent is not a QMouseEvent: %s!'
    raise TypeError(e % str(QEvent.type(pointerEvent)))

  def doubleClick(self, pointerEvent: QPointerEvent) -> None:
    """Double click event"""
    if isinstance(pointerEvent, QMouseEvent):
      button = pointerEvent.buttons()
      return self.statusBar().showMessage('Double click: %s' % str(button))
    e = 'The pointerEvent is not a QMouseEvent: %s!'
    raise TypeError(e % str(QEvent.type(pointerEvent)))

  def tripleClick(self, pointerEvent: QPointerEvent) -> None:
    """Triple click event"""
    if isinstance(pointerEvent, QMouseEvent):
      button = pointerEvent.buttons()
      return self.statusBar().showMessage('Triple click: %s' % str(button))
    e = 'The pointerEvent is not a QMouseEvent: %s!'
    raise TypeError(e % str(QEvent.type(pointerEvent)))

  def singleHold(self, pointerEvent: QPointerEvent) -> None:
    """Single hold event"""
    if isinstance(pointerEvent, QMouseEvent):
      button = pointerEvent.buttons()
      return self.statusBar().showMessage('Single hold: %s' % str(button))
    e = 'The pointerEvent is not a QMouseEvent: %s!'
    raise TypeError(e % str(QEvent.type(pointerEvent)))

  def doubleHold(self, pointerEvent: QPointerEvent) -> None:
    """Double hold event"""
    if isinstance(pointerEvent, QMouseEvent):
      button = pointerEvent.buttons()
      return self.statusBar().showMessage('Double hold: %s' % str(button))
    e = 'The pointerEvent is not a QMouseEvent: %s!'
    raise TypeError(e % str(QEvent.type(pointerEvent)))

  def tripleHold(self, pointerEvent: QPointerEvent) -> None:
    """Triple hold event"""
    if isinstance(pointerEvent, QMouseEvent):
      button = pointerEvent.buttons()
      return self.statusBar().showMessage('Triple hold: %s' % str(button))
    e = 'The pointerEvent is not a QMouseEvent: %s!'
    raise TypeError(e % str(QEvent.type(pointerEvent)))

  def debug02(self) -> None:
    """Debug action 02"""
    self.statusBar().showMessage('Debug action 02')

  def debug03(self) -> None:
    """Debug action 03"""
    self.statusBar().showMessage('Debug action 03')

  def debug04(self) -> None:
    """Debug action 04"""
    self.statusBar().showMessage('Debug action 04')

  def debug05(self) -> None:
    """Debug action 05"""
    self.statusBar().showMessage('Debug action 05')

  def debug06(self) -> None:
    """Debug action 06"""
    self.statusBar().showMessage('Debug action 06')

  def debug07(self) -> None:
    """Debug action 07"""
    self.statusBar().showMessage('Debug action 07')

  def debug08(self) -> None:
    """Debug action 08"""
    self.statusBar().showMessage('Debug action 08')

  def debug09(self) -> None:
    """Debug action 09"""
    self.statusBar().showMessage('Debug action 09')

  #
  # def initSignalSlot(self, ) -> None:
  #   """Initializes the signal-slot connections"""
  #   LayoutWindow.initSignalSlot(self)
  # self.testButton.singleClickTimer.connect(self.testSingleClick)
  # self.testButton.doubleClickTimer.connect(self.testDoubleClick)
  # self.testButton.tripleClickTimer.connect(self.testTripleClick)
  # self.testButton.singleHold.connect(self.testSingleHold)
  # self.testButton.doubleHold.connect(self.testDoubleHold)
  # self.testButton.tripleHold.connect(self.testTripleHold)
  # self.mainMenuBar.debugMenu.debugAction02.triggered.connect(
  #     self.debug02)

  # self.openFileSelected.connect(self.imgEdit.openImage)
  # self.saveFileSelected.connect(self.imgEdit.saveImage)
  # self.imgEdit.contextMenu.selectColor.triggered.connect(
  #     self.requestColor)
  # self.colorSelected.connect(self.imgEdit.setPaintColor)
