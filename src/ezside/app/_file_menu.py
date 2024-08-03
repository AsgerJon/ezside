"""FileMenu subclasses the QMenu class and provides the file menu for the
main window. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from worktoy.desc import AttriBox

from ezside.app import Action


class FileMenu(QMenu):
  """FileMenu subclasses the QMenu class and provides the file menu for the
  main window. """

  __action_list__ = None
  __iter_contents__ = None

  newAction = AttriBox[Action]('New', 'CTRL+N', 'new.png')
  openAction = AttriBox[Action]('Open', 'CTRL+O', 'open.png')
  saveAction = AttriBox[Action]('Save', 'CTRL+S', 'save.png')
  saveAsAction = AttriBox[Action](
      'Save As', 'CTRL+SHIFT+S', 'save_as.png')
  exitAction = AttriBox[Action]('Exit', 'CTRL+Q', 'exit.png')

  def __iter__(self, ) -> Self:
    """Implements the iteration protocol"""
    self.__iter_contents__ = [
        self.newAction,
        self.openAction,
        self.saveAction,
        self.saveAsAction,
        self.exitAction
    ]
    return self

  def __next__(self, ) -> Action:
    """Implements the iteration protocol"""
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def initUi(self) -> None:
    """Initializes the menu"""
    QMenu.addMenu(self, self.newAction)
    QMenu.addMenu(self, self.openAction)
    QMenu.addMenu(self, self.saveAction)
    QMenu.addMenu(self, self.saveAsAction)
    QMenu.addMenu(self, self.exitAction)
