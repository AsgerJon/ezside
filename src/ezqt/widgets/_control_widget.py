"""ControlWidget provides a collection of buttons for controlling
start/stop and timed behaviour."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QVBoxLayout
from attribox import AttriBox
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from ezqt.core import Tight
from ezqt.widgets import BaseWidget


class PushButton(QPushButton):
  """PushButton provides a button with a signal."""

  def __init__(self, *args, **kwargs) -> None:
    QPushButton.__init__(self, *args, **kwargs)
    self.setSizePolicy(Tight, Tight)
    self.__inner_text__ = None
    textKeys = stringList("""text, msg, message, label, title""")
    for key in textKeys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, str):
          self.__inner_text__ = val
          break
        e = typeMsg('text', val, str)
        raise TypeError(e)
    else:
      for arg in args:
        if isinstance(arg, str):
          self.__inner_text__ = arg
          break
      else:
        self.__inner_text__ = 'Click Me!'

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    pass


class ControlWidget(BaseWidget):
  """ControlWidget provides a collection of buttons for controlling
  start/stop and timed behaviour."""

  start = Signal()
  stop = Signal()
  pause = Signal()

  baseLayout = AttriBox[QVBoxLayout]()
  startButton = AttriBox[PushButton]('Start')
  pauseButton = AttriBox[PushButton]('Pause')
  stopButton = AttriBox[PushButton]('Stop')

  __layout_orientation__ = None

  def __init__(self, *args, **kwargs) -> None:
    BaseWidget.__init__(self, *args, **kwargs)
    self.__layout_orientation__ = 'vertical'
    if isinstance(args[0], str):
      if args[0].lower() in ['vertical', 'horizontal']:
        self.__layout_orientation__ = args[0]

  def getLayoutOrientation(self) -> str:
    """The getLayoutOrientation method returns the layout orientation."""
    return self.__layout_orientation__

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.startButton.initUi()
    self.baseLayout.addWidget(self.startButton)
    self.pauseButton.initUi()
    self.baseLayout.addWidget(self.pauseButton)
    self.stopButton.initUi()
    self.baseLayout.addWidget(self.stopButton)
    self.setLayout(self.baseLayout)

  def connectActions(self) -> None:
    """The connectActions method connects the actions of the window."""
    self.startButton.clicked.connect(self.start)
    self.pauseButton.clicked.connect(self.pause)
    self.stopButton.clicked.connect(self.stop)
