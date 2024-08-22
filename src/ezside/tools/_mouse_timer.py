"""MouseTimer provides a subclass of QTimer specifically intended for use
by the 'BaseButton' class to provide advanced support for mouse events. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QTimer, QObject, Qt


class MouseTimer(QTimer):
  """MouseTimer provides a subclass of QTimer specifically intended for use
  by the 'BaseButton' class to provide advanced support for mouse events. """

  def __init__(self, parent: QObject, interval: int) -> None:
    QTimer.__init__(self, parent)
    self.setSingleShot(True)
    self.setInterval(interval)
    self.setTimerType(Qt.TimerType.PreciseTimer)

  def __bool__(self, ) -> bool:
    """True when instance is active and False when inactive."""
    return True if self.isActive() else False
