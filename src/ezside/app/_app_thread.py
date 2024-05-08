"""Subclass of QThread allowing for the running instance of App to
gracefully handle the threads. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Any, TYPE_CHECKING

from PySide6.QtCore import QThread, Slot, QCoreApplication, Signal
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

  errorExit = Signal()
  critExit = Signal()

  def __init__(self, *args, **kwargs) -> None:
    app = QCoreApplication.instance()
    if TYPE_CHECKING:
      assert isinstance(app, App)
    app.registerThread(self)
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
  def initiateQuit(self, startTime: int = None, **kwargs) -> None:
    """Request the thread to quit."""
    if not self.isRunning():
      return
    self.__termination_flag__ = True
    settings = AppSettings()
    key = '%s/graceTime' % self.__class__.__name__
    fb = 5000
    if self.wait(settings.value(key, fb)):
      return
    e = """Thread '%s' of type: '%s' failed to finish in the allotted 
    time!""" % (str(self), self.__class__.__name__)
    self.errorExit.emit()
    raise TimeoutError(monoSpace(e))

  @Slot()
  def forceQuit(self, ) -> None:
    """This method uses more force to stop the thread."""
    self.terminate()
    settings = AppSettings()
    key = '%s/cringeTime' % self.__class__.__name__
    fb = 5000
    if self.wait(settings.value(key, fb)):
      return
    self.critExit.emit()
    e = """Thread '%s' of type: '%s' failed terminate in the allotted 
    time!""" % (str(self), self.__class__.__name__)
    raise RuntimeError(e)
