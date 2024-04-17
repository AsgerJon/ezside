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
from vistutils.fields import TextField
from vistutils.text import joinWords, monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import emptyPen, \
  emptyBrush, \
  AlignLeft, \
  Tight, AlignFlag, AlignHCenter, AlignRight, AlignTop, AlignBottom
from ezside.core import AlignVCenter
from ezside.widgets import BaseWidget, \
  Vertical, \
  VerticalSpacer, \
  HorizontalSpacer, Horizontal

ic.configureOutput(includeContext=True, )


class Label(BaseWidget):
  """Label prints centered text"""

  text = TextField()
  hAlign = AttriBox[AlignFlag](AlignLeft)
  vAlign = AttriBox[AlignFlag](AlignVCenter)
  baseLayout = AttriBox[Vertical]()
  hLayout = AttriBox[Horizontal]()
  hWidget = AttriBox[BaseWidget]()
  vLayout = AttriBox[Vertical]()
  innerLabel = AttriBox[QLabel]()
  topSpacer = AttriBox[HorizontalSpacer]()
  bottomSpacer = AttriBox[HorizontalSpacer]()
  leftSpacer = AttriBox[VerticalSpacer]()
  rightSpacer = AttriBox[VerticalSpacer]()

  def _getRow(self) -> int:
    """Returns the row of the label"""
    if self.hAlign == AlignLeft:
      return 0
    if self.hAlign == AlignHCenter:
      return 1
    if self.hAlign == AlignRight:
      return 2

  def _getCol(self) -> int:
    """Returns the column of the label"""
    if self.vAlign == AlignTop:
      return 0
    if self.vAlign == AlignVCenter:
      return 1
    if self.vAlign == AlignBottom:
      return 2
    e = """Vertical alignment must be one of: '%s', but received: '%s'!"""
    bottomName = str(AlignBottom.name)
    centerName = str(AlignVCenter.name)
    topName = str(AlignTop.name)
    alignNames = joinWords(topName, centerName, bottomName, )
    raise ValueError(monoSpace(e % (alignNames, str(self.vAlign))))

  def initUi(self) -> None:
    """The initUi method initializes the user interface."""
    self.innerLabel.setText(self.text)
    if self.hAlign == AlignLeft:
      self.hLayout.addWidget(self.innerLabel)
      self.hLayout.addWidget(self.rightSpacer)
    elif self.hAlign == AlignHCenter:
      self.hLayout.addWidget(self.leftSpacer)
      self.hLayout.addWidget(self.innerLabel)
      self.hLayout.addWidget(self.rightSpacer)
    elif self.hAlign == AlignRight:
      self.hLayout.addWidget(self.leftSpacer)
      self.hLayout.addWidget(self.innerLabel)
    else:
      e = """Horizontal alignment must be one of: '%s', but received:
      '%s'!"""
      rightName = str(AlignRight.name)
      centerName = str(AlignHCenter.name)
      leftName = str(AlignLeft.name)
      alignNames = joinWords(leftName, centerName, rightName)
      raise ValueError(monoSpace(e % (alignNames, str(self.hAlign))))
    self.hWidget.setLayout(self.hLayout)
    if self.vAlign == AlignTop:
      self.vLayout.addWidget(self.hWidget)
      self.vLayout.addWidget(self.bottomSpacer)
    elif self.vAlign == AlignVCenter:
      self.vLayout.addWidget(self.topSpacer)
      self.vLayout.addWidget(self.hWidget)
      self.vLayout.addWidget(self.bottomSpacer)
    elif self.vAlign == AlignBottom:
      self.vLayout.addWidget(self.topSpacer)
      self.vLayout.addWidget(self.hWidget)
    else:
      e = """Vertical alignment must be one of: '%s', but received: '%s'!"""
      bottomName = str(AlignBottom.name)
      centerName = str(AlignVCenter.name)
      topName = str(AlignTop.name)
      alignNames = joinWords(topName, centerName, bottomName, )
      raise ValueError(monoSpace(e % (alignNames, str(self.vAlign))))
    self.setLayout(self.vLayout)

  def update(self) -> None:
    """The update method updates the user interface."""
    self.innerLabel.setText(self.text)
    BaseWidget.update(self)

  def __init__(self, *args, **kwargs) -> None:
    BaseWidget.__init__(self, *args, **kwargs)
    for arg in args:
      if isinstance(arg, str):
        self.text = arg
        break
