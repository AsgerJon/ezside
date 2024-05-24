"""MarginsDesc provides implements the descriptor protocol for the
QMargins instances. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QMargins, QMarginsF

from ezside.app import EZDesc
from ezside.core import parseMargins


class Margins(EZDesc):
  """MarginsDesc provides implements the descriptor protocol for the
  QMargins instances. """

  def getContentClass(self) -> type:
    """Returns the content class."""
    return QMargins

  def create(self, instance: object, owner: type, **kwargs) -> Any:
    """Create the content."""
    if instance is None:
      return self
    margins = parseMargins(*self.getArgs(), **self.getKwargs())
    if isinstance(margins, QMarginsF):
      return margins.toMargins()
    if isinstance(margins, QMargins):
      return margins
    margins = self.settings.value(self.__settings_id__)
    if isinstance(margins, QMarginsF):
      return margins.toMargins()
    if isinstance(margins, QMargins):
      return margins
