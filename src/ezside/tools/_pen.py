"""This file provides functions for creating QPen instances."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor
from worktoy.parse import maybe


def emptyPen() -> QPen:
  """Return a QPen with no color and width."""
  pen = QPen()
  pen.setStyle(Qt.PenStyle.NoPen)
  pen.setColor(QColor(0, 0, 0, 0, ))
  return pen


def textPen(color: QColor = None) -> QPen:
  """Creates a QPen suitable for drawing text. The pen will default to
  black, but this can be overridden by passing a color argument."""
  pen = QPen()
  pen.setStyle(Qt.PenStyle.SolidLine)
  pen.setColor(maybe(color, QColor(0, 0, 0, 255)))
  return pen


def dashPen(color: QColor = None) -> QPen:
  """Creates a QPen suitable for drawing dashed lines. The pen will default
  to black, but this can be overridden by passing a color argument."""
  pen = QPen()
  pen.setStyle(Qt.PenStyle.DashLine)
  pen.setColor(maybe(color, QColor(0, 0, 0, 255)))
  return pen


def dotPen(color: QColor = None) -> QPen:
  """Creates a QPen suitable for drawing dotted lines. The pen will default
  to black, but this can be overridden by passing a color argument."""
  pen = QPen()
  pen.setStyle(Qt.PenStyle.DotLine)
  pen.setColor(maybe(color, QColor(0, 0, 0, 255)))
  return pen
