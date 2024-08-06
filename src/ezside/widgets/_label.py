"""Label provides a property driven alternative to QLabel. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from PySide6.QtCore import QSize, QRect, QMargins, Qt, QPoint, QMarginsF, \
  QRectF, QSizeF
from PySide6.QtGui import (QFont, QFontMetrics, QPaintEvent, QPainter,
                           QColor, QPen, QFontMetricsF)
from PySide6.QtWidgets import QWidget, QGridLayout
from icecream import ic
from worktoy.desc import AttriBox, Field, DEFAULT
from worktoy.meta import overload, BaseObject
from worktoy.parse import maybe
from worktoy.text import typeMsg

from ezside.tools import textPen, Align, emptyBrush, fillBrush, parsePen, \
  Font
from ezside.widgets import BoxWidget

ic.configureOutput(includeContext=True)


class _Parse(BaseObject):
  """External overloading class"""

  __parsed_parent__ = None
  __parsed_str__ = None
  __fallback_str__ = 'LABEL'

  parent = Field()
  text = Field()

  @parent.GET
  def _getParent(self) -> QWidget:
    """Getter-function for the parent."""
    return maybe(self.__parsed_parent__, None)

  @text.GET
  def _getText(self) -> str:
    """Getter-function for the text."""
    return maybe(self.__parsed_str__, self.__fallback_str__)

  @overload(str)
  def __init__(self, text: str):
    """Overloaded constructor"""
    self.__parsed_str__ = text

  @overload(QWidget)
  def __init__(self, parent: QWidget):
    """Overloaded constructor"""
    self.__parsed_parent__ = parent

  @overload(str, QWidget)
  def __init__(self, text: str, parent: QWidget):
    """Overloaded constructor"""
    self.__init__(parent, text)

  @overload(QWidget, str)
  def __init__(self, parent: QWidget, text: str):
    """Overloaded constructor"""
    self.__parsed_parent__ = parent
    self.__parsed_str__ = text


class Label(BoxWidget):
  """Label provides a property driven alternative to QLabel. """

  font = AttriBox[Font]()
  text = AttriBox[str](DEFAULT('LMAO'))

  rectSize = Field()

  @rectSize.GET
  def _getRectSize(self) -> QSizeF:
    """This method calculates the size required to bound the text."""
    return QFontMetricsF.boundingRect(self.font.metrics, self.text).size()

  def minimumSizeHint(self) -> QSize:
    """This method returns the size hint of the widget."""
    return QSizeF(self.rectSize.width(), self.rectSize.height()).toSize()

  @text.ONSET
  def hookedTextSet(self, oldText: str, newText: str) -> None:
    """This method is called when the text is set."""
    if oldText != newText:
      self.adjustSize()
      self.update()

  def paintEvent(self, event: QPaintEvent) -> None:
    """Reimplementation"""
    BoxWidget.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    borderRect = QRectF.marginsRemoved(viewRect.toRectF(), self.borders)
    paddedRect = QRectF.marginsRemoved(borderRect, self.paddings)
    self.font @ painter
    painter.drawText(paddedRect, self.font.align.qt, self.text)
    painter.end()

  def __init__(self, *args, ):
    parsed = _Parse(*args)
    BoxWidget.__init__(self, parsed.parent)
    self.text = parsed.text
