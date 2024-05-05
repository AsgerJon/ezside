"""BaseLabel provides a widget holding a label"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout
from attribox import AttriBox

from ezside.widgets import BaseWidget


class BaseLabel(BaseWidget):
  """BaseLabel provides a widget holding a label"""

  __inner_label__ = None

  text = AttriBox[str]('yolo')

  def __init__(self, *args, **kwargs) -> None:
    BaseWidget.__init__(self, *args, **kwargs)
    self.__inner_label__ = QLabel()
    self.__inner_label__.setText(self.text)

  @text.ONSET
  def updateText(self, oldText: str, newText: str) -> None:
    """Updates the text of the label."""
    self.text = newText
    self.__inner_label__.setText(self.text)
    self.__inner_label__.update()

  def initStyle(self, ) -> None:
    """Initializes the style for the label."""

  def initUi(self, ) -> None:
    """Initializes the user interface for the label."""
    self.baseLayout.addWidget(self.__inner_label__)
    self.setLayout(self.baseLayout)

  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the label."""
