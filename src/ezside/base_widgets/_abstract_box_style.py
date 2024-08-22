"""AbstractBoxStyle provides an abstract base class for style classes for
use by widget classes implementing the box model. The base class specifies
fields that are expected from subclasses. These are then free to implement
fields as appropriate. This is particularly useful for classes requiring
state-sensitive styles. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QMarginsF, QPointF, Qt
from PySide6.QtGui import QColor, QBrush, QPen, QFont
from worktoy.meta import BaseObject

from ezside.tools import FontFamily, FontWeight, Align, FontCap


class AbstractBoxStyle(BaseObject):
  """AbstractBoxStyle provides an abstract base class for style classes for
  use by widget classes implementing the box model. The base class specifies
  fields that are expected from subclasses. These are then free to implement
  fields as appropriate. This is particularly useful for classes requiring
  state-sensitive styles. """

  __box_margins__: QMarginsF = None  # QMarginsF
  __box_borders__: QMarginsF = None  # QMarginsF
  __box_paddings__: QMarginsF = None  # QMarginsF
  __corner_radius__: QPointF = None  # QPointF specification of corner radii
  __padded_color__: QColor = None  # Color of the innermost region
  __border_color__: QColor = None  # Color of the border
  __padded_brush__: QBrush = None  # These depend on the color
  __border_brush__: QBrush = None  # Should NOT be reimplemented
  __pen_color__: QColor = None
  __font_family__: FontFamily = None
  __font_size__: int = None
  __font_weight__: FontWeight = None
  __font_align__: Align = None
  __font_cap__: FontCap = None

  @abstractmethod
  def getFont(self) -> QFont:
    """Getter-function for the font"""

  @abstractmethod
  def getBoxMargins(self) -> QMarginsF:
    """Getter-function for the box margins"""

  @abstractmethod
  def getBoxBorders(self) -> QMarginsF:
    """Getter-function for the box borders"""

  @abstractmethod
  def getBoxPaddings(self) -> QMarginsF:
    """Getter-function for the box paddings"""

  @abstractmethod
  def getCornerRadius(self) -> QPointF:
    """Getter-function for the corner radius specification"""

  @abstractmethod
  def getPaddedColor(self) -> QColor:
    """Getter-function for the color of the innermost region"""

  @abstractmethod
  def getBorderColor(self) -> QColor:
    """Getter-function for the color of the border"""

  def getTextColor(self) -> QColor:
    """Getter-function for the color of the text"""
    return QColor(0, 0, 0, 255)

  @abstractmethod
  def getPaddedBrush(self) -> QBrush:
    """Getter-function for the brush of the padded area"""

  @abstractmethod
  def getBorderBrush(self) -> QBrush:
    """Getter-function for the brush of the border area"""

  def getTextPen(self) -> QPen:
    """Getter-function for the pen of the text"""
    pen = QPen()
    pen.setStyle(Qt.PenStyle.SolidLine)
    pen.setWidth(1)
    pen.setColor(self.getTextColor())
    return pen

  def getAlignment(self) -> Align:
    """Getter-function for the alignment of the text"""
    return Align.CENTER
