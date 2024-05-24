"""ColorBox implements the EZDesc for color selection dialog boxes."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from ezside.app import EZDesc
from PySide6.QtWidgets import QColorDialog


class ColorBox(EZDesc):
  """ColorBox implements the EZDesc for color selection dialog boxes."""

  def getContentClass(self) -> type:
    """Returns the content class for the color box."""
    return QColorDialog

  def create(self, instance: object, owner: type, **kwargs) -> Any:
    """Creates the color dialog box."""
    currentColor = instance.settings.value(self.settingsId, None)
    if currentColor is None:
      pass
    dialog.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog)
    return dialog
