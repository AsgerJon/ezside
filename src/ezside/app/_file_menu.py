"""FileMenu subclasses the QMenu class and provides the file menu for the
main window. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget
from worktoy.desc import AttriBox

from ezside.app import EZAction, AbstractMenu


class FileMenu(AbstractMenu):
  """FileMenu subclasses the QMenu class and provides the file menu for the
  main window. """

  newAction = AttriBox[EZAction]('New', 'CTRL+N', 'new.png')
  openAction = AttriBox[EZAction]('Open', 'CTRL+O', 'open.png')
  saveAction = AttriBox[EZAction]('Save', 'CTRL+S', 'save.png')
  saveAsAction = AttriBox[EZAction](
      'Save As', 'CTRL+SHIFT+S', 'save_as.png')
  exitAction = AttriBox[EZAction]('Exit', 'CTRL+Q', 'exit.png')

  def initUi(self) -> None:
    """Initializes the menu"""
    self.addAction(self.newAction)
    self.addAction(self.openAction)
    self.addAction(self.saveAction)
    self.addAction(self.saveAsAction)
    self.addAction(self.exitAction)

  def __init__(self, parent: QWidget = None, *args) -> None:
    AbstractMenu.__init__(self, parent, 'File')
    self.initUi()
