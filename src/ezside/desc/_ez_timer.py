"""EZTimer implements the descriptor protocol for QTimer."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QTimer
from attribox import AttriBox

from ezside.app import EZDesc
from ezside.desc import TimerType, Precise


class EZTimer(EZDesc):
  """EZTimer implements the descriptor protocol for QTimer."""

  interval = AttriBox[int]()
  singleShot = AttriBox[bool]()
  timerType = AttriBox[TimerType]()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the EZTimer."""
    super().__init__(*args, **kwargs)
    for arg in args:
      if isinstance(arg, int):
        self.interval = arg
        break
    self.singleShot = False
    self.timerType = Precise

  def getContentClass(self) -> type:
    """Returns the content class. Subclasses should implement this method."""
    return QTimer

  def create(self, instance: type, owner: type, **kwargs) -> QTimer:
    """Create the content. Subclasses should implement this method."""
    timer = QTimer()
    timer.setInterval(self.interval)
    timer.setSingleShot(self.singleShot)
    timer.setTimerType(self.timerType)
    return timer
