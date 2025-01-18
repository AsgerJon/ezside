"""The 'qol.app.widgets' module provides widgets used by the application."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._abstract_widget import AbstractWidget, PaintJob
from ._layout_index import LayoutIndex
from ._layout import Layout
from ._abstract_button import AbstractButton
from ._text_widget import TextWidget
from ._push_button_config import PushButtonConfig
from ._push_button import PushButton
from ._press_hold_button import PressHoldButton

#
# from ._state_widget import StateWidget, PaintJob
# from ._state_indicator import StateIndicator
# from ._box_widget import BoxWidget

__all__ = [
    'AbstractWidget',
    'PaintJob',
    'LayoutIndex',
    'Layout',
    'AbstractButton',
    'TextWidget',
    'PushButtonConfig',
    'PushButton',
    'PressHoldButton',
]
