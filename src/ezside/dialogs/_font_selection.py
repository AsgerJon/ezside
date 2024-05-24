"""FontSelection implements the descriptor protocol for font selection
dialogs."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QFontDialog

from ezside.app import EZDesc
from ezside.desc import FontNotNative

if TYPE_CHECKING:
  from ezside.windows import BaseWindow


class FontSelection(EZDesc):
  """FontSelection implements the descriptor protocol for font selection
  dialogs."""

  def getContentClass(self) -> type:
    """Returns the content class for the font selection dialog."""
    return QFontDialog

  def create(self, instance: BaseWindow, owner: type, **kwargs) -> Any:
    """Creates the font selection dialog."""
    dialog = QFontDialog()
    dialog.setOption(FontNotNative)
    return dialog
