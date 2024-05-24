"""SettingsDescriptor subclasses EZDesc providing a descriptor protocol
for settings value. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic

from ezside.app import EZDesc, EZObject

ic.configureOutput(includeContext=True)


class SettingsDescriptor(EZDesc):
  """SettingsDescriptor subclasses EZDesc providing a descriptor protocol
  for settings value. """

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the Brush."""
    EZDesc.__init__(self, *args, **kwargs)

  def getContentClass(self) -> type:
    """Returns the content class. Subclasses should implement this method."""
    raise NotImplementedError

  def create(self, instance: EZObject, owner: type, **kwargs) -> Any:
    """Create the content. Subclasses should implement this method."""
    raise NotImplementedError
