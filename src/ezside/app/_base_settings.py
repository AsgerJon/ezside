"""AppSettings subclasses the QSettings class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING, Any, Union, Dict, Optional, List

from PySide6.QtCore import QSettings
from PySide6.QtGui import QKeySequence
from icecream import ic
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True, )

if sys.version_info.minor < 10:
  Type = Union[Dict[str, type], type]
  ShortCut = Union[Dict[str, QKeySequence], QKeySequence]
  ANY = Union[Dict[str, Any], Any]
  StrList = Optional[List[str]]
  StrDict = Union[Dict[str, str], str]
elif sys.version_info.minor > 9:
  Type = dict[str, type] | type
  ShortCut = dict[str, QKeySequence] | QKeySequence
  ANY = dict[str, Any] | Any
  StrList = list[str] | None
  StrDict = dict[str, str] | str


class BaseSettings(QSettings):
  """The 'AppSettings' class provides a convenient interface for
  working with the application's variable settings. """

  __missing_attributes__ = None
  __group_names__ = None
  __open_groups__ = None
  __group_types__ = None
  __group_fallbacks__ = None

  @staticmethod
  def camelCase(name: str) -> str:
    """Converts a string to camel case."""
    if name.startswith('__') and name.endswith('__'):
      return name
    name = '%s%s' % (name[0].upper(), name[1:])
    name = name.replace(' ', '_')
    if '_' not in name:
      return '%s%s' % (name[0].lower(), name[1:])
    words = name.split('_')
    first = '%s%s' % (words[0][0].lower(), words[0][1:])
    rest = [word.capitalize() for word in words[1:]]
    return '%s%s' % (first, ''.join(rest))

  @staticmethod
  def snakeCase(name: str) -> str:
    """Converts a string to snake case."""
    if name.startswith('__') and name.endswith('__'):
      return name
    name = '%s%s' % (name[0].upper(), name[1:])
    name = name.replace(' ', '_')
    chars = []
    for char in name:
      if char.isnumeric():
        chars.append(char)
        continue
      if char.islower():
        chars.append(char)
      else:
        chars.append('_%s' % char.lower())
    name = ''.join(chars)
    while '__' in name:
      name = name.replace('__', '_')
    while name.startswith('_'):
      name = name[1:]
    return name

  @classmethod
  def _getKeyboardShortcuts(cls, key: str = None) -> ShortCut:
    """
    Returns a dictionary of common keyboard shortcuts
    categorized by Files, Edit, View, and Help actions.
    """
    if key is None:
      return {
        'new'      : 'CTRL+N',
        'open'     : 'CTRL+O',
        'save'     : 'CTRL+S',
        'saveAs'   : 'CTRL+SHIFT+S',
        'close'    : 'CTRL+W',
        'undo'     : 'CTRL+Z',
        'redo'     : 'CTRL+Y',
        'cut'      : 'CTRL+X',
        'copy'     : 'CTRL+C',
        'paste'    : 'CTRL+V',
        'selectAll': 'CTRL+A',
        'aboutQt'  : 'F12',
        'exit'     : 'ALT+F4',
        'help'     : 'F1',
        '__empty__': '',
      }
    if isinstance(key, str):
      shortcuts = cls._getKeyboardShortcuts()
      if key in shortcuts:
        return shortcuts[key]
      e = """No shortcut defined at name: '%s'""" % key
      raise ValueError(monoSpace(e))
    e = typeMsg('key', key, str)
    raise TypeError(e)

  @classmethod
  def _getIconPath(cls, ) -> str:
    """Getter-function for the path to the icon."""
    here = os.path.dirname(os.path.abspath(__file__))
    there = os.path.join(here, 'iconfiles')
    return os.path.normpath(there)

  @classmethod
  def _getIcons(cls, key: str = None) -> StrDict:
    """Getter-function for the icon path files. If not key is provided,
    the entire dictionary is returned. Otherwise, the value matching the
    key is returned. If a given key is not recognized, it will raise a
    KeyError. """
    if key is None:
      iconPath = cls._getIconPath()
      icons = {}
      for icon in os.listdir(iconPath):
        if icon.endswith('.png'):
          name = icon.split('.')[0]
          path = os.path.join(iconPath, icon)
          icons[name] = path
      return icons
    if isinstance(key, str):
      icons = cls._getIcons()
      if key in icons:
        return icons[key]
      e = """No icon defined at name: '%s'""" % key
      raise ValueError(monoSpace(e))
    e = typeMsg('key', key, str)
    raise TypeError(e)

  @classmethod
  def __class_getitem__(cls, key: str) -> Any:
    """Get the value of the key."""
    return cls().value(key)

  def getMissingAttributes(self) -> List[Dict[str, Any]]:
    """Getter-function for list of missing attributes"""
    return self._getMissing()

  def _getMissing(self, name: str = None, fallback: Any = None) -> ANY:
    """Getter-function for list of missing attributes"""
    if name is None:
      if self.__missing_attributes__ is None:
        self.__missing_attributes__ = []
      return self.__missing_attributes__
    if isinstance(name, str):
      entry = dict(name=name, fallback=fallback)
      return self._getMissing().append(entry)
    e = typeMsg('name', name, str)
    raise TypeError(e)

  def _getGroupNames(self, name: str = None) -> StrList:
    """Getter-function for the group names."""
    if name is None:
      if self.__group_names__ is None:
        self.__group_names__ = []
      return self.__group_names__
    if isinstance(name, str):
      return self._getGroupNames().append(name)
    e = typeMsg('name', name, str)
    raise TypeError(e)

  def _getOpenGroups(self, name: str = None) -> StrList:
    """Getter-function for the open groups."""
    if name is None:
      if self.__open_groups__ is None:
        self.__open_groups__ = []
      return self.__open_groups__
    if isinstance(name, str):
      return self._getOpenGroups().append(name)
    e = typeMsg('name', name, str)
    raise TypeError(e)

  def _getGroupTypes(self, key: str = None, type_: type = None) -> Type:
    """Getter-function for the group types."""
    if key is None:
      if self.__group_types__ is None:
        self.__group_types__ = {}
      return self.__group_types__
    if type_ is None:
      if isinstance(key, str):
        groupTypes = self._getGroupTypes()
        if key in groupTypes:
          return groupTypes[key]
        return object
      e = typeMsg('key', key, str)
      raise TypeError(e)
    if not isinstance(key, str):
      e = typeMsg('key', key, str)
      raise TypeError(e)
    if not isinstance(type_, type):
      e = typeMsg('type_', type_, type)
      raise TypeError(e)
    self._getGroupTypes()[key] = type_

  def _getGroupFallbacks(self, key: str = None, fb: Any = None) -> ANY:
    """Getter-function for the fallbacks"""
    if key is None:
      if self.__group_fallbacks__ is None:
        self.__group_fallbacks__ = {}
      return self.__group_fallbacks__
    if fb is None:
      if isinstance(key, str):
        groupFallbacks = self._getGroupFallbacks()
        while key:
          if key in groupFallbacks:
            return groupFallbacks[key]
          key = self._popKey(key)
        e = """No group fallback defined at name: '%s'""" % key
        raise ValueError(monoSpace(e))
      e = typeMsg('key', key, str)
      raise TypeError(e)
    if not isinstance(key, str):
      e = typeMsg('key', key, str)
      raise TypeError(e)
    self._getGroupFallbacks()[key] = fb

  def beginGroup(self, *args, ) -> None:
    """Begin a new group."""
    prefix, type_ = [*args, None, None][:2]
    if prefix is None or type_ is None:
      e = None
      if not args:
        e = """When opening a group, a prefix and a type must be defined, 
        but none was provided!"""
      if prefix:
        e = """When opening a group, a type must be defined, but none was 
        provided for the following prefix: '%s'!""" % prefix
      raise ValueError(monoSpace(e))
    if not isinstance(prefix, str):
      e = typeMsg('prefix', prefix, str)
      raise TypeError(e)
    if not isinstance(type_, type):
      e = typeMsg('type_', type_, type)
      raise TypeError(e)
    self._getGroupNames(prefix)
    self._getOpenGroups(prefix)
    self._getGroupTypes(prefix, type_)
    super().beginGroup(prefix)

  def endGroup(self, *args) -> None:
    """End the current group."""
    name = self._getOpenGroups().pop()
    return super().endGroup()

  @staticmethod
  def _joinKey(*keys) -> str:
    """Join the keys into a single string."""
    return '/'.join([str(k) for k in keys])

  @classmethod
  def _popKey(cls, key: str) -> str:
    """Pop the last key from the key string."""
    if '/' in key:
      return cls._joinKey(*key.split('/')[:-1])
    return ''

  @classmethod
  def _parseKey(cls, key: Any) -> str:
    """Creates a string version of given key"""
    if isinstance(key, str):
      return key
    if isinstance(key, tuple):
      key = [*key, ]
    if isinstance(key, list):
      return cls._joinKey(*key)

  def value(self, *args) -> Any:
    """Getter-function for the value of a key."""
    key = self._parseKey(args[0])
    fb, type_ = [*args, None, None][1:3]
    if type_ is not None:
      return super().value(key, fb, type_)
    value = super().value(key, )
    if value is None and fb is None:
      return self._getGroupFallbacks(key)
    if value is None:
      self._getMissing(key, fb)
      return fb
    return value

  def setValue(self, key: str, value: Any) -> None:
    """Setter-function for the value of a key."""
    key = key.strip()
    snake = self.snakeCase(key)
    camel = self.camelCase(key)
    if key not in [snake, camel]:
      e = """The key must be either in snake or camel case, but received: 
      '%s' with snake and camel: '%s' and '%s' respectively!"""
      raise ValueError(monoSpace(e % (key, snake, camel)))
    super().setValue(snake, value)
    if key != snake:
      super().setValue(camel, value)
