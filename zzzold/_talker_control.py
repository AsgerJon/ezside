"""TalkerControl class provides the control buttons for the TalkerWindow
dialog."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QMargins, Qt
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from attribox import AttriBox
from vistutils.parse import maybe

from ezside.core import AlignLeft, \
  parseAlignment, \
  Tight, \
  Prefer, \
  VERTICAL, \
  EZTimer, Precise, parsePen, SolidLine
from ezside.core import parseMargins, parseOrientation
from ezside.core import HORIZONTAL
from ezside.dialogs import YRURunning
from ezside.widgets import CanvasWidget, \
  BaseWidget, \
  ImgView
from ezside.widgets import Label
from ezside.widgets.buttons import PushButton
from ezside.widgets.spacers import HorizontalSpacer, VerticalSeparator


class TalkerControl(CanvasWidget):
  """TalkerControl class provides the control buttons for the TalkerWindow
  dialog. """

  __fallback_alignment__ = AlignLeft
  __fallback_margins__ = QMargins(4, 4, 4, 4)
  __fallback_orientation__ = HORIZONTAL

  __inner_state__ = None

  timer = EZTimer(100, Precise, singleShot=False)

  horizontalLayout = AttriBox[QHBoxLayout]()
  verticalLayout = AttriBox[QVBoxLayout]()
  baseWidget = AttriBox[BaseWidget]()

  leftSpacer = AttriBox[HorizontalSpacer]()
  leftSeparator = AttriBox[VerticalSeparator]()
  topSpacer = AttriBox[HorizontalSpacer]()
  topSeparator = AttriBox[HorizontalSpacer]()
  rightSpacer = AttriBox[HorizontalSpacer]()
  rightSeparator = AttriBox[VerticalSeparator]()
  bottomSpacer = AttriBox[HorizontalSpacer]()
  bottomSeparator = AttriBox[HorizontalSpacer]()

  logo = AttriBox[ImgView](icon='risitas')
  startButton = AttriBox[PushButton]('Start')
  stopButton = AttriBox[PushButton]('Stop')
  runIndicator = AttriBox[YRURunning]()
  runLabel = AttriBox[Label]()

  def __init__(self, *args, **kwargs) -> None:
    CanvasWidget.__init__(self, *args, **kwargs)
    orientation = parseOrientation(*args, **kwargs)
    self.orientation = maybe(orientation, self.__fallback_orientation__)
    contentMargins = parseMargins(*args, **kwargs)
    self.contentMargins = maybe(contentMargins, self.__fallback_margins__)
    alignment = parseAlignment(*args, **kwargs)
    self.alignment = alignment or self.__fallback_alignment__
    self.__inner_state__ = False
    if self.orientation == HORIZONTAL:
      self.setSizePolicy(Prefer, Tight)
    elif self.orientation == VERTICAL:
      self.setSizePolicy(Tight, Prefer)

  def horizontalInit(self) -> None:
    """Initializes horizontally"""
    self.horizontalLayout.setContentsMargins(self.contentMargins)
    self.horizontalLayout.setSpacing(0)
    self.horizontalLayout.setAlignment(self.alignment)
    self.logo.initUi()
    self.horizontalLayout.addWidget(self.logo)
    self.leftSeparator.initUi()
    self.horizontalLayout.addWidget(self.leftSeparator)
    self.startButton.initUi()
    self.startButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    self.horizontalLayout.addWidget(self.startButton)
    self.stopButton.initUi()
    self.stopButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    self.horizontalLayout.addWidget(self.stopButton)
    self.runIndicator.initUi()
    self.horizontalLayout.addWidget(self.runIndicator)
    self.runLabel.initUi()
    self.horizontalLayout.addWidget(self.runLabel)
    self.setLayout(self.horizontalLayout)

  def initUi(self) -> None:
    """Sets up the widgets"""
    self.horizontalInit()

  def initSignalSlot(self) -> None:
    """Connects signals and slots"""
    self.startButton.setEnabled(True)
    self.stopButton.setEnabled(False)
    self.startButton.singleLeft.connect(self.activate)
    self.stopButton.singleLeft.connect(self.deactivate)
    self.timer.timeout.connect(self.runIndicator.update)

  def activate(self, **kwargs) -> None:
    """Activates the talker"""
    self.__inner_state__ = True
    self.startButton.disable()
    self.stopButton.enable()
    self.timer.start()
    interval = self.timer.interval()
    self.runLabel.text = 'Running with\ninterval: %dms' % interval
    self.runLabel.forceStyle('textPen', self.getActivePen())
    self.update()

  def deactivate(self, **kwargs) -> None:
    """Deactivates the talker"""
    self.__inner_state__ = False
    self.stopButton.disable()
    self.startButton.enable()
    self.timer.stop()
    interval = self.timer.interval()
    self.runLabel.text = 'Paused with \ninterval: %dms' % interval
    self.runLabel.forceStyle('textPen', self.getInactivePen())
    self.update()

  @staticmethod
  def getActivePen() -> QPen:
    """Getter-function for the active pen"""
    return parsePen(QColor(0, 63, 0, 255), 1, SolidLine)

  @staticmethod
  def getInactivePen() -> QPen:
    """Getter-function for the inactive pen"""
    return parsePen(QColor(63, 0, 0, 255), 1, SolidLine)
