"""ColorSelection provides the color selection dialog window for the main
application window implementing the descriptor protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Union

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QColorDialog, QWidget
from attribox import AbstractDescriptor

from ezside.app import EZObject
from moreattribox import Wait

Shiboken = type(QObject)

THIS = Union[QWidget, EZObject]
SCOPE = type(QObject)


class ColorSelection(AbstractDescriptor):
  """ColorSelection provides the color selection dialog window for the main
  application window implementing the descriptor protocol."""

  __initial_color__ = None
  __fallback_color__ = Wait(0, 0, 0, 255, )

  def _create(self, instance: THIS, owner: SCOPE, ) -> QColorDialog:
    """Creates an instance of the dialog window."""
    fbColor = self.__fallback_color__
    currentColor = instance.settings.value('color', fbColor)
    dialog = QColorDialog(currentColor, instance)
    dialog.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog)
    return dialog

  def __instance_get__(self, instance: THIS, owner: SCOPE) -> Any:
    """Implementation of the getter. The remaining functionality required
    by the descriptor protocol is implemented in the AbstractDescriptor
    class. """
    if instance is None:
      return self
    return self._create(instance, owner)
