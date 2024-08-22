"""LayoutWindow provides a subclass of BaseWindow that is responsible for
organizing the widget layout of the main window, leaving business logic
for a further subclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from worktoy.desc import AttriBox, THIS

from ezside.app import BaseWindow
from ezside.layouts import VerticalLayout, AbstractLayout
from ezside.base_widgets import Label
from ezside.widgets import ImgEdit

ic.configureOutput(includeContext=True)


class LayoutWindow(BaseWindow):
  """LayoutWindow provides a subclass of BaseWindow that is responsible for
  organizing the widget layout of the main window, leaving business logic
  for a further subclass."""

  baseWidget = AttriBox[VerticalLayout]()
  headerLabel = AttriBox[Label](THIS, 'LOL')
  welcomeLabel = AttriBox[Label](THIS, 'Welcome to EZSide')
  infoLabel = AttriBox[Label](THIS, 'New Layout System!!')

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the object"""
    BaseWindow.__init__(self, )
    self.setWindowTitle('-- EZSide --')

  def initLayout(self) -> None:
    """This method is responsible for initializing the user interface."""
    self.baseWidget.addWidget(self.headerLabel)
    self.baseWidget.addWidget(self.welcomeLabel)
    self.baseWidget.addWidget(self.infoLabel)
    self.setCentralWidget(self.baseWidget)

  def show(self) -> None:
    """Show the window"""
    self.initLayout()
    self.initSignalSlot()
    BaseWindow.show(self)
