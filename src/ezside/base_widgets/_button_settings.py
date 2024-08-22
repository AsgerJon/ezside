"""ButtonSettings encapsulates the settings for buttons."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import json
import os
from typing import Any

from worktoy.desc import Field
from worktoy.meta import BaseObject
from worktoy.parse import maybe
from worktoy.text import stringList


class ButtonSettings(BaseObject):
  """ButtonSettings encapsulates the settings for buttons."""

  __fallback_file__ = 'mouse_settings.json'
  __file_name__ = None
  __settings_data__ = None

  file = Field()

  @classmethod
  def _getRoot(cls, here: str = None) -> str:
    """Returns path to root directory"""
    if here is None:
      here = os.path.dirname(os.path.abspath(__file__))
    items = os.listdir(here)
    rootItems = stringList("""src, README.md ,LICENSE""")
    for item in rootItems:
      if item not in items:
        parentDir = cls._getRoot(os.path.join(here, '..'))
        return cls._getRoot(os.path.normpath(parentDir))
    else:
      return here

  @classmethod
  def getSettingsPath(cls, e: str = None) -> str:
    """Returns the icon directory path"""
    if e is not None:
      if not os.path.isabs(e):
        e = """Encountered bad path: '%s'!""" % e
        raise ValueError(e)
      if not os.path.exists(e):
        e = """While searching for icon directory '%s' was reached, 
        which does not exist!"""
        raise FileNotFoundError(e)
      if os.path.isfile(e):
        e = """While searching for icon directory '%s' was reached, 
        which is a file!"""
        raise NotADirectoryError(e)
      raise RecursionError

    settingsPath = cls._getRoot()
    for directory in stringList("""src, ezside, base_widgets"""):
      settingsPath = os.path.join(settingsPath, directory)
      settingsPath = os.path.normpath(settingsPath)
      if not os.path.exists(settingsPath):
        return cls.getSettingsPath(settingsPath)
    return settingsPath

  def _getFileName(self) -> str:
    """Getter-function for file name"""
    return maybe(self.__file_name__, self.__fallback_file__)

  @file.GET
  def _getFilePath(self) -> str:
    """Getter-function for the file."""
    here = self.getSettingsPath()
    name = self._getFileName()
    return os.path.normpath(os.path.abspath(os.path.join(here, name)))

  def _getDataSettings(self, ) -> dict:
    """Getter-function for data settings"""
    return maybe(self.__settings_data__, {})

  def _setDataSettings(self, settingsData: dict) -> None:
    """Setter-function for data settings"""
    self.__settings_data__ = settingsData

  def _updateSettings(self, **kwargs) -> None:
    """Updates settings with key value pair"""
    for (key, val) in kwargs.items():
      existing = maybe(self.__settings_data__, {})
      self.__settings_data__ = {**self.__settings_data__, key: val}

  def _saveData(self, ) -> None:
    """Saves data to disk"""
    with open(self.file, 'w', encoding='utf-8') as file:
      json.dump(self._getDataSettings(), file)

  def _loadData(self, ) -> None:
    """Loads data from disk"""
    with open(self.file, 'r', encoding='utf-8') as file:
      self.__settings_data__ = json.load(file)
    for (key, val) in self.__settings_data__.items():
      if isinstance(val, str):
        if val.isnumeric():
          self.__settings_data__[key] = int(val)

  def __getitem__(self, key: str) -> Any:
    """Retrieves the setting at given name"""
    return self._getDataSettings().get(key, None)

  def __setitem__(self, key: str, value: Any) -> None:
    """Updates the settings with key and value"""
    self._updateSettings(**{key: value})

  def __init__(self, ) -> None:
    BaseObject.__init__(self)
    self._loadData()
