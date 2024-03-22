"""DataWidget provides a place to put the DataView."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from attribox import AttriBox

from ezside.widgets import BaseWidget, WhiteNoise, DataView
from settings import Default


class DataWidget(BaseWidget):
  """DataWidget provides a place to put the DataView."""

  __fallback_num_points__ = Default.numPoints

  start = Signal()
  stop = Signal()
  pause = Signal()

  baseLayout = AttriBox[QVBoxLayout]()
  dataView = AttriBox[DataView]()

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(64, 64)
    self.dataView.initUi()
    self.baseLayout.addWidget(self.dataView)
    self.setLayout(self.baseLayout)

  @Slot()
  def refresh(self) -> None:
    """The refresh method refreshes the data."""
    self.dataView.refresh()
