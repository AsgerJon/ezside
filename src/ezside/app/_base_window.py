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

from ezside.app import StatusBar, MenuBar
from ezside.tools import Timer


class BaseWindow(QMainWindow):
  """BaseWindow subclasses QMainWindow and provides a base window for the
  application. It implements menus, menubar and statusbar. It is intended to
  be further subclassed to implement widget layout and business logic. """

  pulse = Signal()
  timer = AttriBox[Timer](Qt.TimerType.PreciseTimer, 500, False)
  mainStatusBar = AttriBox[StatusBar]()
  mainMenuBar = AttriBox[MenuBar]()

  def __init__(self, *args) -> None:
    QMainWindow.__init__(self)
    self.setMenuBar(self.mainMenuBar)
    self.setStatusBar(self.mainStatusBar)

  def show(self) -> None:
    """Reimplementation setting up signals and slots before invoking
    parent method."""
    QMainWindow.show(self)
