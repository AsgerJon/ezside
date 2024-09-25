"""Config provides a class representation of a configuration."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, Self
from worktoy.meta import BaseObject

from moreworktoy.conf import getRoot


class Config(BaseObject):
  """Config provides a class representation of a configuration."""

  __inner_config__ = None
  __module_name__ = None
  __iter_contents__ = None

  @staticmethod
  def _readConfig(configPath: str) -> dict[str, str]:
    """Read the configuration from the file."""
    with open(configPath, 'r', encoding='utf-8') as f:
      lines = f.readlines()
    out = []
    lines = [i for i in lines if i]
    lines = [i for i in lines if not i.startswith('#')]
    lines = [i for i in lines if len(i.split('=')) == 2]
    return {k: v for (k, v) in [i.split('=') for i in lines]}

  @staticmethod
  def _parseConfig(**config) -> dict[str, object]:
    """Parse the configuration."""
    out = {}
    for k, v in config.items():
      if v.isnumeric():
        v = float(v)
        if v.is_integer():
          out[k] = int(v)
          continue
        out[k] = v
        continue
      if v.lower() in ['true', 'false']:
        out[k] = True if v.lower() == 'true' else False
        continue
      out[k] = v
    return out

  def _getConfigPath(self, ) -> str:
    """Return the path to the configuration file."""
    root = getRoot()
    return """%s/.%s""" % (root, self.__module_name__)

  def __init__(self, moduleName: str, ) -> None:
    """Initializes the configuration."""
    self.__module_name__ = moduleName
    configPath = self._getConfigPath()
    config = self._readConfig(configPath)
    self.__inner_config__ = self._parseConfig(**config)

  def __getitem__(self, key: str, ) -> object:
    """Return the value of the configuration."""
    return self.__inner_config__[key]

  def __setitem__(self, *_) -> Never:
    """Raises a read only error"""
    e = """The configuration is read only!"""
    raise TypeError(e)

  def __iter__(self, ) -> Self:
    """Iterates over the configuration."""
    self.__iter_contents__ = [k for (k, v) in self.__inner_config__.items()]
    return self

  def __next__(self, ) -> object:
    """Returns the next key in the configuration."""
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration
