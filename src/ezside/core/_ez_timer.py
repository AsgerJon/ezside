"""EZTimer provides a simplified subclass of QTimer"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg


class EZTimer(QTimer):
  """EZTimer provides a simplified subclass of QTimer"""

  def __init__(self, *args, **kwargs) -> None:
    """EZTimer provides a simplified subclass of QTimer"""
    intervalKeys = stringList("""interval, time, delay, duration""")
    singleShotKeys = stringList("""singleShot, oneShot, oneTime, oneOff""")
    timerTypeKeys = stringList("""timerType, precision, accuracy, type""")
    KEYS = [intervalKeys, singleShotKeys, timerTypeKeys]
    values = dict(interval=None, singleShot=None, timerType=None)
    types = dict(interval=int, singleShot=bool, timerType=Qt.TimerType)
    defaultValues = dict(interval=1000,
                         singleShot=False,
                         timerType=Qt.TimerType.PreciseTimer)
    for (keys, (name, type_)) in zip(KEYS, types.items()):
      for key in keys:
        if key in kwargs:
          val = kwargs[key]
          if isinstance(val, type_):
            values[name] = val
            break
          e = typeMsg(key, val, type_)
          raise TypeError(e)
      else:
        for arg in args:
          if isinstance(arg, type_):
            values[name] = arg
            break
        else:
          values[name] = defaultValues[name]
    QTimer.__init__(self)
    self.setInterval(values['interval'])
    self.setSingleShot(values['singleShot'])
    self.setTimerType(values['timerType'])
