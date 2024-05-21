"""QDescriptor subclasses QObject and AbstractDescriptor combining
support for signals and slot with the descriptor protocol."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from PySide6.QtCore import QObject
from attribox import AbstractDescriptor

from ezside.core import parseParent


class QDescriptor(QObject, AbstractDescriptor):
  """QDescriptor subclasses QObject and AbstractDescriptor combining
  support for signals and slot with the descriptor protocol."""

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args, **kwargs)
    QObject.__init__(self, parent)
    AbstractDescriptor.__init__(self, )

  @abstractmethod
  def __instance_get__(self, instance: object, owner: type, **kwargs) -> Any:
    """The __instance_get__ method is called when the descriptor is accessed
    via the owning instance. """
