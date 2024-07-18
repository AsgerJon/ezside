"""SocketThreads class provides threaded socket connections."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from socket import socket, SOCK_STREAM, AF_INET
from typing import TYPE_CHECKING

from PySide6.QtCore import QThread, Signal, QCoreApplication
from worktoy.desc import AttriBox


class SocketThread(QThread):
  """SocketThreads class provides threaded socket connections."""

  __threaded_socket__ = None
  __allow_run__ = True
  host = AttriBox[str]('localhost')
  port = AttriBox[int](42069)
  timeLimit = AttriBox[int](500)
  data = Signal(bytes)
  connected = Signal(str)

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the AppThread instance."""
    QThread.__init__(self, )
    for arg in args:
      if isinstance(arg, int):
        self.loopTime = arg
        break
    app = QCoreApplication.instance()
    if TYPE_CHECKING:
      from ezside.app import App
      assert isinstance(app, App)
    app.registerThread(self)

  def start(self, *args, **kwargs) -> None:
    """Start the thread."""
    self.__threaded_socket__ = socket(AF_INET, SOCK_STREAM)
    self.__threaded_socket__.bind((self.host, self.port))
    self.__threaded_socket__.listen(1)
    QThread.start(self, *args, **kwargs)

  def run(self) -> None:
    """Run the thread."""
    while self.__allow_run__:
      connection, address = self.__threaded_socket__.accept()
      self.connected.emit(str(address))
      with connection:
        while True:
          data = connection.recv(1024)
          if not data:
            break
          if not self.__allow_run__:
            break
          self.data.emit(data)
      connection.close()

  def requestQuit(self) -> None:
    """Request the thread to quit."""
    if TYPE_CHECKING:
      assert isinstance(self.timeLimit, int)
    self.__allow_run__ = False
    self.quit()
    if self.wait(self.timeLimit):
      return self.finished.emit()
    self.terminate()
    if self.wait(self.timeLimit):
      return self.finished.emit()
    raise TimeoutError
