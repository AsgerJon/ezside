"""Subclass of QThread allowing for the running instance of App to
gracefully handle the threads. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time
from typing import Callable, Any, TYPE_CHECKING, Never

from PySide6.QtCore import QThread, Slot, QCoreApplication
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.app import AppSettings

if TYPE_CHECKING:
  from ezside.app import App


class AppThread(QThread):
  """Subclass of QThread allowing for the running instance of App to
  gracefully handle the threads. """

  __termination_flag__ = None
  __call_me_maybe__ = None

  def __init__(self, *args, **kwargs) -> None:
    app = QCoreApplication.instance()
    if TYPE_CHECKING:
      assert isinstance(app, App)
    app.registerThread(self)
    app.quitRequested.connect(self.requestQuit)
    self.finished.connect(app.maybeQuit)
    QThread.__init__(self, *args, **kwargs)

  def getLoop(self, ) -> Callable:
    """Get the inner loop."""
    if self.__call_me_maybe__ is None:
      e = """Thread loop has not been set!"""
      raise AttributeError(e)
    if callable(self.__call_me_maybe__):
      return self.__call_me_maybe__
    e = typeMsg('__call_me_maybe__', self.__call_me_maybe__, Callable)
    raise TypeError(e)

  def setLoop(self, callMeMaybe: Callable) -> Callable:
    """Set the inner loop."""
    if self.__call_me_maybe__ is not None:
      e = """Thread loop has already been set!"""
      raise AttributeError(e)
    if not callable(callMeMaybe):
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)
    self.__call_me_maybe__ = callMeMaybe
    return callMeMaybe

  def LOOP(self, callMeMaybe: Callable) -> Callable:
    """Set the inner loop."""
    return self.setLoop(callMeMaybe)

  def start(self, *args, ) -> Any:
    """Start the thread."""
    if self.__call_me_maybe__ is None:
      e = """Thread loop has not been set!"""
      raise AttributeError(e)
    self.__termination_flag__ = False
    return QThread.start(self, *args)

  def run(self) -> None:
    """Run the thread."""
    callMeMaybe = self.getLoop()
    while not self.__termination_flag__:
      callMeMaybe()

  @Slot()
  def requestQuit(self, startTime: int = None, **kwargs) -> None:
    """Request the thread to quit."""
    if not self.isRunning():
      e = """Unable to quit thread that is not running!"""
      raise RuntimeError(e)
    self.__termination_flag__ = True
    tic = time.time()
    graceLimit = AppSettings().value('thread/graceTime', 5)
    quitLimit = AppSettings().value('thread/quitTime', 15)
    exitLimit = AppSettings().value('thread/exitTime', 30)
    sig9Limit = AppSettings().value('thread/killTime', 60)
    if TYPE_CHECKING:
      assert isinstance(graceLimit, (int, float))
      assert isinstance(quitLimit, (int, float))
      assert isinstance(sig9Limit, (int, float))
    timeLimits = [graceLimit, quitLimit, sig9Limit]
    if startTime is not None:
      timeLimits = [startTime + t for t in timeLimits]

    def nice(*args) -> None:
      """Nice termination."""
      if self.isRunning():
        r = kwargs.get('recursion', 0)
        if r == 1:
          raise TimeoutError('Unexpected thread state, still running!')
        if r == 2:
          raise RuntimeError('Unexpected thread state, still running!')
        if r == 3:
          raise SystemExit
        t = [10, 20, 35, ]
        return self.requestQuit(startTime=t[r], _recursion=r + 1)

    def grace(*args) -> Never:
      """Graceful termination."""
      ee = """Thread loop failed to terminate upon setting the termination 
      flag!"""
      QThread.quit(self, )
      raise TimeoutError(monoSpace(ee))

    def lastChance(*args, ) -> Never:
      """Last chance for the python interpreter to quit the thread"""
      QThread.terminate(self)
      ee = """Thread still running after 'quit', calling 'terminate'. 
      Please note that this is your last chance to quit the thread before 
      SystemExit!"""
      raise RuntimeError(monoSpace(ee))

    def kill9(*args) -> Never:
      """Kill the python interpreter. No message, no nothing. You had your
      chance. """
      raise SystemExit

    pleaseLeave = [grace, lastChance, kill9]
    for (leave, lim) in zip(pleaseLeave, timeLimits):
      if self.wait(lim):
        break
      leave(self)
