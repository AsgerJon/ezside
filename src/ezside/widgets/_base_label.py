"""BaseLabel provides a widget holding a label"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QFrame
from attribox import AttriBox

from ezside.core import Center
from ezside.widgets import BaseWidget


class BaseLabel(BaseWidget):
  """BaseLabel provides a widget holding a label"""

  text = AttriBox[str]('yolo')
  baseLayout = AttriBox[QVBoxLayout]()
  innerLabel = AttriBox[QLabel]()

  def __init__(self, text: str = 'yolo', *args, **kwargs) -> None:
    self.text = text
    BaseWidget.__init__(self, *args, **kwargs)

  @text.ONSET
  def updateText(self, oldText: str, newText: str) -> None:
    """Updates the text of the label."""
    self.innerLabel.setText(newText)
    self.innerLabel.update()

  def initStyle(self, ) -> None:
    """Initializes the style for the label."""
    font = QFont()
    font.setFamily('Montserrat')
    font.setPointSize(24)
    font.setCapitalization(QFont.Capitalization.SmallCaps)
    self.innerLabel.setFont(font)
    self.innerLabel.setAlignment(Center)
    self.innerLabel.setFrameStyle(QFrame.Shape.Box)

  def initUi(self, ) -> None:
    """Initializes the user interface for the label."""
    self.baseLayout.addWidget(self.innerLabel)
    self.setLayout(self.baseLayout)

  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the label."""
