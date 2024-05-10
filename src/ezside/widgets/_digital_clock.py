"""DigitalClock widget uses the SevenSegmentDigit class to display the
current time in a digital clock format. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from datetime import datetime
from typing import Any

from PySide6.QtGui import QColor
from icecream import ic
from PySide6.QtCore import Slot, QPoint, QMargins
from PySide6.QtWidgets import QHBoxLayout

from ezside.core import AlignTop, \
  AlignLeft, \
  AlignFlag, \
  AlignVCenter, \
  AlignHCenter
from ezside.widgets import BaseWidget, SevenSegmentDigit, CanvasWidget
from ezside.widgets import ColonDisplay

ic.configureOutput(includeContext=True)


class DigitalClock(CanvasWidget):
  """DigitalClock widget uses the SevenSegmentDigit class to display the
  current time in a digital clock format. """

  @classmethod
  def staticStyles(cls) -> dict[str, Any]:
    """The registerFields method registers the fields of the widget.
    Please note, that subclasses can reimplement this method, but must
    provide these same fields. """
    return {
      'margins'        : QMargins(0, 0, 0, 0, ),
      'borders'        : QMargins(2, 2, 2, 2, ),
      'paddings'       : QMargins(0, 0, 0, 0, ),
      'borderColor'    : QColor(0, 0, 0, 255),
      'backgroundColor': QColor(223, 223, 223, 255),
      'radius'         : QPoint(4, 4, ),
      'vAlign'         : AlignVCenter,
      'hAlign'         : AlignHCenter,
    }

  @classmethod
  def styleTypes(cls) -> dict[str, type]:
    """The styleTypes method provides the type expected at each name. """
    return {
      'margins'        : QMargins,
      'borders'        : QMargins,
      'paddings'       : QMargins,
      'borderColor'    : QColor,
      'backgroundColor': QColor,
      'radius'         : QPoint,
      'vAlign'         : AlignFlag,
      'hAlign'         : AlignFlag,
    }

  def dynStyles(self) -> list[str]:
    """The dynStyles method provides the dynamic styles of the widget."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the DigitalClock widget."""
    super().__init__(*args, **kwargs)
    self.baseLayout = QHBoxLayout()
    self.baseLayout.setContentsMargins(0, 0, 0, 0, )
    self.baseLayout.setSpacing(0)
    self.hoursTens = SevenSegmentDigit(id='clock')
    self.hours = SevenSegmentDigit(id='clock')
    self.colon1 = ColonDisplay(id='clock')
    self.minutesTens = SevenSegmentDigit(id='clock')
    self.minutes = SevenSegmentDigit(id='clock')
    self.colon2 = ColonDisplay(id='clock')
    self.secondsTens = SevenSegmentDigit(id='clock')
    self.seconds = SevenSegmentDigit(id='clock')
    self.initUi()

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
