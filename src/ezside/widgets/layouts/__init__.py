"""The 'layouts' package provides a simplified set of class for organizing
placement and sizing of widgets. Please note that these simplifications
come at the cost of some functionality in particular for dynamic layout
management. These classes are intended for use in static layouts where
complexity comes widgets nesting other widgets to achieve abstracted
functionality. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._align_box import AlignBox
from ._abstract_layout import AbstractLayout
from ._horizontal_layout import HorizontalLayout
from ._vertical_layout import VerticalLayout
from ._grid_layout import GridLayout
