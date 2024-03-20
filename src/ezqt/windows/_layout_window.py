"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QGridLayout
from attribox import AttriBox
from icecream import ic

from ezqt.core import LawnGreen
from ezqt.widgets import (HorizontalPanel, DataWidget, ClientInfo,
                          BaseWidget, \
                          WhiteNoise, PlotEnvelope)
from ezqt.widgets import TextLabel, CornerPanel, VerticalPanel
from ezqt.windows import BaseWindow

ic.configureOutput(includeContext=True, )


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
  plotEnvelope = AttriBox[PlotEnvelope]()

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(400, 400)
    rowCount = 2
    colCount = 2

    self.bottomRight.initUi()
    self.bottomLeft.initUi()
    self.topRight.initUi()
    self.topLeft.initUi()
    self.left.initUi()
    self.top.initUi()
    self.right.initUi()
    self.bottom.initUi()

    self.baseLayout.addWidget(self.bottomRight, rowCount + 1, 1 + colCount)
    self.baseLayout.addWidget(self.bottom, rowCount + 1, 1, 1, colCount)
    self.baseLayout.addWidget(self.bottomLeft, rowCount + 1, 0)

    self.baseLayout.addWidget(self.left, 1, 0, rowCount, 1)
    self.baseLayout.addWidget(self.right, 1, colCount + 1, rowCount, 1)

    self.baseLayout.addWidget(self.topLeft, 0, 0)
    self.baseLayout.addWidget(self.top, 0, 1, 1, colCount)
    self.baseLayout.addWidget(self.topRight, 0, colCount + 1)

    self.whiteNoise.initUi()
    self.baseLayout.addWidget(self.whiteNoise, 1, 2)
    self.plotEnvelope.initUi()
    self.baseLayout.addWidget(self.plotEnvelope, 2, 2)
    self.dataWidget.initUi()
    self.baseLayout.addWidget(self.dataWidget, 1, 1, 2, 1)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)
    BaseWindow.initUi(self, )
