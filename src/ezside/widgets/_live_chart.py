"""LiveChart visualizes data that is being updated in real-time. It
leverages the QChart framework along with the BaseWidget class to achieve
this and further customization. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCharts import QChart, QValueAxis, QChartView, QScatterSeries
from PySide6.QtGui import QBrush, QFont, QColor, QPainter
from PySide6.QtWidgets import QVBoxLayout, QFrame, QHBoxLayout
from icecream import ic

from ezside.core import parseFont, Normal, SolidFill, parseBrush
from ezside.core import AlignLeft, AlignBottom
from ezside.widgets import BaseWidget, Label, PushButton


class LiveChart(BaseWidget):
  """LiveChart visualizes data that is being updated in real-time. It
  leverages the QChart framework along with the BaseWidget class to achieve
  this and further customization. """

  view: QChartView
  chart: QChart
  hAxis: QValueAxis
  vAxis: QValueAxis
  series: QScatterSeries
  baseLayout: QVBoxLayout
  buttonLayout: QHBoxLayout
  buttonWidget: BaseWidget
  pauseButton: PushButton
  resumeButton: PushButton
  welcomeBanner: Label

  __chart_title__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the LiveChart instance."""
    BaseWidget.__init__(self, *args, **kwargs)
    for arg in args:
      if isinstance(arg, str):
        self.__chart_title__ = arg
        break
    else:
      self.__chart_title__ = 'Live Chart'

  @classmethod
  def styleTypes(cls) -> dict[str, type]:
    """The styleTypes method provides the type expected at each name. """
    return {
      'chartTheme': QChart.ChartTheme,
      'titleFont' : QFont,
      'titleBrush': QBrush,
      'labelFont' : QFont,
      'labelColor': QColor,
      'timeWindow': int,
      'minValue'  : float,
      'maxValue'  : float,
    }

  @classmethod
  def staticStyles(cls) -> dict[str, Any]:
    """The registerFields method registers the fields of the widget.
    Please note, that subclasses can reimplement this method, but must
    provide these same fields. """
    return {
      'chartTheme': QChart.ChartTheme.ChartThemeBrownSand,
      'titleFont' : parseFont('Montserrat', 20, Normal),
      'titleBrush': parseBrush(QColor(0, 0, 0, 255), SolidFill, ),
      'labelFont' : parseFont('Montserrat', 12, Normal),
      'labelColor': QColor(0, 0, 63, 255),
      'timeWindow': 5000,  # milliseconds
      'minValue'  : -0.2,
      'maxValue'  : 5.0,
    }

  def dynStyles(self) -> dict[str, Any]:
    """Implementation of dynamic fields"""
    return {}

  def initChart(self, ) -> None:
    """Initialize the user interface."""
    self.baseLayout = QVBoxLayout(self)
    self.chart = QChart()
    self.chart.setTitle('')
    self.chart.legend().hide()
    self.chart.setTheme(self.getStyle('chartTheme'))
    self.series = QScatterSeries()
    self.series.setPointLabelsFont(self.getStyle('labelFont'))
    self.series.setPointLabelsColor(self.getStyle('labelColor'))
    self.series.setName('Live Data')
    self.chart.addSeries(self.series)
    self.hAxis = QValueAxis()
    self.hAxis.setRange(-self.getStyle('timeWindow'), 0)
    self.vAxis = QValueAxis()
    self.vAxis.setRange(self.getStyle('minValue'), self.getStyle('maxValue'))
    self.chart.addAxis(self.hAxis, AlignBottom)
    self.chart.addAxis(self.vAxis, AlignLeft)
    self.series.attachAxis(self.hAxis)
    self.series.attachAxis(self.vAxis)
    self.view = QChartView(self.chart)
    self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
    self.view.setFrameShadow(QFrame.Shadow.Sunken)
    self.view.setFrameShape(QFrame.Shape.StyledPanel, )

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    self.setMouseTracking(True)
    self.initChart()
    self.baseLayout.addWidget(self.view)
    self.welcomeBanner = Label('LMAO!')
    self.baseLayout.addWidget(self.welcomeBanner)
    self.buttonLayout = QHBoxLayout()
    self.buttonWidget = BaseWidget()
    self.pauseButton = PushButton()
    self.pauseButton.initUi()
    self.pauseButton.initSignalSlot()
    self.resumeButton = PushButton()
    self.resumeButton.initUi()
    self.resumeButton.initSignalSlot()
    self.buttonLayout.addWidget(self.pauseButton)
    self.buttonLayout.addWidget(self.resumeButton)
    self.buttonWidget.setLayout(self.buttonLayout)
    self.baseLayout.addWidget(self.buttonWidget)
    self.setLayout(self.baseLayout)

  def initSignalSlot(self) -> None:
    """Initialize the signal slot."""
    self.pauseButton.singleClick.connect(self.pause)
    self.resumeButton.singleClick.connect(self.resume)

  def pause(self) -> None:
    """Pauses the chart from updating"""
    ic('pause lmao')

  def resume(self) -> None:
    """Resumes the chart updating"""
    ic('resume lmao')
