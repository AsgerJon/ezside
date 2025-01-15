"""CompoundClick encapsulates a user input event that consist of multiple
consecutive clicks. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QObject
from worktoy.desc import AttriBox, Field, THIS
from worktoy.base import BaseObject, overload
from worktoy.text import typeMsg, monoSpace

from . import MouseRelease


class CompoundClick(QObject):
  """CompoundClick encapsulates a user input event that consist of multiple
  consecutive clicks. """

  def __init__(self, *args) -> None:
    """The parent is understood to be the widget receiving the event. """
    for arg in args:
      if isinstance(arg, QObject):
        QObject.__init__(self, arg)
        break
    else:
      QObject.__init__(self, )
    for arg in args:
      if isinstance(arg, MouseRelease):
        pass
