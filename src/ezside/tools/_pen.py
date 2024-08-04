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


def solidPen(color: QColor = None, ) -> QPen:
  """Creates a QPen suitable for drawing solid lines. The pen will default
  to black, but this can be overridden by passing a color argument."""
  pen = QPen()
  pen.setStyle(Qt.PenStyle.SolidLine)
  pen.setColor(maybe(color, QColor(0, 0, 0, 255)))
  return pen


def dashPen(color: QColor = None, ) -> QPen:
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


def parsePen(*args) -> QPen:
  """Parses the given arguments to an instance of QPen. """
  color, width, style = None, None, None
  for arg in args:
    if isinstance(arg, QColor) and color is None:
      color = arg
    elif isinstance(arg, int) and width is None:
      width = arg
    elif isinstance(arg, Qt.PenStyle) and style is None:
      style = arg
    if color is not None and width is not None and style is not None:
      break
  else:
    color = maybe(color, QColor(0, 0, 0, 255))
    width = maybe(width, 1)
    style = maybe(style, Qt.PenStyle.SolidLine)
  pen = QPen()
  pen.setColor(color)
  pen.setWidth(width)
  pen.setStyle(style)
  return pen
