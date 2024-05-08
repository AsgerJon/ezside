"""DigitalClock widget uses the SevenSegmentDigit class to display the
current time in a digital clock format. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Slot
from attribox import AttriBox

from ezside.core import Prefer, AlignRight, Tight
from ezside.widgets import BaseWidget, SevenSegmentDigit, ColonDisplay
from ezside.widgets.layouts import HorizontalLayout
from morevistutils import Bag


class DigitalClock(BaseWidget):
  """DigitalClock widget uses the SevenSegmentDigit class to display the
  current time in a digital clock format. """

  baseLayout = AttriBox[HorizontalLayout](spacing=0, hAlign=AlignRight, )

  colon = ColonDisplay @ Bag()
  seconds = SevenSegmentDigit @ Bag(key='seconds')
  secondsTens = SevenSegmentDigit @ Bag(key='secondsTens')
  minutes = SevenSegmentDigit @ Bag(key='minutes')
  minutesTens = SevenSegmentDigit @ Bag(key='minutesTens')
  hours = SevenSegmentDigit @ Bag(key='hours')
  hoursTens = SevenSegmentDigit @ Bag(key='hoursTens')

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
