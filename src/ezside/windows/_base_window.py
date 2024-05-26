"""BaseWindow provides the base class for the main application window. It
implements menus and actions for the application, leaving widgets for the
LayoutWindow class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import QAction, QDesktopServices, QColor, QFont
from PySide6.QtWidgets import QMenu, QApplication
from icecream import ic

from ezside.dialogs import ColorSelection, FontSelection
from ezside.menus import MenuBar, StatusBar
from ezside.windows import CoreWindow

ic.configureOutput(includeContext=True)


class BaseWindow(CoreWindow):
  """BaseWindow class provides menus and actions for the application."""

  mainMenuBar = MenuBar()
  mainStatusBar = StatusBar()
  selectColor = ColorSelection()
  selectFont = FontSelection()

  backgroundSelection = ColorSelection()

  file: QMenu
  edit: QMenu
  help: QMenu
  new: QAction
  open: QAction
  save: QAction
  saveAs: QAction
  exit: QAction
  undo: QAction
  redo: QAction
  cut: QAction
  copy: QAction
  paste: QAction
  aboutQt: QAction
  aboutPySide6: QAction
  aboutPython: QAction
  aboutConda: QAction
  debug01: QAction
  debug02: QAction

  @staticmethod
  def openUrlFactory(url: str) -> Callable:
    """Opens a URL in the default browser."""

    def callMeMaybe() -> None:
      """Opens the URL."""
      QDesktopServices.openUrl(QUrl(url))

    return callMeMaybe

  def initMenus(self) -> None:
    """Initializes the menus."""
    self.mainMenuBar.initUi()
    self.mainStatusBar.initUi()
    self.setMenuBar(self.mainMenuBar)
    self.setStatusBar(self.mainStatusBar)

  def initActions(self) -> None:
    """Initializes the actions."""
    self.aboutQt.triggered.connect(QApplication.aboutQt)
    self.aboutPySide6.triggered.connect(
      self.openUrlFactory("https://doc.qt.io/qtforpython/"))
    self.aboutPython.triggered.connect(
      self.openUrlFactory("https://www.python.org/"))
    self.aboutConda.triggered.connect(
      self.openUrlFactory("https://docs.conda.io/en/latest/"))
    self.new.triggered.connect(self.newSlot)
    # self.debug01.triggered.connect(self.selectColor.show)
    self.debug02.triggered.connect(self.selectFont.show)
    self.selectFont.fontSelected.connect(self.onFontSelected)
    self.selectColor.colorSelected.connect(self.onColorSelected)
    self.debug01.triggered.connect(self.backgroundSelection.show)
    self.backgroundSelection.colorSelected.connect(
      self.app.setBackgroundBase)

  @Slot()
  def newSlot(self, ) -> None:
    """Slot for creating a new file."""

  @Slot()
  def openSlot(self, ) -> None:
    """Slot responsible for opening the file selection dialog."""

  @Slot(str)
  def onOpenFileSelected(self, openFile: str) -> None:
    """Slot for handling selected open file. """

  @Slot()
  def saveSlot(self, ) -> None:
    """Slot responsible for opening the save file selection dialog."""

  @Slot(str)
  def onSaveFileSelected(self, saveFile: str) -> None:
    """Slot responsible for handling the selected save file."""

  @Slot()
  def selectFolderSlot(self, ) -> None:
    """Slot responsible for opening the folder selection dialog."""

  @Slot(str)
  def onFolderSelected(self, selectFolder: str) -> None:
    """Slot responsible for handling the selected folder."""

  @Slot()
  def exitSlot(self, ) -> None:
    """Slot for exiting the application."""

  def undoSlot(self, ) -> None:
    """Slot for undoing the last action."""

  def redoSlot(self, ) -> None:
    """Slot for redoing the last action."""

  def cutSlot(self, ) -> None:
    """Slot for cutting the selected text."""

  def copySlot(self, ) -> None:
    """Slot for copying the selected text."""

  def pasteSlot(self, ) -> None:
    """Slot for pasting the selected text."""

  def openColorSelection(self) -> None:
    """Opens the color selection dialog."""

  @Slot(QColor)
  def onColorSelected(self, color: QColor) -> None:
    """Slot for when a color is selected."""

  def openFontSelection(self) -> None:
    """Opens the font selection dialog."""

  @Slot(QFont)
  def onFontSelected(self, font: QFont) -> None:
    """Slot for when a font is selected."""
