"""AppDesc implements the descriptor protocol for pointing to the
singleton instance of the running application. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QCoreApplication
from attribox import AbstractDescriptor


class AppDesc(AbstractDescriptor):
  """AppDesc implements the descriptor protocol for pointing to the
  singleton instance of the running application. """

  def __instance_get__(self, instance: object, owner: type) -> Any:
    """Implementation of the getter. The remaining functionality required
    by the descriptor protocol is implemented in the AbstractDescriptor
    class. """
    if instance is None:
      return self
    return QCoreApplication.instance()
