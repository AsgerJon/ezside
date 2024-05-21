"""VerticalSeparator widget provides a vertical separator widget. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.widgets.spacers import AbstractSeparator


class VerticalSeparator(AbstractSeparator):
  """VerticalSeparator widget provides a vertical separator widget. """

  def _getHorizontalFlag(self) -> bool:
    """Returns the horizontal flag. True indicates that the separator should
    occupy horizontal space."""
    return False

  def _getVerticalFlag(self) -> bool:
    """Returns the vertical flag. True indicates that the separator should
    occupy vertical space."""
    return True

  def initUi(self) -> None:
    """Sets minimum size"""
    AbstractSeparator.initUi(self)
    self.setMinimumSize(4, 32)
