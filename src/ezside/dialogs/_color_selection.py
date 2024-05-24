"""ColorSelection implements access to the color selection dialog through
the descriptor protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QColorDialog
from vistutils.parse import maybe

from ezside.app import EZDesc
from ezside.desc import ColNotNative, parseColor

if TYPE_CHECKING:
  from ezside.windows import BaseWindow as Win

ColDialog = QColorDialog


class ColorSelection(EZDesc):
  """ColorSelection implements access to the color selection dialog through
  the descriptor protocol."""

  __init_color__ = None
  __fallback_init_color__ = QColor(255, 255, 255, 255)

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the ColorSelection."""
    EZDesc.__init__(self, *args, **kwargs, )
    color = parseColor(*self.getArgs(), **self.getKwargs())
    self.__init_color__ = maybe(color, self.__fallback_init_color__)

  def getContentClass(self) -> type:
    """Returns the content class."""
    return QColorDialog

  def create(self, instance: Win, owner: type, **kwargs) -> ColDialog:
    """Create the content."""
    dialog = QColorDialog()
    dialog.setCurrentColor(self.__init_color__)
    dialog.setOption(ColNotNative)
    return dialog
