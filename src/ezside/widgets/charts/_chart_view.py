"""ChartView provides a widget showing live updating charts from the
QChart framework."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from math import pi, sin

from PySide6.QtCharts import QChartView, QValueAxis, QChart, QScatterSeries
from PySide6.QtCore import QPointF, Slot

from ezside.core import AlignBottom, AlignLeft


class ChartView(QChartView):
  """ChartView provides a widget showing live updating charts from the
  QChart framework."""

  __recent_time__ = None
  chart: QChart
  series: QScatterSeries
  horizontalAxis: QValueAxis
  verticalAxis: QValueAxis

  def __init__(self, *args, **kwargs) -> None:
    QChartView.__init__(self, *args, **kwargs)

  def initUi(self) -> None:
    """Initialize the UI elements."""
    n = 16
    self.chart = QChart()
    self.chart.setTitle('fuck')
    self.series = QScatterSeries()
    self.chart.addSeries(self.series)
    for i in range(n):
      x = 2 * pi / (n - 1) * i
      y = sin(x)
      p = QPointF(x, y)
      self.series.append(p)
    self.horizontalAxis = QValueAxis()
    self.horizontalAxis.setRange(0, 2 * pi)
    self.verticalAxis = QValueAxis()
    self.verticalAxis.setRange(-1, 1)
    self.chart.addAxis(self.horizontalAxis, AlignBottom)
    self.chart.addAxis(self.verticalAxis, AlignLeft)
    self.series.attachAxis(self.horizontalAxis)
    self.series.attachAxis(self.verticalAxis)
    self.setChart(self.chart)

  def addPoint(self, value: float = None) -> None:
    """Adds to the series"""
    if self.__recent_time__ is None:
      self.__recent_time__ = 2 * pi + pi / 8
    else:
      self.__recent_time__ += pi / 8
    value = sin(self.__recent_time__) if value is None else value
    self.series.append(self.__recent_time__, value)
    t1 = self.__recent_time__
    t0 = t1 - 2 * pi
    self.horizontalAxis.setRange(t0, t1)

  @Slot()
  def step(self) -> None:
    """Steps the data"""
    self.addPoint()
