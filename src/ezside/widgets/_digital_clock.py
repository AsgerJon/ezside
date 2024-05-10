"""DigitalClock widget uses the SevenSegmentDigit class to display the
current time in a digital clock format. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from datetime import datetime
from typing import Any

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QHBoxLayout

from ezside.core import AlignTop, AlignLeft
from ezside.widgets import BaseWidget, \
  SevenSegmentDigit, \
  CanvasWidget, \
  ColonDisplay


class DigitalClock(CanvasWidget):
  """DigitalClock widget uses the SevenSegmentDigit class to display the
  current time in a digital clock format. """

  hoursTens: SevenSegmentDigit
  hours: SevenSegmentDigit
  colon1: ColonDisplay
  minutesTens: SevenSegmentDigit
  minutes: SevenSegmentDigit
  colon2: ColonDisplay
  secondsTens: SevenSegmentDigit
  seconds: SevenSegmentDigit

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the DigitalClock widget."""
    super().__init__(*args, **kwargs)
    self.baseLayout = QHBoxLayout()
    self.hoursTens = SevenSegmentDigit()
    self.hours = SevenSegmentDigit()
    self.colon1 = ColonDisplay()
    self.minutesTens = SevenSegmentDigit()
    self.minutes = SevenSegmentDigit()
    self.colon2 = ColonDisplay()
    self.secondsTens = SevenSegmentDigit()
    self.seconds = SevenSegmentDigit()
    self.initUi()

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
    """The registerFields method registers the fields of the widget."""
    fields = CanvasWidget.registerFields()
    fields['vAlign'] = AlignTop
    fields['hAlign'] = AlignLeft
    return fields

  @classmethod
  def registerStates(cls) -> list[str]:
    """The registerStates method registers the states of the widget."""
    return ['base', ]

  @classmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """The registerDynamicFields method registers the dynamic fields of the
    widget."""
    return {}

  def detectState(self) -> str:
    """The detectState method detects the state of the widget."""
    return 'base'

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the widget."""
    # self.setSizePolicy(Tight, Prefer)
    self.baseLayout.setAlignment(AlignTop | AlignLeft)
    self.baseLayout.addWidget(self.hoursTens, )
    self.hoursTens.initUi()
    self.baseLayout.addWidget(self.hours, )
    self.hours.initUi()
    self.baseLayout.addWidget(self.colon1, )
    self.colon1.initUi()
    self.baseLayout.addWidget(self.minutesTens, )
    self.minutesTens.initUi()
    self.baseLayout.addWidget(self.minutes, )
    self.minutes.initUi()
    self.baseLayout.addWidget(self.colon2, )
    self.colon2.initUi()
    self.baseLayout.addWidget(self.secondsTens, )
    self.secondsTens.initUi()
    self.baseLayout.addWidget(self.seconds, )
    self.seconds.initUi()
    self.setLayout(self.baseLayout)

  def initSignalSlot(self) -> None:
    """The initSignalSlot method initializes the signal and slot connections
    of the widget."""

  @Slot()
  def refresh(self) -> None:
    """The refresh method refreshes the widget."""
    self.update()

  def update(self) -> None:
    """Checks if the inner value of the widget is different from the
    displayed value and changes before applying parent update."""
    rightNow = datetime.now()
    s, S = int(rightNow.second % 10), int(rightNow.second // 10)
    m, M = int(rightNow.minute % 10), int(rightNow.minute // 10)
    h, H = int(rightNow.hour % 10), int(rightNow.hour // 10)
    self.hoursTens.setInnerValue(s)
    self.hours.setInnerValue(S)
    self.colon1.setInnerValue(m)
    self.minutesTens.setInnerValue(M)
    self.minutes.setInnerValue(h)
    self.colon2.setInnerValue(H)
    BaseWidget.update(self)
