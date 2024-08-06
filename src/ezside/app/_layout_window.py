"""LayoutWindow provides a subclass of BaseWindow that is responsible for
organizing the widget layout of the main window, leaving business logic
for a further subclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QVBoxLayout, QLayout, QHBoxLayout
from worktoy.desc import AttriBox, THIS

from ezside.app import BaseWindow, StatusBar
from ezside.widgets import Label, BoxWidget, DigitalClock


class LayoutWindow(BaseWindow):
  """LayoutWindow provides a subclass of BaseWindow that is responsible for
  organizing the widget layout of the main window, leaving business logic
  for a further subclass."""

  baseWidget = AttriBox[BoxWidget](THIS)
  horizontalWidget = AttriBox[BoxWidget](THIS)
  baseLayout = AttriBox[QVBoxLayout]()
  horizontalLayout = AttriBox[QHBoxLayout]()
  headerLabel = AttriBox[Label](THIS, 'Welcome to EZSide')
  leftLabel = AttriBox[Label](THIS, 'Left')
  centralLabel = AttriBox[Label](THIS, 'Central')
  rightLabel = AttriBox[Label](THIS, 'Right')
  footerLabel = AttriBox[Label](THIS, 'Footer')

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the object"""
    BaseWindow.__init__(self, )
    self.setWindowTitle('-- EZSide --')

  def initLayout(self) -> None:
    """This method is responsible for initializing the user interface."""
    self.baseWidget.backgroundColor = QColor(144, 255, 0, 255)
    self.horizontalWidget.backgroundColor = QColor(255, 144, 0, 255)
    self.baseLayout.addWidget(self.headerLabel)
    self.horizontalLayout.addWidget(self.leftLabel)
    self.horizontalLayout.addWidget(self.centralLabel)
    self.horizontalLayout.addWidget(self.rightLabel)
    self.horizontalWidget.setLayout(self.horizontalLayout)
    self.baseLayout.addWidget(self.horizontalWidget)
    self.baseLayout.addWidget(self.footerLabel)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)
