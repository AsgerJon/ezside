"""LayoutWindow organizes the widgets on the layouts."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QVBoxLayout, QLabel
from attribox import AttriBox
from icecream import ic

from ezside.desc import Expand
from ezside.widgets import BaseWidget, TextBox, PushButtonWidget, Label
from ezside.windows import BaseWindow, lol

ic.configureOutput(includeContext=True)


class LayoutWindow(BaseWindow):
  """LayoutWindow organizes the widgets on the layouts."""

  baseWidget = AttriBox[BaseWidget]()
  baseLayout = AttriBox[QVBoxLayout]()
  welcomeBanner = Label('Welcome to EZSide!', id='title')
  testButton = AttriBox[PushButtonWidget]('yolo!')

  def initUi(self) -> None:
    """Initializes the user interface."""
    self.setSizePolicy(Expand, Expand)
    self.setMinimumSize(QSize(480, 320))
    self.welcomeBanner.initUi()
    self.baseLayout.addWidget(self.welcomeBanner)
    self.testButton.initUi()
    self.baseLayout.addWidget(self.testButton)
    self.baseWidget.initUi()
    self.baseWidget.setSizePolicy(Expand, Expand)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)
