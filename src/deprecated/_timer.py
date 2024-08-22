"""Timer provides a subclass of QTimer providing improved support for use
in AttriBox descriptors."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QMainWindow, QWidget
from worktoy.parse import maybe


class Timer(QTimer, ):
  """Timer provides a subclass of QTimer providing improved support for use
  in AttriBox descriptors."""

  def __init__(self, *args) -> None:
    _parent, _interval, _type, _single = None, None, None, None
    for arg in args:
      if isinstance(arg, QWidget) and _parent is None:
        _parent = arg
      if isinstance(arg, int) and _interval is None:
        _interval = arg
      if isinstance(arg, Qt.TimerType) and _type is None:
        _type = arg
      if isinstance(arg, bool) and _single is None:
        _single = arg
      if all([i is not None for i in [_parent, _interval, _type, _single]]):
        break
    else:
      _parent = maybe(_parent, None)
      _interval = maybe(_interval, 0)
      _type = maybe(_type, Qt.TimerType.PreciseTimer)
      _single = maybe(_single, False)
    QTimer.__init__(self, _parent)
    self.setInterval(_interval)
    self.setTimerType(_type)
    self.setSingleShot(_single)
