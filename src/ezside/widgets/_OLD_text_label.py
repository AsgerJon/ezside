"""TextLabel provides a property driven alternative to QLabel. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from PySide6.QtCore import QSize, QRect, QMargins, Qt, QPoint, QMarginsF, \
  QRectF
from PySide6.QtGui import (QFont, QFontMetrics, QPaintEvent, QPainter,
                           QColor, QPen, QBrush, QFontMetricsF)
from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QGridLayout
from icecream import ic
from worktoy.desc import AttriBox, Field
from worktoy.parse import maybe
from worktoy.text import typeMsg

from ezside.tools import textPen, Align, emptyBrush, emptyPen, fillBrush, \
  parsePen
from ezside.widgets import BoxWidget

ic.configureOutput(includeContext=True)


class TextLabel(BoxWidget):
  """TextLabel provides a property driven alternative to QLabel. """

  __fallback_weight__ = QFont.Weight.Normal
  __font_weight__ = None
  __text_alignment__ = None

  text = AttriBox[str]('LMAO')
  textColor = AttriBox[QColor](QColor(0, 0, 0, 255))
  fontFamily = AttriBox[str]('Courier')
  fontSize = AttriBox[int](12)

  alignment = Field()
  fontWeight = Field()
  textFont = Field()
  metrics = Field()
  textRect = Field()
  pen = Field()

  @alignment.GET
  def getAlignment(self) -> Align:
    """This method returns the alignment of the text label. """
    alignment = maybe(self.__text_alignment__, Align.CENTER)
    if isinstance(alignment, Align):
      return alignment
    e = typeMsg('alignment', alignment, Align)
    raise TypeError(e)

  @alignment.SET
  def setAlignment(self, alignment: Align) -> None:
    """This method sets the alignment of the text label. """
    if not isinstance(alignment, Align):
      e = typeMsg('alignment', alignment, Align)
      raise TypeError(e)
    self.__text_alignment__ = alignment

  @fontWeight.GET
  def getFontWeight(self) -> QFont.Weight:
    """This method returns the font weight of the text label. """
    weight = maybe(self.__font_weight__, self.__fallback_weight__)
    if isinstance(weight, QFont.Weight):
      return weight
    e = typeMsg('weight', weight, QFont.Weight)
    raise TypeError(e)

  @fontWeight.SET
  def setFontWeight(self, weight: QFont.Weight) -> None:
    """This method sets the font weight of the text label. """
    if not isinstance(weight, QFont.Weight):
      e = typeMsg('weight', weight, QFont.Weight)
      raise TypeError(e)
    self.__font_weight__ = weight

  @textFont.GET
  def getTextFont(self) -> QFont:
    """This method returns the font used by the text label. """
    out = QFont()
    out.setFamily(self.fontFamily)
    out.setPointSize(self.fontSize)
    return out

  @textFont.SET
  def setTextFont(self, font: QFont) -> None:
    """This method decomposes the font into its components and sets
    relevant attributes to match. """
    if not isinstance(font, QFont):
      e = typeMsg('font', font, QFont)
      raise TypeError(e)
    family = QFont.family(font)
    size = QFont.pointSize(font)
    weight = QFont.weight(font)
    self.fontFamily = family
    self.fontSize = size
    self.fontWeight = weight
    self.adjustSize()
    self.update()

  @metrics.GET
  def getMetrics(self) -> QFontMetricsF:
    """This method returns the font metrics of the text label. """
    metrics = QFontMetrics(self.textFont)
    return QFontMetricsF(metrics)

  @textRect.GET
  def getBoundingRect(self) -> QRectF:
    """This method returns the bounding size of the text with the given
    font. """
    align = Align.CENTER
    rect = self.metrics.boundingRect(self.contentRect, align.qt, self.text)
    return self.alignment.fitRectF(rect, self.contentRect)

  @pen.GET
  def getTextPen(self) -> QPen:
    """This method returns the pen used to draw the text. """
    return textPen(self.textColor)

  @alignment.DELETE
  @textRect.SET
  @textRect.DELETE
  @metrics.SET
  @metrics.DELETE
  @pen.SET
  @pen.DELETE
  @textFont.DELETE
  @fontWeight.DELETE
  def _badAccessor(self, *_) -> Never:
    """Illegal accessor function"""
    e = """Tried illegally accessing an attribute!"""
    raise TypeError(e)

  @text.ONSET
  def updateState(self, *args) -> None:
    """This method is triggered when the text at the text field is
    changed. """
    self.adjustSize()
    self.update()

  def __init__(self, *args, **kwargs) -> None:
    parent, text = None, None
    for arg in args:
      if isinstance(arg, QWidget) and parent is None:
        parent = arg
      if isinstance(arg, str) and text is None:
        text = arg
      if parent is not None and text is not None:
        BoxWidget.__init__(self, parent)
        self.text = text
        break
    else:
      if parent is None:
        BoxWidget.__init__(self, )
      else:
        BoxWidget.__init__(self, parent)

  def sizeHint(self) -> QSize:
    """This method returns the size hint of the widget."""
    origin, size0 = QPoint(0, 0), QSize(69, 420)
    rect0 = QRect(origin, size0)
    align = Align.CENTER.qt
    rect = self.metrics.boundingRect(rect0, align, self.text)
    rect = rect.marginsAdded(self.allMargins)
    return rect.toRect().size()

  def minimumSizeHint(self) -> QSize:
    """This method returns the minimum size hint of the widget."""
    return self.metrics.tightBoundingRect(self.text).toRect().size()

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation of the paint event"""
    BoxWidget.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    painter.setFont(self.textFont)
    painter.setPen(self.pen)
    painter.setBrush(fillBrush(QColor(144, 255, 0, 31)))
    rect = self.textRect
    # painter.drawRect(rect)
    painter.drawRect(viewRect)
    rect.moveCenter(viewRect.center())

    painter.drawText(viewRect, Qt.AlignmentFlag.AlignCenter, self.text)
    painter.end()


class Label(TextLabel):
  """Label provides a property driven alternative to QLabel. """

  baseLayout = AttriBox[QGridLayout]()
  innerLabel = AttriBox[TextLabel]('YOLO')
  innerMargins = Field()

  def getFontWeight(self) -> QFont.Weight:
    """This method returns the font weight of the text label. """
    return self.innerLabel.getFontWeight()

  def setFontWeight(self, weight: QFont.Weight) -> None:
    """This method sets the font weight of the text label. """
    self.innerLabel.setFontWeight(weight)

  def getTextFont(self) -> QFont:
    """This method returns the font used by the text label. """
    return self.innerLabel.getTextFont()

  def setTextFont(self, font: QFont) -> None:
    """This method decomposes the font into its components and sets
    relevant attributes to match. """
    self.innerLabel.setTextFont(font)

  def getMetrics(self) -> QFontMetrics:
    """This method returns the font metrics of the text label. """
    return self.innerLabel.getMetrics()

  def getBoundingRect(self) -> QRect:
    """This method returns the bounding size of the text with the given
    font. """
    return self.innerLabel.getBoundingRect()

  def getTextPen(self) -> QPen:
    """This method returns the pen used to draw the text. """
    return self.innerLabel.getTextPen()

  def updateState(self, *args) -> None:
    """This method is triggered when the text at the text field is
    changed. """
    self.innerLabel.updateState(*args)

  def initUi(self) -> None:
    """This method initializes the user interface."""
    self.innerLabel.alignment = Align.CENTER
    self.margins = QMarginsF(4, 4, 4, 4, )
    self.borders = QMarginsF(1, 1, 1, 1, )
    self.paddings = QMarginsF(4, 4, 4, 4, )
    self.baseLayout.setContentsMargins(self.allMargins.toMargins())
    self.baseLayout.setSpacing(0)
    self.baseLayout.setAlignment(self.alignment.qt)
    self.baseLayout.addWidget(self.innerLabel, 0, 0)
    self.setLayout(self.baseLayout)

  def __init__(self, *args) -> None:
    parent, text = None, None
    for arg in args:
      if isinstance(arg, QWidget) and parent is None:
        parent = arg
      elif isinstance(arg, str) and text is None:
        text = arg
      if parent is not None and text is not None:
        break
    else:
      text = maybe(text, 'blabla')
    TextLabel.__init__(self, parent)
    self.innerLabel.text = text
    self.initUi()

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paint event implementation fill with blank paint"""
    painter = QPainter()
    painter.begin(self)
    painter.setPen(parsePen(QColor(0, 0, 0, 255), 4))
    painter.setBrush(emptyBrush())
    viewRect = painter.viewport()
    innerView = QRect(QPoint(0, 0, ), viewRect.size())
    innerView = innerView.marginsRemoved(QMargins(4, 4, 4, 4, ))
    innerView.moveCenter(viewRect.center())
    painter.drawRect(innerView)
    painter.end()
