"""WrapView wraps the QChartView subclasses, as they must remain
subclasses of QGraphicView. The WrapView widget shows the DataView
instance while remaining a subclass of BaseWidget. This allows the
DataView to be used in layouts and other widgets that require a BaseWidget
instance."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Slot
from attribox import AttriBox, this
from icecream import ic
from vistutils.parse import maybe

from ezside.widgets import BaseWidget, DataView,

ic.configureOutput(includeContext=True)


class WrapView(BaseWidget):
  """WrapView provides a wrapper around the DataView."""

  __this_vals__ = None

  dataView = AttriBox[DataView](this)
  baseLayout = AttriBox[Layout]('horizontal')

  def __init__(self, seriesType: str = None, *args, **kwargs):
    BaseWidget.__init__(self, *args, **kwargs)
    self._seriesType = maybe(seriesType, 'scatter')

  def initUi(self) -> None:
    """Initializes the user interface for the main window."""
    self.baseLayout.addWidget(self.dataView)
    self.setLayout(self.baseLayout)

  @Slot()
  def refresh(self) -> None:
    """Refreshes the data."""

  def getSeriesType(self) -> str:
    """Returns the series type."""
    return self._seriesType or 'scatter'
