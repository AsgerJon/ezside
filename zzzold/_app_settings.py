"""AppSettings provides a subclass of QSettings that raises errors when
receiving unknown keys. The class implements the descriptor protocol and
should be accessed through the descriptor instance."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import Any, TYPE_CHECKING, Callable

from PySide6.QtCore import QSettings, QObject, QRect
from PySide6.QtGui import QIcon, QKeySequence
from attribox import AbstractDescriptor
from icecream import ic
from vistutils.waitaminute import typeMsg

from ezside.app import MissingSettingsError, CastingException

Shiboken = type(QObject)

if TYPE_CHECKING:
  from ezside.app import EZObject

ic.configureOutput(includeContext=True)


class _InnerSettings(QSettings):
  """AppSettings subclasses the QSettings class."""

  __expected_types__ = None
  __factory_functions__ = None

  @classmethod
  def _getTypeKey(cls, castType: type) -> str:
    """Returns the key that points to the given type"""
    for (key, val) in cls._getExpectedTypeDictionary().items():
      if castType is val:
        return key
    else:
      clsName = castType.__name__
      e = """Unable to resolve key pointing to: '%s'""" % clsName
      raise KeyError(e)

  @classmethod
  def _autoCast(cls, stringValue: str, castType: type) -> Any:
    """Automatically casts a string to a type. """
    castKey = cls._getTypeKey(castType)
    factory = cls._getFactoryFunction(castKey)
    try:
      return castType(stringValue)
    except Exception as exception:
      raise CastingException(exception, castType, stringValue, )

  @classmethod
  def _factory(cls, stringValue: str, castType: type) -> Any:
    """Rather than casting the string by just calling the expected type on
    the string. Alternatively, this method """

  @classmethod
  def _getFactoryFunctionDictionary(cls, **kwargs) -> dict[str, type]:
    """Returns the factory functions for each key. """
    if cls.__factory_functions__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls.__factory_functions__ = {}
      return cls._getFactoryFunctionDictionary(_recursion=True)
    if isinstance(cls.__factory_functions__, dict):
      for (key, val) in cls.__factory_functions__.items():
        if not callable(val):
          e = typeMsg('val', val, Callable)
          raise TypeError(e)
      return cls.__factory_functions__
    e = typeMsg('__factory_functions__', cls.__factory_functions__, dict)
    raise TypeError(e)

  @classmethod
  def _getExpectedTypeDictionary(cls, **kwargs) -> dict[str, type]:
    """Returns the expected types for each key. """
    if cls.__expected_types__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls.__expected_types__ = {}
      return cls._getExpectedTypeDictionary(_recursion=True)
    if isinstance(cls.__expected_types__, dict):
      for (key, val) in cls.__expected_types__.items():
        if not isinstance(val, type):
          raise TypeError
      return cls.__expected_types__
    e = typeMsg('__expected_types__', cls.__expected_types__, dict)
    raise TypeError(e)

  @classmethod
  def _getFactoryFunction(cls, key: str) -> Callable:
    """Returns the factory function for a key. """
    factoryDict = cls._getFactoryFunctionDictionary()
    if key not in factoryDict:
      e = """The key '%s' does not have a factory function. """ % (key,)
      raise KeyError(e)
    callMeMaybe = factoryDict.get(key, None)
    if callable(callMeMaybe):
      return callMeMaybe
    e = typeMsg('callMeMaybe', callMeMaybe, Callable)
    raise TypeError(e)

  @classmethod
  def _setFactoryFunction(cls, key: str, function: Callable) -> None:
    """Sets the factory function for a key. """
    factoryDict = cls._getFactoryFunctionDictionary()
    if key in factoryDict:
      e = """The key '%s' already has a factory function. """ % (key,)
      raise KeyError(e)
    if callable(function):
      return factoryDict.update({key: function})
    e = typeMsg('function', function, Callable)
    raise TypeError(e)

  @classmethod
  def setExpectedType(cls, key: str, type_: type) -> None:
    """Sets the expected type for a key. """
    expTypeDict = cls._getExpectedTypeDictionary()
    if isinstance(type_, type):
      return expTypeDict.update({key: type_})
    e = typeMsg('type_', type_, type)
    raise TypeError(e)

  @classmethod
  def _getExpectedType(cls, key: str) -> type:
    """Returns the expected type for a key. """
    expTypeDict = cls._getExpectedTypeDictionary()
    if key not in expTypeDict:
      e = """The key '%s' does not have an expected type. """ % (key,)
      raise KeyError(e)
    type_ = expTypeDict[key]
    if isinstance(type_, type):
      return type_
    e = typeMsg('type_', type_, type)
    raise TypeError(e)

  def __init__(self, *args, **kwargs) -> None:
    format_ = QSettings.Format.IniFormat
    scope = QSettings.Scope.UserScope
    parent, orgName, appName = None, None, None
    for arg in args:
      if isinstance(arg, str):
        if orgName is None:
          orgName = arg
        else:
          appName = arg
      elif isinstance(arg, QObject):
        parent = arg
    QSettings.__init__(self, format_, scope, orgName, appName, parent)

  def value(self, key: str, fb: Any = None, type_: type = None) -> Any:
    """The value method is overridden to raise an error when the key is not
    recognized. """
    baseValue = QSettings.value(self, key, None, )
    if baseValue is None:
      raise MissingSettingsError(key)
    expectedType = self._getExpectedType(key)
    if not isinstance(expectedType, type):
      e = typeMsg('expectedType', expectedType, type)
      raise TypeError(e)
    if isinstance(baseValue, expectedType):
      return baseValue
    if isinstance(baseValue, str):
      castedValue = self._autoCast(baseValue, expectedType)
      if isinstance(castedValue, expectedType):
        return castedValue
      e = typeMsg('castedValue', castedValue, expectedType)
      raise TypeError(e)
    e = typeMsg('baseValue', baseValue, expectedType)
    raise TypeError(e)

  def setValue(self, key: str, value: Any, **kwargs) -> None:
    """The setValue method is overridden to raise an error when the key is
    not recognized. """
    self.setExpectedType(key, type(value))
    QSettings.setValue(self, key, value)


class Settings(AbstractDescriptor):
  """lmao"""

  __pos_args__ = None
  __key_args__ = None

  @staticmethod
  def snakeToCamel(snakeCase: str) -> str:
    """Converts a snake_case string to a CamelCase string."""
    parts = snakeCase.split('_')
    if len(parts) == 1:
      return parts.pop()
    name = parts.pop(0)
    cunt = ''.join([part.capitalize() for part in parts])
    return '%s%s' % (name, cunt)

  @classmethod
  def loadIcons(cls, settingsObject: _InnerSettings = None) -> None:
    """Load the settings """
    here = os.path.dirname(os.path.abspath(__file__))
    iconPath = os.path.join(here, 'iconfiles')
    for item in os.listdir(iconPath):
      if item.endswith('.png'):
        name = item.replace('.png', '')
        icon = QIcon(os.path.join(iconPath, item))
        key = 'icon/%s' % cls.snakeToCamel(name)
        if settingsObject is not None:
          settingsObject.setExpectedType(key, QIcon)
        settingsObject.setValue(key, icon)
    for i in range(10):
      key = 'icon/debug%d' % i
      value = QIcon(os.path.join(iconPath, 'risitas.png'))
      settingsObject.setValue(key, value)

  @staticmethod
  def loadShortcuts(settingsObject: _InnerSettings = None) -> None:
    """Load the settings """
    mapCuts = {
      'new'         : 'CTRL+N',
      'open'        : 'CTRL+O',
      'save'        : 'CTRL+S',
      'saveAs'      : 'CTRL+SHIFT+S',
      'close'       : 'CTRL+W',
      'undo'        : 'CTRL+Z',
      'redo'        : 'CTRL+Y',
      'cut'         : 'CTRL+X',
      'copy'        : 'CTRL+C',
      'paste'       : 'CTRL+V',
      'selectAll'   : 'CTRL+A',
      'aboutQt'     : 'F12',
      'exit'        : 'ALT+F4',
      'debug1'      : 'F1',
      'debug2'      : 'F2',
      'debug3'      : 'F3',
      'debug4'      : 'F4',
      'debug5'      : 'F5',
      'debug6'      : 'F6',
      'debug7'      : 'F7',
      'debug8'      : 'F8',
      'debug9'      : 'F9',
      '__empty__'   : '',
      'preferences' : '',
      'aboutPySide6': '',
      'aboutPython' : '',
      'aboutConda'  : '',
      'help'        : ''
    }
    for (name, keys) in mapCuts.items():
      key = 'shortcut/%s' % name
      combo = QKeySequence.fromString(keys)
      if settingsObject is not None:
        settingsObject.setExpectedType(key, QKeySequence)
      settingsObject.setValue(key, combo)

  @staticmethod
  def loadGeometry(settingsObject: _InnerSettings = None) -> None:
    """Load the settings """
    mapVals = {'window/geometry': QRect(100, 100, 800, 600)}
    for (key, value) in mapVals.items():
      if settingsObject is not None:
        settingsObject.setExpectedType(key, type(value))
      settingsObject.setValue(key, value)

  def _loadSettings(self, settingsObject: _InnerSettings = None) -> None:
    """Load the settings """
    self.loadIcons(settingsObject)
    self.loadShortcuts(settingsObject)
    self.loadGeometry(settingsObject)

  def _createInstance(self) -> _InnerSettings:
    """Create the main window instance."""
    settingsObject = _InnerSettings()
    self._loadSettings(settingsObject)
    return settingsObject

  def __init__(self, *args, **kwargs) -> None:
    self.__pos_args__ = args
    self.__key_args__ = kwargs

  def __instance_get__(self, instance: EZObject, owner: Shiboken) -> Any:
    """The getter function instantiates the settings class."""
    if instance is None:
      return self
    settingsObject = self._createInstance()
    self._loadSettings(settingsObject)
    return settingsObject
