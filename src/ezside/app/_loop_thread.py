"""Subclass of QThread allowing for the running instance of App to
gracefully handle the threads. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time
from time import perf_counter_ns
from typing import Callable, TYPE_CHECKING

from PySide6.QtCore import QThread
from worktoy.desc import AttriBox
from worktoy.parse import maybe

from ezside.app import SocketThread

if TYPE_CHECKING:
  pass


class LoopExit(Exception):
  """LoopExit is raised when the loop is exited."""
  pass


class LoopThread(SocketThread):
  """Subclass of QThread allowing for the running instance of App to
  gracefully handle the threads. """

  __allow_run__ = None
  __force_quit__ = None
  __callback_timer__ = None
  __callback_functions__ = None

  loopTime = AttriBox[int]()

  def _getCallbacks(self) -> list[Callable]:
    """Get the callback functions."""
    return maybe(self.__callback_functions__, [])

  def appendCallback(self, callMeMaybe: Callable) -> None:
    """Append a callback function."""
    existing = maybe(self.__callback_functions__, [])
    self.__callback_functions__ = [*existing, callMeMaybe]

  def CALLBACK(self, callMeMaybe: Callable, ) -> None:
    """Alias for appendCallback"""
    return self.appendCallback(callMeMaybe)

  def CALL(self, callMeMaybe: Callable, ) -> None:
    """Alias for appendCallback"""
    return self.appendCallback(callMeMaybe)

  def start(self, *args, **kwargs) -> None:
    """Start the thread."""
    if self._getCallbacks():
      self.__allow_run__ = True
      QThread.start(self, *args, **kwargs)
    return

  def run(self) -> None:
    """Run the thread."""
    if TYPE_CHECKING:
      assert isinstance(self.loopTime, int)
    self.started.emit()
    while self.__allow_run__:
      tic = perf_counter_ns()
      try:
        self.callback()
      except LoopExit:
        return
      toc = perf_counter_ns() - tic
      if toc > self.loopTime:
        continue
      time.sleep(self.loopTime - toc)

  def callback(self) -> None:
    """Invoke the callbacks"""
    tic = perf_counter_ns()
    for callMeMaybe in self._getCallbacks():
      callMeMaybe()
      if self.__force_quit__:
        raise LoopExit
