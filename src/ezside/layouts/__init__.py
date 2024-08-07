"""The 'ezside.layouts' provides an alternative layout implementation.
This is motivated by the fact that while QLayout does work, it is
absolutely terrible to work with. You will find yourself wasting hours and
hours wondering where your widgets have gone. This nightmare begins the
moment you introduce nested layouts. Which is the very place the layout
system should manage things. So many hours and frustrations has been
wasted trying to find out, why your widget is showing up. So GG QLayout. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._layout_index import LayoutIndex
from ._layout_item import LayoutItem
from ._abstract_layout import AbstractLayout
from ._vertical_layout import VerticalLayout
from ._horizontal_layout import HorizontalLayout
