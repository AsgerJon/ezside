"""DataSeries wraps the QXYSeries, QScatterSeries and QLineSeries classes
to provide a common interface for these classes."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import numpy as np
from PySide6.QtCharts import QXYSeries, QLineSeries, QScatterSeries
from PySide6.QtCore import Slot
from attribox import AttriBox

from ezqt.widgets import DataRoll


class DataSeries(QXYSeries):
  """DataSeries wraps the QXYSeries, QScatterSeries and QLineSeries classes
  to provide a common interface for these classes."""

  data = AttriBox[DataRoll]()

  def updateValues(self, ) -> None:
    """Updates the values of the series."""
    data = self.data.snapShot()
    t = data.real
    x = data.imag
    self.clear()
    self.appendNp(t.astype(np.float32), x.astype(np.float32))


class ScatterSeries(QScatterSeries):
  """ScatterSeries wraps the QScatterSeries class to provide a common
  interface for the QXYSeries, QScatterSeries and QLineSeries classes."""

  data = AttriBox[DataRoll]()

  def updateValues(self, ) -> None:
    """Updates the values of the series."""
    data = self.data.snapShot()
    t = data.real
    x = data.imag
    self.clear()
    self.appendNp(t.astype(np.float32), x.astype(np.float32))

  @Slot(float)
  def appendValue(self, value: float) -> None:
    """Appends a value to the series."""
    self.data.append(value)


class LineSeries(QLineSeries):
  """ScatterSeries wraps the QScatterSeries class to provide a common
  interface for the QXYSeries, QScatterSeries and QLineSeries classes."""

  data = AttriBox[DataRoll]()

  def updateValues(self, ) -> None:
    """Updates the values of the series."""
    data = self.data.snapShot()
    t = data.real
    x = data.imag
    self.clear()
    self.appendNp(t.astype(np.float32), x.astype(np.float32))

  @Slot(float)
  def appendValue(self, value: float) -> None:
    """Appends a value to the series."""
    self.data.append(value)
