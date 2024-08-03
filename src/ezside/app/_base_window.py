"""BaseWindow subclasses QMainWindow and provides a base window for the
application. It implements menus, menubar and statusbar. It is intended to
be further subclassed to implement widget layout and business logic. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

from PySide6.QtCore import QSize, Signal, QTimer, Qt
from PySide6.QtGui import QPixmap, QIcon, QKeySequence, QShowEvent
from PySide6.QtWidgets import QMainWindow, QMenuBar, QStatusBar
from worktoy.desc import AttriBox

from ezside.app import StatusBar
from ezside.tools import Timer


class BaseWindow(QMainWindow):
  """BaseWindow subclasses QMainWindow and provides a base window for the
  application. It implements menus, menubar and statusbar. It is intended to
  be further subclassed to implement widget layout and business logic. """

  pulse = Signal()
  timer = AttriBox[Timer](Qt.TimerType.PreciseTimer, 500, False)
  mainStatusBar = AttriBox[StatusBar]()

  @classmethod
  def _getIcon(cls, menu: str) -> QIcon:
    """Returns the file icon"""
    here = os.path.dirname(os.path.abspath(__file__))
    iconPath = os.path.join(here, 'icons', '%s.png' % menu.lower())
    pix = QPixmap(iconPath)
    icon = QIcon(pix)
    return icon

  def __init__(self, ) -> None:
    QMainWindow.__init__(self, )
    self.setWindowTitle('EZSide')
    self.setMinimumSize(QSize(480, 320))
    self.setMenuBar(QMenuBar())
    self.setStatusBar(self.mainStatusBar)
    self.fileMenu = self.menuBar().addMenu('File')
    self.editMenu = self.menuBar().addMenu('Edit')
    self.helpMenu = self.menuBar().addMenu('Help')
    self.debugMenu = self.menuBar().addMenu('Debug')
    self.newAction = self.fileMenu.addAction('New')
    self.newAction.setIcon(self._getIcon('new'))
    self.newAction.setShortcut(QKeySequence.fromString('CTRL+N'))
    self.newAction.triggered.connect(self.mainStatusBar.echoFactory('New'))
    self.openAction = self.fileMenu.addAction('Open')
    self.openAction.setIcon(self._getIcon('open'))
    self.openAction.setShortcut(QKeySequence.fromString('CTRL+O'))
    self.saveAction = self.fileMenu.addAction('Save')
    self.saveAction.setIcon(self._getIcon('save'))
    self.saveAction.setShortcut(QKeySequence.fromString('CTRL+S'))
    self.saveAsAction = self.fileMenu.addAction('Save As')
    self.saveAsAction.setIcon(self._getIcon('save_as'))
    self.saveAsAction.setShortcut(QKeySequence.fromString('CTRL+SHIFT+S'))
    self.exitAction = self.fileMenu.addAction('Exit')
    self.exitAction.setIcon(self._getIcon('exit'))
    self.exitAction.setShortcut(QKeySequence.fromString('ALT+F4'))
    self.copyAction = self.editMenu.addAction('Copy')
    self.copyAction.setIcon(self._getIcon('copy'))
    self.copyAction.setShortcut(QKeySequence.fromString('CTRL+C'))
    self.cutAction = self.editMenu.addAction('Cut')
    self.cutAction.setIcon(self._getIcon('cut'))
    self.cutAction.setShortcut(QKeySequence.fromString('CTRL+X'))
    self.pasteAction = self.editMenu.addAction('Paste')
    self.pasteAction.setIcon(self._getIcon('paste'))
    self.pasteAction.setShortcut(QKeySequence.fromString('CTRL+V'))
    self.aboutQtAction = self.helpMenu.addAction('About Qt')
    self.aboutQtAction.setIcon(self._getIcon('about_qt'))
    self.aboutQtAction.setShortcut(QKeySequence.fromString('F12'))
    self.debugAction01 = self.debugMenu.addAction('DEBUG 01')
    self.debugAction01.setIcon(self._getIcon('risitas'))
    self.debugAction01.setShortcut(QKeySequence.fromString('F1'))
    self.debugAction02 = self.debugMenu.addAction('DEBUG 02')
    self.debugAction02.setIcon(self._getIcon('risitas'))
    self.debugAction02.setShortcut(QKeySequence.fromString('F2'))
    self.debugAction03 = self.debugMenu.addAction('DEBUG 03')
    self.debugAction03.setIcon(self._getIcon('risitas'))
    self.debugAction03.setShortcut(QKeySequence.fromString('F3'))
    self.debugAction04 = self.debugMenu.addAction('DEBUG 04')
    self.debugAction04.setIcon(self._getIcon('risitas'))
    self.debugAction04.setShortcut(QKeySequence.fromString('F4'))
    self.debugAction05 = self.debugMenu.addAction('DEBUG 05')
    self.debugAction05.setIcon(self._getIcon('risitas'))
    self.debugAction05.setShortcut(QKeySequence.fromString('F5'))
    self.debugAction06 = self.debugMenu.addAction('DEBUG 06')
    self.debugAction06.setIcon(self._getIcon('risitas'))
    self.debugAction06.setShortcut(QKeySequence.fromString('F6'))
    self.debugAction07 = self.debugMenu.addAction('DEBUG 07')
    self.debugAction07.setIcon(self._getIcon('risitas'))
    self.debugAction07.setShortcut(QKeySequence.fromString('F7'))
    self.debugAction08 = self.debugMenu.addAction('DEBUG 08')
    self.debugAction08.setIcon(self._getIcon('risitas'))
    self.debugAction08.setShortcut(QKeySequence.fromString('F8'))
    self.debugAction09 = self.debugMenu.addAction('DEBUG 09')
    self.debugAction09.setIcon(self._getIcon('risitas'))
    self.debugAction09.setShortcut(QKeySequence.fromString('F9'))
    self.timer.timeout.connect(self.pulse.emit)

  def show(self) -> None:
    """Reimplementation setting up signals and slots before invoking
    parent method."""
    QMainWindow.show(self)

  def showEvent(self, event: QShowEvent) -> None:
    """Show the main window."""
    QMainWindow.showEvent(self, event)
    print('%s - Show event' % self.__class__.__name__)
