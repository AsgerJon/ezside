"""TwoState provides a two state button where the current state is clearly
indicated visually. Further the effectively implements two buttons clearly
separated, each responsible for activating one of the two states. This
provides a debouncing feature. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from typing import Any

from PySide6.QtCore import QMargins, Qt, Signal, QCoreApplication
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLayout
from attribox import AttriBox
from icecream import ic
from vistutils.parse import maybe
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import Precise, SolidFill, parseBrush, AlignTop
from ezside.core import EZTimer
from ezside.core import Orientation, parseOrientation, HORIZONTAL, VERTICAL
from ezside.widgets import CanvasWidget, LayoutDescriptor, GraffitiVandal
from ezside.widgets.buttons import PushButton
from ezside.widgets.spacers import HorizontalSpacer, VerticalSpacer
from ezside.widgets.spacers import AbstractSpacer


class _ToggleButton(PushButton):
  """Slight modification of the PushButton class. """

  _moveTimer = EZTimer(25, Precise, singleShot=True)
  _pressHoldTimer = EZTimer(500, Precise, singleShot=True)
  _releaseTimer = EZTimer(150, Precise, singleShot=True)
  _clickTimer = EZTimer(150, Precise, singleShot=True)  # timeout -> dbl clk
  _doubleReleaseTimer = EZTimer(200, Precise, singleShot=True)
  _doubleClickTimer = EZTimer(125, Precise, singleShot=True)
  turnedOn = Signal()
  turnedOff = Signal()
  deactivated = Signal()

  def _getForcedStyle(self, name: str) -> Any:
    """Returns the forced style."""
    return None

  def getDefaultStyles(self, ) -> dict[str, Any]:
    """Reimplementation of the getDefaultStyles method."""
    base = {}
    margins = QMargins(4, 4, 4, 4, )
    borders = QMargins(4, 4, 4, 4, )
    paddings = QMargins(4, 4, 4, 4, )
    if self.__is_enabled__:
      backgroundColor = QColor(144, 255, 0, 63)
    else:
      backgroundColor = QColor(223, 255, 191, 63)
    if self.__is_hovered__:
      borderColor = QColor(191, 191, 191, 255)
    else:
      borderColor = QColor(15, 15, 15, 0)
    backgroundColor = QColor(144, 255, 0, 255)
    borderColor = QColor(127, 191, 0, 255)
    base['backgroundBrush'] = parseBrush(backgroundColor, SolidFill)
    base['margins'] = margins
    base['borders'] = borders
    base['paddings'] = paddings
    base['borderBrush'] = parseBrush(borderColor, SolidFill)
    return base

  def initSignalSlot(self, ) -> None:
    """Initialize the signal slot."""
    PushButton.initSignalSlot(self)
    self.singleLeft.connect(self.leftClick)
    self.doubleLeft.connect(self.leftDoubleClick)

  def leftClick(self, ) -> None:
    """LEFT CLICK"""
    if not self.__is_enabled__:
      return
    self.__is_enabled__ = False
    self.deactivated.emit()
    self._resetState()
    self.update()

  def activate(self) -> None:
    """Activates the button."""
    self.__is_enabled__ = True
    self._resetState()
    self.update()

  def leftDoubleClick(self) -> None:
    """LEFT DOUBLE CLICK"""

  def __bool__(self) -> bool:
    """Returns True if the button is enabled."""
    return True if self.__is_enabled__ else False


class TwoState(CanvasWidget):
  """TwoState provides a two state button where the current state is clearly
  indicated visually. Further the effectively implements two buttons clearly
  separated, each responsible for activating one of the two states. This
  provides a debouncing feature. """

  __fallback_orientation__ = HORIZONTAL
  __view_rect__ = None

  orientation = Orientation()

  layout = LayoutDescriptor()
  onButton = AttriBox[_ToggleButton]()
  hSpacer = AttriBox[HorizontalSpacer]()
  vSpacer = AttriBox[VerticalSpacer]()
  offButton = AttriBox[_ToggleButton]()

  ON = Signal()
  OFF = Signal()

  def __init__(self, *args, **kwargs) -> None:
    CanvasWidget.__init__(self, *args, **kwargs)
    orientation = parseOrientation(*args, **kwargs)
    self.orientation = maybe(orientation, self.__fallback_orientation__)

  def getMargins(self) -> QMargins:
    """Getter-function for the margins"""
    return QMargins(4, 4, 4, 4, )

  def getSpacer(self) -> AbstractSpacer:
    """Getter-function for the spacer"""
    if self.orientation is HORIZONTAL:
      return self.hSpacer
    if self.orientation is VERTICAL:
      return self.vSpacer

  def initUi(self) -> None:
    """Initializes the user interface."""
    self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    if not isinstance(self.layout, QLayout):
      e = typeMsg('layouts', self.layout, QLayout)
      raise TypeError(e)
    self.layout.setSpacing(8)
    self.layout.setContentsMargins(self.getMargins())
    self.layout.setAlignment(AlignTop)
    self.onButton.initUi()
    self.onButton.setMinimumSize(64, 64)
    self.onButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    self.layout.addWidget(self.onButton)
    if self.orientation is HORIZONTAL:
      self.hSpacer.initUi()
      self.layout.addWidget(self.hSpacer)
    elif self.orientation is VERTICAL:
      self.vSpacer.initUi()
      self.layout.addWidget(self.vSpacer)
    else:
      e = """Unexpected orientation: '%s'!""" % self.orientation
      raise RuntimeError(monoSpace(e))
    self.offButton.initUi()
    self.offButton.setMinimumSize(64, 64)
    self.offButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    self.layout.addWidget(self.offButton)
    self.setLayout(self.layout)

  def initSignalSlot(self) -> None:
    """Initializes the signal slot."""
    ic('two state, init signal slot')
    self.onButton.initSignalSlot()
    self.offButton.initSignalSlot()
    self.onButton.deactivated.connect(self.ON)
    self.offButton.deactivated.connect(self.OFF)
    self.ON.connect(self.offButton.activate)
    self.OFF.connect(self.onButton.activate)

  def getDefaultStyles(self) -> dict:
    """Getter-function for default styles"""
    backgroundColor = QColor(255, 255, 255, 255)
    backgroundBrush = parseBrush(backgroundColor, SolidFill)
    return dict(backgroundBrush=backgroundBrush)

  def customPaint(self, painter: GraffitiVandal) -> None:
    """Custom paint event handler."""
    self.__view_rect__ = painter.customPaintRect()
