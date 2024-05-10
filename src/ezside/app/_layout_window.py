"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QVBoxLayout
from icecream import ic

from ezside.app import BaseWindow
from ezside.core import AlignTop, AlignLeft
from ezside.widgets import Label, BaseWidget, DigitalClock
from ezside.widgets.charts import ChartView

ic.configureOutput(includeContext=True, )


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and implements the layout of
  widgets."""

  welcomeLabel: Label
  clock: DigitalClock
  baseLayout: QVBoxLayout
  baseWidget: BaseWidget
  chartView: ChartView

  def initStyle(self) -> None:
    """The initStyle method initializes the style of the window and the
    widgets on it, before 'initUi' sets up the layout. """

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(QSize(640, 480))
    self.baseLayout = QVBoxLayout()
    self.baseWidget = BaseWidget()
    self.baseWidget.__debug_flag__ = True
    self.baseLayout.setAlignment(AlignTop | AlignLeft)
    self.welcomeLabel = Label('LMAO')
    self.welcomeLabel.initUi()
    self.baseLayout.addWidget(self.welcomeLabel)
    self.clock = DigitalClock()
    self.clock.initUi()
    self.baseLayout.addWidget(self.clock)
    self.chartView = ChartView()
    self.chartView.initUi()
    self.baseLayout.addWidget(self.chartView)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)

  @abstractmethod  # MainWindow
  def initSignalSlot(self) -> None:
    """The initActions method initializes the actions of the window."""
