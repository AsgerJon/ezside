"""EZObject class should be used as the second baseclass when creating
core class or entry point classes that inherit from fundamental classes in
the PySide6 package."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from attribox import AttriBox
from icecream import ic
from vistutils.parse import maybe
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from ezside.app import AppDesc

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class EZObject:
  """EZObject class should be used as the second baseclass when creating
  core class or entry point classes that inherit from fundamental classes in
  the PySide6 package."""

  __settings_id__ = None
  __fallback_id__ = 'normal'
  __static_state__ = None
  __fallback_state__ = 'base'
  __ui_initialized__ = None
  __signals_connected__ = None

  app = AppDesc()
  settingsId = AttriBox[str]('__NOT_INITIALIZED__')

  def __init__(self, *args, **kwargs) -> None:
    """This implementation stops arguments from reaching object.__init__
    and raising irrelevant exceptions."""

  def getId(self) -> str:
    """Return the unique identifier of the object."""
    return self.__settings_id__

  def getState(self) -> str:
    """Return the state of the object."""
    return maybe(self.__static_state__, self.__fallback_state__)

  def getSettingsKey(self, name: str) -> Any:
    """Returns the key including the settings id and the object state."""
    base, state = self.getId(), self.getState()
    return '%s/%s/%s' % (base, state, name)

  def getSetting(self, settingsName: str, value: Any) -> Any:
    """Sets the settings value for the given settings name along with
    the settings id and the state of the object. """
    key = self.getSettingsKey(settingsName)
    return self.settings.value(key)

  def setSetting(self, settingsName: str, value: Any) -> None:
    """Sets the settings value for the given settings name along with
    the settings id and the state of the object. """
    key = self.getSettingsKey(settingsName)
    self.settings.setValue(key, value)

  def initUi(self, ) -> None:
    """Initializes the user interface of the object."""
