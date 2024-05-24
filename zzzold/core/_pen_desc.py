"""PenDesc provides a descriptor protocol for the QPen class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPen

from ezside.app import EZDesc
from ezside.core import parsePen


class Pen(EZDesc):
  """PenDesc provides a descriptor protocol for the QPen class. """

  def __init__(self, *args, **kwargs) -> None:
    EZDesc.__init__(self, *args, **kwargs, )

  def getContentClass(self) -> type:
    """Returns the content class."""
    return QPen

  def create(self, instance: type, owner: type, **kwargs) -> QPen:
    """Create the content."""
    pen = parsePen(*self.getArgs(), **self.getKwargs())
    if isinstance(pen, QPen):
      return pen
    pen = self.settings.value(self.__settings_id__)
    if isinstance(pen, QPen):
      return pen
