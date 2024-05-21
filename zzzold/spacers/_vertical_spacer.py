"""VerticalSpacer """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.widgets.spacers import AbstractSpacer


class VerticalSpacer(AbstractSpacer):
  """VerticalSpacer provides a horizontal spacer widget. """

  def _getHorizontalFlag(self) -> bool:
    """Returns the horizontal flag. True indicates that the spacer should
    occupy horizontal space."""
    return False

  def _getVerticalFlag(self) -> bool:
    """Returns the vertical flag. True indicates that the spacer should
    occupy vertical space."""
    return True
 