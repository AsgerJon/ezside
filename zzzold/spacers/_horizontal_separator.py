"""HorizontalSeparator provides a horizontal line that can be used to
separate widgets in a layouts."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.widgets.spacers import AbstractSeparator


class HorizontalSeparator(AbstractSeparator):
  """HorizontalSeparator provides a horizontal line that can be used to
  separate widgets in a layouts. """

  def _getHorizontalFlag(self) -> bool:
    """Returns the horizontal flag. True indicates that the spacer should
    occupy horizontal space."""
    return True

  def _getVerticalFlag(self) -> bool:
    """Returns the vertical flag. True indicates that the spacer should
    occupy vertical space."""
    return False

  def initUi(self) -> None:
    """Sets minimum size"""
    AbstractSeparator.initUi(self)
    self.setMinimumSize(32, 4)
