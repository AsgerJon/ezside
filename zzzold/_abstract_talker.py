"""AbstractTalker class providing dialogs for talkers. These continuously
emit a signal of user configurable value. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Signal, QCoreApplication
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout
from attribox import AttriBox

from ezside.core import parseParent
from ezside.dialogs import TalkerControl
from ezside.widgets import BaseWidget, Label
from ezside.widgets.spacers import VerticalSpacer

if TYPE_CHECKING:
  from ezside.windows import BaseWindow, App


class AbstractTalker(QDialog):
  """AbstractTalker class providing dialogs for talkers. These continuously
  emit a signal of user configurable value. """

  baseLayout = AttriBox[QVBoxLayout]()
  baseWidget = AttriBox[BaseWidget]()
  titleBanner = AttriBox[Label]('LMAO', id='title')
  contentWidget = AttriBox[BaseWidget]()
  contentLayout = AttriBox[QHBoxLayout]()
  leftSpacer = AttriBox[VerticalSpacer]()
  rightSpacer = AttriBox[VerticalSpacer]()
  controlWidget = AttriBox[TalkerControl]()

  say = Signal(object)

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args, **kwargs)
    if parent is None:
      app = QCoreApplication.instance()
      if TYPE_CHECKING:
        assert isinstance(app, App)
      parent = app.main
      if TYPE_CHECKING:
        assert isinstance(parent, BaseWindow)
    QDialog.__init__(self, parent)
    parent.requestQuit.connect(self.close)

  def initUi(self) -> None:
    """Initializes the user interface for the widget. """
    self.baseLayout.setSpacing(0)
    self.baseLayout.setContentsMargins(0, 0, 0, 0)
    self.titleBanner.initUi()
    self.baseLayout.addWidget(self.titleBanner)
    self.rightSpacer.initUi()
    self.contentLayout.addWidget(self.rightSpacer)
    self.contentWidget.setLayout(self.contentLayout)
    self.contentWidget.initUi()
    self.baseLayout.addWidget(self.contentWidget)
    self.controlWidget.initUi()
    self.baseLayout.addWidget(self.controlWidget)
    self.setLayout(self.baseLayout)

  def initSignalSlot(self) -> None:
    """Connects the signals and slots for the widget. """
    self.controlWidget.initSignalSlot()

  def show(self, ) -> None:
    """Before invoking the parent show method, the initUi and
    initSignalSlot methods run."""
    self.initUi()
    self.initSignalSlot()
    QDialog.show(self)
