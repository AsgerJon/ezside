"""The 'widgets' package provides the widgets for the main application
window. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._base_widget import BaseWidget
from ._label import Label
from ._layouts import Grid, Vertical, Horizontal
from ._spacers import HorizontalSpacer, VerticalSpacer, GridSpacer
from ._spacers import AbstractSpacer
