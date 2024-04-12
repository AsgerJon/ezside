"""CornerPanel provides corners together with horizontal and vertical
panels."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize

from ezside.widgets import VerticalPanel
from ezside.settings import Defaults


class CornerPanel(VerticalPanel):
  """CornerPanel provides corners together with horizontal and vertical
  panels."""

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    m = Defaults.bannerMargin
    self.setFixedSize(QSize(m, m))
