"""BaseWindow subclasses QMainWindow providing the base window functions."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget

from worktoy.text import typeMsg
from worktoy.desc import AttriBox, THIS
from . import MenuBar, StatusBar
from .dialogs import ConfirmationDialog


class _ConfirmExitDialog(ConfirmationDialog):
  """The _ConfirmExitDialog class subclasses ConfirmationDialog to provide a
  dialog for confirming the exit of the application."""

  def __init__(self, parent: QWidget = None) -> None:
    ConfirmationDialog.__init__(self, parent)
    self.textWidget.label.text = 'Are you sure you want to exit?'


class BaseWindow(QMainWindow):
  """BaseWindow subclasses QMainWindow providing the base window
  functions."""

  isClosing = AttriBox[bool](False)

  confirmExitDialog = AttriBox[_ConfirmExitDialog](THIS)
  menus = AttriBox[MenuBar]('Menus', THIS)
  status = AttriBox[StatusBar]('Status', THIS)

  def __init__(self, *args) -> None:
    QMainWindow.__init__(self)

  def initBars(self, ) -> None:
    """The BaseWindow class provides menu and status bars."""
    self.menus.initMenus()
    self.setMenuBar(self.menus)
    self.status.initUi()
    self.setStatusBar(self.status)

  def _initBaseLogic(self, ) -> None:
    """The _initBaseLogic method provides the base logic for the window."""
    self.menus.helpMenu.aboutQtAction.triggered.connect(QApplication.aboutQt)
    self.menus.fileMenu.exitAction.triggered.connect(self.beginShutdown)
    self.confirmExitDialog.rejected.connect(self.cancelShutdown)
    self.confirmExitDialog.accepted.connect(self.shutdown)

  @abstractmethod
  def initUi(self, ) -> None:
    """Subclasses must provide the initUi method to provide layouts and
    widgets."""

  @abstractmethod
  def initLogic(self, ) -> None:
    """Subclasses must provide the initLogic method to provide the logic for
    the window."""

  @Slot()
  def beginShutdown(self, ) -> None:
    """This method is called to begin the shutdown process."""
    self.isClosing = True
    self.status.showMessage("""Awaiting confirmation to exit.""")
    self.confirmExitDialog.show()

  @Slot()
  def cancelShutdown(self) -> None:
    """This method is called to cancel the shutdown process."""
    self.status.showMessage("""Cancelled exit.""", 5000)
    self.isClosing = False

  @Slot()
  def shutdown(self, ) -> None:
    """This method is called to complete the shutdown process."""
    self.status.showMessage("""Shutting Down...""", 5000)
    self.close()

  def show(self) -> None:
    """The show method initializes the UI and logic before showing the
    window."""
    self.initBars()
    self._initBaseLogic()
    self.initUi()
    self.initLogic()
    QMainWindow.show(self)
