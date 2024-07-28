"""SevenSeg provides a widget representation of a seven segment display."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize, QSizeF, QPoint
from worktoy.keenum import KeeNum, auto
from worktoy.text import typeMsg

from ezside.widgets import BoxWidget


class Segment(KeeNum):
  """Segment provides an enumeration of the seven segments of a seven
  segment display."""

  A = auto((0, 2, 3, 5, 6, 7, 8, 9))
  B = auto((0, 1, 2, 3, 4, 7, 8, 9))
  C = auto((0, 1, 3, 4, 5, 6, 7, 8, 9))
  D = auto((0, 2, 3, 5, 6, 8, 9))
  E = auto((0, 2, 6, 8))
  F = auto((0, 4, 5, 6, 8, 9))
  G = auto((2, 3, 4, 5, 6, 8, 9))

  def state(self, digit: int) -> bool:
    """Determines the state of the segment given the digit to be
    displayed."""
    return True if digit in self.value else False


class SevenSeg(BoxWidget):
  """SevenSeg provides a widget representation of a seven segment display."""

  @classmethod
  def getLongSide(cls, size: QSizeF | QSize) -> int:
    """Determines the long side of a segment given the size of the
    segment. The size is assumed to be the size available to the drawing
    with all margins subtracted. """
    if isinstance(size, QSizeF):
      return cls.getLongSide(size.toSize())
    return size.width()

  @classmethod
  def getShortSide(cls, size: QSizeF | QSize) -> int:
    """Determines the short side of a segment given the size of the
    segment. The size is assumed to be the size available to the drawing
    with all margins subtracted. """
    longSide = cls.getLongSide(size)
    return int((size.height() - 2 * longSide) / 3)

  @classmethod
  def getSegmentCenters(cls, size: QSizeF | QSize) -> dict[Segment, QPoint]:
    """Determines the centers of the segments given the size of the
    segment. The size is assumed to be the size available to the drawing
    with all margins subtracted. """
