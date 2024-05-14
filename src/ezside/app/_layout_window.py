"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QVBoxLayout
from icecream import ic

from ezside.app import BaseWindow
from ezside.app.menus import ConfirmBox
from ezside.core import AlignTop, AlignLeft, CursorVector
from ezside.widgets import BaseWidget, Label, PushButton

ic.configureOutput(includeContext=True, )


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and implements the layout of
  widgets."""

  confirmBox = ConfirmBox()

  def __init__(self, *args, **kwargs) -> None:
    """The constructor of the LayoutWindow class."""
    BaseWindow.__init__(self, *args, **kwargs)
    self.baseLayout = QVBoxLayout()
    self.baseWidget = BaseWidget()
    self.titleWidget = Label('Title', id='title')
    self.headerWidget = Label('Header', id='header')
    self.buttonWidget = PushButton('Click Me', )
    self.vectorLabel = Label('LMAO', id='info')
    self.velocityIndicator = Label('Velocity', id='info')

  def initStyle(self) -> None:
    """The initStyle method initializes the style of the window and the
    widgets on it, before 'initUi' sets up the layout. """

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.baseWidget.__debug_flag__ = True
    self.baseLayout.setAlignment(AlignTop | AlignLeft)
    self.baseLayout.addWidget(self.titleWidget)
    self.baseLayout.addWidget(self.headerWidget)
    self.buttonWidget.setMinimumSize(QSize(384, 384))
    self.buttonWidget.initUi()
    self.baseLayout.addWidget(self.buttonWidget)
    self.vectorLabel.initUi()
    self.buttonWidget.mouseMove.connect(self.vectorLabel.echo)
    self.buttonWidget.mouseMove.connect(self.velocity)
    self.baseLayout.addWidget(self.vectorLabel)
    self.velocityIndicator.prefix = '| > '
    self.velocityIndicator.suffix = ' < |'
    self.velocityIndicator.initUi()
    self.baseLayout.addWidget(self.velocityIndicator)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)

  @abstractmethod  # MainWindow
  def initSignalSlot(self) -> None:
    """The initActions method initializes the actions of the window."""

  def velocity(self, *args) -> None:
    """The velocity method updates the velocity of the window."""
    if args:
      if isinstance(args[0], CursorVector):
        self.velocityIndicator.text = '%.3f' % abs(args[0])
