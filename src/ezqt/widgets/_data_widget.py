"""DataWidget provides a place to put the DataView."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout

from attribox import AttriBox
from ezqt.widgets import TextLabel, BaseWidget, HorizontalPanel, DataView
from settings import Default


class DataWidget(BaseWidget):
  """DataWidget provides a place to put the DataView."""

  incMinVertical = AttriBox[QPushButton]('Increase Min Vertical')
  displayMinVertical = AttriBox[TextLabel]()
  decMinVertical = AttriBox[QPushButton]('Reduce Min Vertical')
  separator = AttriBox[HorizontalPanel]()
  incMaxVertical = AttriBox[QPushButton]('Increase Max Vertical')
  displayMaxVertical = AttriBox[TextLabel]()
  decMaxVertical = AttriBox[QPushButton]('Reduce Max Vertical')

  verticalLayout = AttriBox[QVBoxLayout]()
  verticalWidget = AttriBox[BaseWidget]()
  dataView = AttriBox[DataView](Default.numPoints)
  baseWidget = AttriBox[BaseWidget]()
  baseLayout = AttriBox[QHBoxLayout]()

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.baseLayout.addWidget(self.dataView)
    self.verticalLayout.addWidget(self.incMinVertical)
    self.verticalLayout.addWidget(self.displayMinVertical)
    self.verticalLayout.addWidget(self.decMinVertical)
    self.verticalLayout.addWidget(self.separator)
    self.verticalLayout.addWidget(self.incMaxVertical)
    self.verticalLayout.addWidget(self.displayMaxVertical)
    self.verticalLayout.addWidget(self.decMaxVertical)
    self.verticalWidget.setLayout(self.verticalLayout)
    self.baseLayout.addWidget(self.verticalWidget)
    self.setLayout(self.baseLayout)

  def connectActions(self) -> None:
    """The connectActions method connects the actions of the window."""
    self.incMinVertical.clicked.connect(self.dataView.incMinVertical)
    self.decMinVertical.clicked.connect(self.dataView.decMinVertical)
    self.incMaxVertical.clicked.connect(self.dataView.incMaxVertical)
    self.decMaxVertical.clicked.connect(self.dataView.decMaxVertical)
    self.incMinVertical.clicked.connect(self.dataView.incMinVertical)
    self.decMinVertical.clicked.connect(self.dataView.decMinVertical)
    self.incMaxVertical.clicked.connect(self.dataView.incMaxVertical)
    self.decMaxVertical.clicked.connect(self.dataView.decMaxVertical)
    self.dataView.minValChange.connect(self.displayMinVertical.setText)
    self.dataView.maxValChange.connect(self.displayMaxVertical.setText)
