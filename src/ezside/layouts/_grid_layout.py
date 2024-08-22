"""GridLayout provides a subclass of AbstractLayout implement grid
layouts. When adding widgets to the layout, the row and column must be
specified. Optionally, the rowSpan and colSpan can be specified to
span multiple rows or columns. By default, the rowSpan and colSpan are
1, meaning the widget will only span one row or column."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.layouts import AbstractLayout


class GridLayout(AbstractLayout):
  """GridLayout provides a subclass of AbstractLayout implement grid
  layouts. When adding widgets to the layout, the row and column must be
  specified. Optionally, the rowSpan and colSpan can be specified to
  span multiple rows or columns. By default, the rowSpan and colSpan are
  1, meaning the widget will only span one row or column."""
  pass
