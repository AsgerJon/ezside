"""Flag implements the descriptor protocol with the slot and signal system
used in the PySide6.QtCore module. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.parse import maybe
from worktoy.desc import CoreDescriptor


class Flag(CoreDescriptor):
  """Flag implements the descriptor protocol with the slot and signal system
  used in the PySide6.QtCore module. """

  __fallback_default__ = False
  __default_value__ = None

  def _getDefault(self, ) -> bool:
    out = maybe(self.__default_value__, self.__fallback_default__)
    return True if out else False
 