"""VerticalLayout provides a layout, which explicitly exposes its
basewidgets.
"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from worktoy.parse import maybe

from ezside.layouts import AbstractLayout, LayoutItem
from ezside.basewidgets import BoxWidget


class VerticalLayout(AbstractLayout):
  """VerticalLayout subclasses AbstractLayout providing a single column
  layout."""
