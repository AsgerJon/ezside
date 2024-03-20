"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QGridLayout
from attribox import AttriBox

from ezqt.core import LawnGreen
from ezqt.widgets import (HorizontalPanel, DataWidget, ClientInfo,
                          BaseWidget, \
                          WhiteNoise)
from ezqt.widgets import TextLabel, CornerPanel, VerticalPanel
from ezqt.windows import BaseWindow


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and implements the layout of
  widgets."""

  baseWidget = AttriBox[BaseWidget]()
  baseLayout = AttriBox[QGridLayout]()

  left = AttriBox[VerticalPanel](LawnGreen)
  top = AttriBox[HorizontalPanel](LawnGreen)
  right = AttriBox[VerticalPanel](LawnGreen)
  bottom = AttriBox[HorizontalPanel](LawnGreen)
  topLeft = AttriBox[CornerPanel](LawnGreen)
  topRight = AttriBox[CornerPanel](LawnGreen)
  bottomLeft = AttriBox[CornerPanel](LawnGreen)
  bottomRight = AttriBox[CornerPanel](LawnGreen)

  titleBanner = AttriBox[TextLabel]('EZQt')
  whiteNoise = AttriBox[WhiteNoise]()
  clientInfo = AttriBox[ClientInfo]()
  dataWidget = AttriBox[DataWidget]()

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(800, 800)
    rowCount = 2
    colCount = 1
    self.baseLayout.addWidget(self.bottomRight, rowCount + 1, 1 + colCount)
    self.baseLayout.addWidget(self.bottom, rowCount + 1, 1, 1, colCount)
    self.baseLayout.addWidget(self.bottomLeft, rowCount + 1, 0)

    self.baseLayout.addWidget(self.left, 1, 0, rowCount, 1)
    self.baseLayout.addWidget(self.right, 1, colCount + 1, rowCount, 1)

    self.baseLayout.addWidget(self.topLeft, 0, 0)
    self.baseLayout.addWidget(self.top, 0, 1, 1, colCount)
    self.baseLayout.addWidget(self.topRight, 0, colCount + 1)

    self.whiteNoise.initUi()
    self.baseLayout.addWidget(self.whiteNoise, 1, 1)
    self.dataWidget.initUi()
    self.baseLayout.addWidget(self.dataWidget, 2, 1)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)
    BaseWindow.initUi(self, )
