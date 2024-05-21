"""EZObject class should be used as the second baseclass when creating
core class or entry point classes that inherit from fundamental classes in
the PySide6 package."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Never, Any

from icecream import ic
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from ezside.app import Settings, AppDesc

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class EZObject:
  """EZObject class should be used as the second baseclass when creating
  core class or entry point classes that inherit from fundamental classes in
  the PySide6 package."""

  __settings_id__ = None

  app = AppDesc()
  settings = Settings()

  def __init__(self, *args, **kwargs) -> Never:
    """This implementation stops arguments from reaching object.__init__
    and raising irrelevant exceptions."""
    styleKeys = stringList("""id, settingsId""")
    for key in styleKeys:
      if key in kwargs:
        val = kwargs.get(key, )
        if isinstance(val, str):
          self.__settings_id__ = val
          break
        e = typeMsg(key, val, str)
        raise TypeError(e)
    else:
      for arg in args:
        if isinstance(arg, str):
          self.__settings_id__ = arg
          break
      else:
        self.__settings_id__ = 'normal'

  def getId(self) -> str:
    """Return the unique identifier of the object."""
    return self.__settings_id__

  def getState(self) -> str:
    """Return the state of the object."""
    return 'base'

  def getSettingsKey(self, name: str) -> Any:
    """Returns the key including the settings id and the object state."""
    base, state = self.getId(), self.getState()
    return '%s/%s/%s' % (base, state, name)

  def getSetting(self, settingsName: str, value: Any) -> Any:
    """Sets the settings value for the given settings name along with
    the settings id and the state of the object. """
    key = self.getSettingsKey(settingsName)
    return self.settings(key)

  def setSettings(self, settingsName: str, value: Any) -> None:
    """Sets the settings value for the given settings name along with
    the settings id and the state of the object. """
    key = self.getSettingsKey(settingsName)
    self.settings.setValue(key, value)
