"""HorizontalSpacer provides a horizontal spacer widget. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from ezside.widgets.spacers import AbstractSpacer
from moreattribox import Flag


class HorizontalSpacer(AbstractSpacer):
  """HorizontalSpacer provides a horizontal spacer widget. """

  def _getHorizontalFlag(self) -> True:
    """Returns the horizontal flag. True indicates that the spacer should
    occupy horizontal space."""
    return True

  def _getVerticalFlag(self) -> False:
    """Returns the vertical flag. True indicates that the spacer should
    occupy vertical space."""
    return False
