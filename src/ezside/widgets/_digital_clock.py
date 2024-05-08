"""DigitalClock widget uses the SevenSegmentDigit class to display the
current time in a digital clock format. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from datetime import datetime
from typing import Any

from PySide6.QtCore import Slot
from attribox import AttriBox

from ezside.core import Prefer, AlignRight, Tight
from ezside.widgets import BaseWidget, SevenSegmentDigit, ColonDisplay
from ezside.widgets.layouts import HorizontalLayout
from morevistutils import Bag


class DigitalClock(BaseWidget):
  """DigitalClock widget uses the SevenSegmentDigit class to display the
  current time in a digital clock format. """

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
    """The registerFields method registers the fields of the widget."""
    return {}

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

  baseLayout = AttriBox[HorizontalLayout](spacing=0, hAlign=AlignRight, )

  colon = ColonDisplay @ Bag()
  seconds = SevenSegmentDigit @ Bag(key='seconds', styleId='clock')
  secondsTens = SevenSegmentDigit @ Bag(key='secondsTens', styleId='clock')
  minutes = SevenSegmentDigit @ Bag(key='minutes', styleId='clock')
  minutesTens = SevenSegmentDigit @ Bag(key='minutesTens', styleId='clock')
  hours = SevenSegmentDigit @ Bag(key='hours', styleId='clock')
  hoursTens = SevenSegmentDigit @ Bag(key='hoursTens', styleId='clock')

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the widget."""
    self.baseLayout.setSizePolicy(Tight, Prefer)
    self.baseLayout.addWidget(self.hoursTens, key='hoursTens')
    self.baseLayout.addWidget(self.hours, key='hours')
    self.baseLayout.addWidget(self.colon, )
    self.baseLayout.addWidget(self.minutesTens, key='minutesTens')
    self.baseLayout.addWidget(self.minutes, key='minutes')
    self.baseLayout.addWidget(self.colon, )
    self.baseLayout.addWidget(self.secondsTens, key='secondsTens')
    self.baseLayout.addWidget(self.seconds, key='seconds')
    self.baseLayout.initUi()

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
    self.baseLayout['seconds'].setInnerValue(s)
    self.baseLayout['secondsTens'].setInnerValue(S)
    self.baseLayout['minutes'].setInnerValue(m)
    self.baseLayout['minutesTens'].setInnerValue(M)
    self.baseLayout['hours'].setInnerValue(h)
    self.baseLayout['hoursTens'].setInnerValue(H)
    self.baseLayout.update()
