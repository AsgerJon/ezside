"""BaseThread provides a central subclass of QThread allowing all threads
to be centrally managed. The purpose of this class is to ensure thread
safety, but providing a single central mechanism that organizes shutdown
of the threads."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QThread
from threading import Lock

from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.settings import Defaults


class BaseThread(QThread):
  """BaseThread provides a central subclass of QThread allowing all threads
  to be centrally managed. The purpose of this class is to ensure thread
  safety, but providing a single central mechanism that organizes shutdown
  of the threads."""
  __all_threads__ = []
  __thread_lock__ = Lock()
  __fallback_timelimit__ = 1000

  @classmethod
  def _getTimeLimit(cls) -> int:
    """Get the time limit for the thread."""
    with cls.__thread_lock__:
      defaultTimeLimit = Defaults.getThreadTimeLimit()
      if isinstance(defaultTimeLimit, int):
        return defaultTimeLimit
      if defaultTimeLimit is None:
        return cls.__fallback_timelimit__
      e = typeMsg('defaultTimeLimit', defaultTimeLimit, int)
      raise TypeError(e)

  @classmethod
  def appendThread(cls, thread: BaseThread) -> bool:
    """Append the thread to the list of threads."""
    with cls.__thread_lock__:
      cls.__all_threads__.append(thread)

  @classmethod
  def closeAll(cls) -> bool:
    """Close all the threads."""
    with cls.__thread_lock__:
      timeLimit = cls._getTimeLimit()
      while cls.__all_threads__:
        thread = cls.__all_threads__.pop()
        thread.quit()
        if not thread.wait(timeLimit):
          e = """Thread: '%s' did not close within the allotted time!"""
          raise TimeoutError(monoSpace(e % thread))

  def start(self, *args, **kwargs) -> None:
    """Start the thread."""
    BaseThread.appendThread(self)
    QThread.start(self, *args, **kwargs)
