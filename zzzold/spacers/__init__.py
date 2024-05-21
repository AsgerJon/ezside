"""The 'spacers' module provides widgets for spacing and separation.
Spacers respond to the debug flag which makes them visible, otherwise they
do implement a paint event, but are not visible. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._abstract_spacer import AbstractSpacer
from ._abstract_separator import AbstractSeparator
from ._vertical_spacer import VerticalSpacer
from ._horizontal_spacer import HorizontalSpacer
from ._corner_widget import CornerWidget
from ._horizontal_separator import HorizontalSeparator
from ._vertical_separator import VerticalSeparator
