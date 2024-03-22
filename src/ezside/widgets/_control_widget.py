"""ControlWidget provides a collection of buttons for controlling
start/stop and timed behaviour."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, \
  QBoxLayout
from attribox import AttriBox
from icecream import ic
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from ezside.core import Tight
from ezside.widgets import BaseWidget, VSpacer, HSpacer, AbstractSpacer


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


class AbstractControl(BaseWidget):
  """ControlWidget provides a collection of buttons for controlling
  start/stop and timed behaviour."""

  start = Signal()
  stop = Signal()
  pause = Signal()

  startButton = AttriBox[PushButton]('Start')
  pauseButton = AttriBox[PushButton]('Pause')
  stopButton = AttriBox[PushButton]('Stop')

  horizontalSpacer = AttriBox[HSpacer]()
  verticalSpacer = AttriBox[VSpacer]()
  horizontalLayer = AttriBox[QHBoxLayout]()
  verticalLayout = AttriBox[QVBoxLayout]()

  __layout_orientation__ = None

  @abstractmethod
  def getSpacer(self) -> AbstractSpacer:
    """The getSpacer method returns a spacer widget."""

  @abstractmethod
  def getLayout(self) -> QBoxLayout:
    """The getLayout method returns the layout type."""

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.startButton.initUi()
    self.getLayout().addWidget(self.startButton)
    self.pauseButton.initUi()
    self.getLayout().addWidget(self.pauseButton)
    self.stopButton.initUi()
    self.getLayout().addWidget(self.stopButton)
    self.setLayout(self.getLayout())
    self.getLayout().addWidget(self.getSpacer())
    self.connectActions()

  def connectActions(self) -> None:
    """The connectActions method connects the actions of the window."""
    self.startButton.clicked.connect(self.start.emit)
    self.pauseButton.clicked.connect(self.pause.emit)
    self.stopButton.clicked.connect(self.stop.emit)


class VerticalAbstractControl(AbstractControl):
  """VerticalControl provides a collection of buttons for controlling
  start/stop and timed behaviour."""

  def getSpacer(self) -> AbstractSpacer:
    """The getSpacer method returns a spacer widget."""
    return self.verticalSpacer

  def getLayout(self) -> QBoxLayout:
    """The getLayout method returns the layout type."""
    return self.verticalLayout


class HorizontalAbstractControl(AbstractControl):
  """HorizontalControl provides a collection of buttons for controlling
  start/stop and timed behaviour."""

  def getSpacer(self) -> AbstractSpacer:
    """The getSpacer method returns a spacer widget."""
    return self.horizontalSpacer

  def getLayout(self) -> QBoxLayout:
    """The getLayout method returns the layout type."""
    return self.horizontalLayer
