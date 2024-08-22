"""BaseWindow subclasses QMainWindow and provides a base window for the
application. It implements menus, menubar and statusbar. It is intended to
be further subclassed to implement widget layout and business logic. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal, Qt, Slot, QSize, QTimer
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QMainWindow, QColorDialog, QFontDialog
from PySide6.QtWidgets import QApplication
from icecream import ic
from worktoy.desc import THIS, AttriBox, Field
from worktoy.text import typeMsg

from ezside.app import StatusBar, MenuBar
from ezside.dialogs import DirectoryDialog, SaveFileDialog, OpenFileDialog, \
  AboutPythonDialog, NewDialog

ic.configureOutput(includeContext=True)


class BaseWindow(QMainWindow):
  """BaseWindow subclasses QMainWindow and provides a base window for the
  application. It implements menus, menubar and statusbar. It is intended to
  be further subclassed to implement widget layout and business logic. """

  __pulse_timer__ = None

  colorWheel = AttriBox[QColorDialog](THIS)
  fontOptions = AttriBox[QFontDialog](THIS)
  openFile = AttriBox[OpenFileDialog](THIS)
  saveFile = AttriBox[SaveFileDialog](THIS)
  selDir = AttriBox[DirectoryDialog](THIS)
  aboutPython = AttriBox[AboutPythonDialog](THIS)
  prevColor = AttriBox[QColor](QColor(255, 255, 255, 255))
  colorSelected = Signal(QColor)
  fontSelected = Signal(QFont)
  directorySelected = Signal(str)
  openFileSelected = Signal(str)
  saveFileSelected = Signal(str)
  pulse = Signal()
  newImage = Signal(NewDialog)
  mainStatusBar = AttriBox[StatusBar](THIS)
  mainMenuBar = AttriBox[MenuBar](THIS)

  pulseTimer = Field()

  def _createPulseTimer(self) -> None:
    """Creator-function for the pulse timer"""
    if self.__pulse_timer__ is None:
      self.__pulse_timer__ = QTimer()
      self.__pulse_timer__.setInterval(250)
      self.__pulse_timer__.setSingleShot(False)
      self.__pulse_timer__.setTimerType(Qt.TimerType.VeryCoarseTimer)

  @pulseTimer.GET
  def _getPulseTimer(self, **kwargs) -> QTimer:
    """Getter-function for the pulse timer"""
    if self.__pulse_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createPulseTimer()
      return self._getPulseTimer(_recursion=True)
    if isinstance(self.__pulse_timer__, QTimer):
      return self.__pulse_timer__
    e = typeMsg('__pulse_timer__', self.__pulse_timer__, QTimer)
    raise TypeError(e)

  def __init__(self, *args) -> None:
    QMainWindow.__init__(self)
    self.setMenuBar(self.mainMenuBar)
    self.setStatusBar(self.mainStatusBar)

  @Slot()
  def requestColor(self) -> None:
    """Triggering this method opens the color dialog. When accepted the
    selected color is emitted through the 'colorSelected' signal. """
    self.colorWheel.show()

  @Slot()
  def requestFont(self) -> None:
    """Triggering this method opens the font selection dialog."""
    self.fontOptions.show()

  @Slot()
  def requestOpenFile(self) -> None:
    """Triggering this method opens a file dialog for opening a file."""
    self.openFile.show()

  @Slot()
  def requestSaveFile(self) -> None:
    """Triggering this method opens a file dialog for saving a file."""
    self.saveFile.show()

  @Slot()
  def requestDir(self) -> None:
    """Triggering this method opens a directory dialog for selecting a
    directory."""
    self.selDir.show()

  @Slot()
  def requestNewFile(self) -> None:
    """Triggering this method starts the 'new' wizard"""
    raise NotImplementedError

  def initSignalSlot(self, ) -> None:
    """Initializes the signal slot connections for the object."""
    #  Connecting pulse to status bar clock
    self.pulseTimer.timeout.connect(self.pulse)
    self.pulse.connect(self.mainStatusBar.digitalClock.refreshTime)
    #  Connecting 'accept' signals from dialogs to relevant slots
    self.colorWheel.colorSelected.connect(self.colorSelected)
    self.fontOptions.fontSelected.connect(self.fontSelected)
    self.selDir.fileSelected.connect(self.directorySelected)
    self.openFile.fileSelected.connect(self.openFileSelected)
    self.saveFile.fileSelected.connect(self.saveFileSelected)
    #  Implementing 'about' actions to relevant information dialogs
    self.mainMenuBar.helpMenu.aboutQtAction.triggered.connect(
        QApplication.aboutQt)
    self.mainMenuBar.helpMenu.aboutPythonAction.triggered.connect(
        self.aboutPython.show)
    self.mainMenuBar.fileMenu.exitAction.triggered.connect(self.close)
    self.mainMenuBar.fileMenu.newAction.triggered.connect(
        self.requestNewFile)
    self.mainMenuBar.fileMenu.openAction.triggered.connect(
        self.requestOpenFile)
    self.mainMenuBar.fileMenu.saveAsAction.triggered.connect(
        self.requestSaveFile)
    #  Starting timers
    self.pulseTimer.start()
