"""Timer provides a subclass of QTimer providing improved support for use
in AttriBox descriptors."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QMainWindow
from worktoy.meta import BaseMetaclass, overload
from worktoy.parse import maybe


class Timer(QTimer, ):
  """Timer provides a subclass of QTimer providing improved support for use
  in AttriBox descriptors."""

  def __init__(self, parent: QMainWindow = None, *args, ) -> None:
    QTimer.__init__(self, parent)
    interval, timerType, singleShot = None, None, None
    for arg in args:
      if isinstance(arg, int) and interval is None:
        interval = arg
      elif isinstance(arg, Qt.TimerType) and timerType is None:
        timerType = arg
      elif isinstance(arg, bool) and singleShot is None:
        singleShot = arg
    self.setInterval(maybe(interval, 1000))
    self.setTimerType(maybe(timerType, Qt.TimerType.CoarseTimer))
    self.setSingleShot(maybe(singleShot, False))

  def _timeout(self) -> None:
    """This method is called when the timer times out. It is intended to be
    overridden by subclasses."""
    pass

  def start(self, *args, **kwargs) -> None:
    """Start the timer with the specified arguments."""
    super().start(*args, **kwargs)

  def stop(self) -> None:
    """Stop the timer."""
    super().stop()
