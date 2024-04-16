"""Label prints centered text"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt, QRect, QRectF
from PySide6.QtGui import QPainter, \
  QPaintEvent, \
  QFontMetrics
from PySide6.QtWidgets import QLabel
from attribox import AttriBox
from icecream import ic
from vistutils.waitaminute import typeMsg

from ezside.core import emptyPen, \
  emptyBrush, \
  AlignLeft, \
  Tight
from ezside.core import AlignVCenter
from ezside.widgets import BaseWidget, Vertical

ic.configureOutput(includeContext=True, )


class Label(BaseWidget):
  """Label prints centered text"""

  text = AttriBox[str]('Label')
  baseLayout = AttriBox[Vertical]()
  innerLabel = AttriBox[QLabel]()

  def initUi(self) -> None:
    """The initUi method initializes the user interface."""
    self.innerLabel.setText(self.text)
    self.baseLayout.addWidget(self.innerLabel)
    self.setLayout(self.baseLayout)

  def update(self) -> None:
    """The update method updates the user interface."""
    self.innerLabel.setText(self.text)
    BaseWidget.update(self)
