"""Timer wraps the QTimer class."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QTimer
from vistutils.parse import maybe
from vistutils.text import stringList

from ezside.core import Precise, TimerType
from settings import Default


class Timer(QTimer):
  """Timer wraps the QTimer class."""

  def __init__(self, *args, **kwargs) -> None:
    interval = None
    timerType = None
    singleShot = None
    intervalKeys = stringList("""interval, time, epoch, period""")
    typeKeys = stringList("""timerType, type, mode""")
    singleShotKeys = stringList("""singleShot, oneShot, once""")
    Keys = [intervalKeys, typeKeys, singleShotKeys]
    for keys in Keys:
      for key in keys:
        if key in kwargs:
          val = kwargs.get(key)
          if key in intervalKeys:
            if isinstance(val, int):
              interval = val
              break
          elif key in typeKeys:
            if isinstance(val, int):
              timerType = val
              break
          elif key in singleShotKeys:
            if isinstance(val, bool):
              singleShot = val
              break
    else:
      for arg in args:
        if isinstance(arg, int):
          interval = arg
        if isinstance(arg, bool):
          singleShot = arg
        if isinstance(arg, TimerType):
          timerType = arg
      interval = maybe(interval, Default.anyTimer)
      timerType = maybe(timerType, Precise)
      singleShot = maybe(singleShot, False)
    QTimer.__init__(self, )
    self.setInterval(interval)
    self.setTimerType(timerType)
    self.setSingleShot(singleShot)
