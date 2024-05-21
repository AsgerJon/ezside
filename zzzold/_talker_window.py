"""TalkerWindow provides a dialog window allowing users to specify
emission of periodic signals. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QDialog, QMainWindow
from attribox import AttriBox

from ezside.core import Expand, Tight, parseParent
from ezside.widgets import Equalizer, Label


class TalkerWindow(QDialog):
  """TalkerWindow provides a dialog window allowing users to specify
  emission of periodic signals. """

  baseLayout = AttriBox[QVBoxLayout]()
  titleLabel = AttriBox[Label]('LMAO', id='title')
  equalizer = AttriBox[Equalizer]()

  emitValue = Signal(float)

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(QMainWindow, *args, **kwargs)
    QDialog.__init__(self, parent)

  def initUi(self) -> None:
    """Initializes the user interface for the widget. """
    self.baseLayout.setSpacing(0)
    self.baseLayout.setContentsMargins(0, 0, 0, 0)
    self.titleLabel.setSizePolicy(Expand, Tight)
    self.titleLabel.text = 'Talker'
    self.titleLabel.initUi()
    self.baseLayout.addWidget(self.titleLabel)
    self.equalizer.setMinimumSize(200, 200)
    self.equalizer.initUi()
    self.baseLayout.addWidget(self.equalizer)
    self.setLayout(self.baseLayout)

  def initSignalSlot(self) -> None:
    """Connects the signals and slots for the widget. """
    self.equalizer.emitValue.connect(self.emitValue)
    self.equalizer.initSignalSlot()
    self.equalizer.emitValue.connect(self.emitValue)

  def show(self) -> None:
    """LMAO"""
    self.initUi()
    self.initSignalSlot()
    QDialog.show(self)

  def closeEvent(self, event) -> None:
    """Implements a graceful shutdown of widgets and timers."""
    self.equalizer.valueTimer.stop()
    self.equalizer.close()
    self.titleLabel.close()
    QDialog.closeEvent(self, event)
