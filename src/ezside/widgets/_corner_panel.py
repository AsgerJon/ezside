"""CornerPanel provides corners together with horizontal and vertical
panels."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize

from ezside.widgets import VerticalPanel
from settings import Default


class CornerPanel(VerticalPanel):
  """CornerPanel provides corners together with horizontal and vertical
  panels."""

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    m = Default.bannerMargin
    self.setFixedSize(QSize(m, m))
