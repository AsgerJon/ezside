"""DataWidget provides a place to put the DataView."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from attribox import AttriBox, this

from ezqt.widgets import BaseWidget, DataView
from settings import Default


class DataWidget(BaseWidget):
  """DataWidget provides a place to put the DataView."""

  __fallback_num_points__ = Default.numPoints

  verticalLayout = AttriBox[QVBoxLayout]()
  verticalWidget = AttriBox[BaseWidget]()
  dataView = AttriBox[DataView](this)
  baseWidget = AttriBox[BaseWidget]()
  baseLayout = AttriBox[QHBoxLayout]()

  def __init__(self, *args, **kwargs) -> None:
    BaseWidget.__init__(self, *args, **kwargs)
    self._numPoints = None
    for arg in args:
      if isinstance(arg, int):
        self._numPoints = arg
    self.initUi()
    self.connectActions()

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.baseLayout.addWidget(self.dataView)
    self.verticalWidget.setLayout(self.verticalLayout)
    self.baseLayout.addWidget(self.verticalWidget)
    self.setLayout(self.baseLayout)

  def connectActions(self) -> None:
    """The connectActions method connects the actions of the window."""

  def getNumPoints(self) -> int:
    """The getNumPoints method returns the number of points."""
    return self._numPoints
