"""DataView collects the functionality from QCharts to show data in a plot
that is continuously updated."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import numpy as np
from PySide6.QtCharts import QChart, QChartView, QScatterSeries
from PySide6.QtCore import Signal
from icecream import ic

from attribox import AttriBox
from ezqt.widgets import DataRoll

ic.configureOutput(includeContext=True, )


class DataView(QChartView):
  """DataView collects the functionality from QCharts to show data in a plot
  that is continuously updated."""

  data = AttriBox[DataRoll](256)
  series = AttriBox[QScatterSeries]()
  dataChart = AttriBox[QChart]()

  minValChange = Signal(float)
  maxValChange = Signal(float)

  def refresh(self) -> None:
    """Refreshes the data in the chart."""
    self.series.clear()
    data = self.data.snapShot()
    t = data.real
    x = data.imag
    self.series.appendNp(t.astype(np.float32), x.astype(np.float32))

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the DataView."""
    QChartView.__init__(self, )
    self.setMinimumSize(640, 480)
    self.dataChart.addSeries(self.series)
    self.refresh()
    self.dataChart.createDefaultAxes()
    self.setChart(self.dataChart)
    self.dataChart.setAnimationOptions(QChart.AnimationOption.NoAnimation)

  def getVerticalRange(self) -> tuple[float, float]:
    """Returns the vertical range of the chart."""
    a = self.dataChart.axes()[1]
    return a.min(), a.max()

  def min(self) -> float:
    """Returns the minimum value of the vertical range."""
    return self.getVerticalRange()[0]

  def max(self) -> float:
    """Returns the maximum value of the vertical range."""
    return self.getVerticalRange()[1]

  def decMin(self, ) -> None:
    """Decreases the minimum value of the vertical range."""
    a = self.dataChart.axes()[1]
    newVal = a.min() * (0.9 if a.min() < 0 else 1.1)
    self.minValChange.emit(newVal)
    self.dataChart.axes()[1].setMin(newVal)

  def incMin(self, ) -> None:
    """Increases the minimum value of the vertical range."""
    a = self.dataChart.axes()[1]
    newVal = a.min() * (0.9 if a.min() < 0 else 1.1)
    self.minValChange.emit(newVal)
    self.dataChart.axes()[1].setMin(newVal)

  def decMax(self, ) -> None:
    """Decreases the maximum value of the vertical range."""
    a = self.dataChart.axes()[1]
    newVal = a.max() * (0.9 if a.max() < 0 else 1.1)
    self.maxValChange.emit(newVal)
    self.dataChart.axes()[1].setMax(newVal)

  def incMax(self, ) -> None:
    """Increases the maximum value of the vertical range."""
    a = self.dataChart.axes()[1]
    newVal = a.max() * (0.9 if a.max() > 0 else 1.1)
    self.maxValChange.emit(newVal)
    self.dataChart.axes()[1].setMax(newVal)
