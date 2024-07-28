"""LayoutWindow provides a subclass of BaseWindow that is responsible for
organizing the widget layout of the main window, leaving business logic
for a further subclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout
from worktoy.desc import THIS, AttriBox

from ezside.app import BaseWindow
from ezside.widgets import TextLabel, BoxWidget


class LayoutWindow(BaseWindow):
  """LayoutWindow provides a subclass of BaseWindow that is responsible for
  organizing the widget layout of the main window, leaving business logic
  for a further subclass."""

  baseWidget = AttriBox[BoxWidget](THIS)
  baseLayout = AttriBox[QVBoxLayout]()
  welcomeLabel = AttriBox[TextLabel](THIS, 'YOLO')

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the object"""
    BaseWindow.__init__(self, )
    self.setWindowTitle('-- EZSide --')

  def initLayout(self) -> None:
    """This method is responsible for initializing the user interface."""
    self.baseLayout.addWidget(self.welcomeLabel)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)

  def show(self, ) -> None:
    """This method is responsible for showing the window."""
    self.initLayout()
    BaseWindow.show(self)
