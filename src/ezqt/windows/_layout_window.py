"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QGridLayout

from attribox import AttriBox
from ezqt.core import LawnGreen
from ezqt.widgets import TextLabel, HorizontalPanel, VerticalPanel, \
  CornerPanel, Noisinator, DataWidget
from ezqt.windows import BaseWindow


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and implements the layout of
  widgets."""

  baseWidget = AttriBox[QWidget]()
  baseLayout = AttriBox[QGridLayout]()
  left = AttriBox[VerticalPanel](LawnGreen)
  top = AttriBox[HorizontalPanel](LawnGreen)
  right = AttriBox[VerticalPanel](LawnGreen)
  bottom = AttriBox[HorizontalPanel](LawnGreen)
  topLeft = AttriBox[CornerPanel](LawnGreen)
  topRight = AttriBox[CornerPanel](LawnGreen)
  bottomLeft = AttriBox[CornerPanel](LawnGreen)
  bottomRight = AttriBox[CornerPanel](LawnGreen)
  titleBanner = AttriBox[TextLabel]()
  lolBanner = AttriBox[TextLabel]('LMAO')
  noise = AttriBox[Noisinator]('Noise')
  dataWidget = AttriBox[DataWidget]()

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    BaseWindow.initUi(self, )
    self.setMinimumSize(800, 800)
    self.baseLayout.addWidget(self.bottomRight, 4, 2)
    self.baseLayout.addWidget(self.bottom, 4, 1)
    self.baseLayout.addWidget(self.bottomLeft, 4, 0)
    self.baseLayout.addWidget(self.left, 1, 0, 3, 1)
    self.baseLayout.addWidget(self.topLeft, 0, 0)
    self.baseLayout.addWidget(self.top, 0, 1)
    self.baseLayout.addWidget(self.topRight, 0, 2)
    self.baseLayout.addWidget(self.right, 1, 2, 3, 1)
    self.baseLayout.addWidget(self.titleBanner, 1, 1, )
    self.dataWidget.initUi()
    self.baseLayout.addWidget(self.dataWidget, 2, 1)
    self.noise.initUi()
    self.noise.setParent(self)
    self.baseLayout.addWidget(self.noise, 3, 1)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)

  def connectActions(self) -> None:
    """The connectActions method connects the actions of the window."""
    BaseWindow.connectActions(self)

  def show(self) -> None:
    """Shows the main window."""
    self.initUi()
    BaseWindow.show(self)
