"""FontSelection provides the font selection dialog window for the main
application window implementing the descriptor protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Union

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFontDialog, QWidget
from attribox import AbstractDescriptor

from ezside.app import EZObject
from ezside.desc import Normal, parseFont
from moreattribox import Wait

THIS = Union[QWidget, EZObject]
SCOPE = type(QObject)


class FontSelection(AbstractDescriptor):
  """FontSelection provides the font selection dialog window for the main
  application window implementing the descriptor protocol."""

  __initial_font__ = None
  __fallback_font__ = Wait('MesloLGS', 12, Normal) @ parseFont

  @staticmethod
  def _create(instance: THIS, owner: SCOPE, ) -> QFontDialog:
    """Creates an instance of the dialog window."""
    fbFont = parseFont('MesloLGS', 12, Normal)
    currentFont = instance.settings.value('font', fbFont)
    if isinstance(instance, QWidget):
      dialog = QFontDialog(currentFont, instance)
    else:
      dialog = QFontDialog(currentFont)
    dialog.setOption(QFontDialog.FontDialogOption.DontUseNativeDialog)
    return dialog

  def __instance_get__(self,
                       instance: THIS,
                       owner: SCOPE,
                       **kwargs) -> Any:
    """Implementation of the getter. The remaining functionality required
    by the descriptor protocol is implemented in the AbstractDescriptor
    class. """
    if instance is None:
      return self
    return self._create(instance, owner)
