"""DataView collects the functionality from QCharts to show data in a plot
that is continuously updated."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCharts import QChart, QChartView
from PySide6.QtCore import Slot
from icecream import ic
from attribox import AttriBox

from ezside.widgets import ScatterSeries, LineSeries
from settings import Default

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True, )


class DataView(QChartView):
  """DataView collects the functionality from QCharts to show data in a plot
  that is continuously updated."""

  innerChart = AttriBox[QChart]()
  lineVals = AttriBox[LineSeries]()
  scatter = AttriBox[ScatterSeries]()

  def initUi(self) -> None:
    """Sets up the view"""
    self.setMinimumSize(Default.chartViewWidth, Default.chartViewHeight)
    self.initScatter()

  def initScatter(self, ) -> None:
    """Initializes the scatter series."""
    self.setChart(self.innerChart)
    self.innerChart.removeAllSeries()
    self.innerChart.addSeries(self.scatter)
    self.innerChart.createDefaultAxes()
    self.update()

  def initLine(self) -> None:
    """Initializes the line series."""
    self.setChart(self.innerChart)
    self.innerChart.removeAllSeries()
    self.innerChart.addSeries(self.lineVals)
    self.innerChart.createDefaultAxes()
    self.update()

  @Slot(float)
  def append(self, value: float) -> None:
    """Appends a value to the series."""
    self.scatter.appendValue(value)
    self.lineVals.appendValue(value)

  @Slot()
  def refresh(self) -> None:
    """Refreshes the data."""
    self.scatter.updateValues()
    self.lineVals.updateValues()
    self.update()
