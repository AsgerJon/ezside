"""_BaseWidgetPrivates provides a base class for the BaseWidget class
that provides the private attributes and functionality."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from enum import EnumType
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QWidget
from icecream import ic
from vistutils.text import monoSpace, stringList
from vistutils.waitaminute import typeMsg

from ezside.core import resolveEnum
from morevistutils import hasAbstractMethod

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class _BaseWidgetPrivates(QWidget):
  """_BaseWidgetPrivates provides a base class for the BaseWidget class
  that provides the private attributes and functionality."""

  __debug_flag__ = None

  __style_fields__ = None
  __style_states__ = None

  __static_styles__ = None
  __dynamic_styles__ = None
  __style_id__ = None
  __fallback_id__ = 'normal'
  __fallback_styles__ = None
  __style_types__ = None
  __sub_classes__ = None

  def __new__(cls, *args, **kwargs) -> Any:
    """The __new__ method is used to create the instance of the class."""
    self = super().__new__(cls)
    self.__style_id__ = self._parseStyleId(**kwargs)
    self._registerStyleId(self.__style_id__)
    return self

  def __init__(self, *args, **kwargs) -> None:
    """Subclasses that wish to allow __init__ to set the value of the
    'styleId' and other subclass specific primitive attributes, must apply
    these before invoking the parent __init__ method. This is because
    the __init__ automatically triggers the rest of the 'init' methods.
    Please note that BaseWidget will look for keyword arguments to set the
    styleId, at the following names:
      - 'styleId'
      - 'style'
      - 'id'"""
    for arg in args:
      if isinstance(arg, QWidget):
        QWidget.__init__(self, arg)
        break
    else:
      QWidget.__init__(self)
    if self.__class__.__fallback_styles__ is None:
      self.__class__.registerSettings()

  @classmethod
  def _getStyleIds(cls) -> list[str]:
    """Getter-function for the style ids."""
    app = QCoreApplication.instance()
    settings = getattr(app, 'getSettings', )()
    settingsKey = '%s/%s' % (cls.__name__, 'styleIds')
    styleIds = settings.value(settingsKey, None)
    if styleIds is None:
      settings.setValue(settingsKey, 'normal')
      return ['normal', ]
    if isinstance(styleIds, str):
      return styleIds.split(', ')
    e = typeMsg('styleIds', styleIds, str)
    raise TypeError(monoSpace(e))

  @classmethod
  def _registerStyleId(cls, styleId: str) -> None:
    """Registers a styleId."""
    app = QCoreApplication.instance()
    settings = getattr(app, 'getSettings', )()
    settingsKey = '%s/%s' % (cls.__name__, 'styleIds')
    existing = settings.value(settingsKey, None)
    if existing is None:
      settings.setValue(settingsKey, styleId)
    if isinstance(existing, str):
      if styleId in existing:
        return
      existing = '%s, %s' % (existing, styleId)
      if styleId not in existing:
        settings.setValue(settingsKey, '%s, %s' % (existing, styleId))

  def _parseStyleId(self, **kwargs) -> str:
    """Parses the styleId."""
    styleIdKeys = stringList("""id, styleId, style""")
    for key in styleIdKeys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, str):
          return val
        e = typeMsg('val', val, str)
        raise TypeError(monoSpace(e))
    else:
      return self.__fallback_id__

  @classmethod
  @abstractmethod
  def registerStates(cls) -> list[str]:
    """Getter-function for the states."""

  @classmethod
  @abstractmethod
  def registerFields(cls) -> dict[str, Any]:
    """Getter-function for the fields."""

  @classmethod
  @abstractmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """Subclasses may implement this method to define dynamic values at
    fields that depend on the current state and style id. """

  def _getStyleId(self) -> str:
    """Getter-function for the style id."""
    return self.__style_id__

  def _getStylePrefix(self, ) -> str:
    """Getter-function for the style prefix."""
    clsName = self.__class__.__name__
    styleId = self._getStyleId()
    state = self.detectState()
    key = '%s/%s/%s' % (clsName, styleId, state)
    return key

  def _createStaticStyles(self) -> None:
    """Creates the static styles."""
    fields = self.registerFields()
    styleIds = self._getStyleIds()
    states = self.registerStates()
    self.__static_styles__ = {}
    clsName = self.__class__.__name__
    for Id in styleIds:
      for state in states:
        for (name, value) in fields.items():
          key = '%s/%s/%s/%s' % (clsName, Id, state, name)
          self.__static_styles__[key] = value

  def _getStaticStyles(self, **kwargs) -> dict[str, Any]:
    """Getter-function for the static styles."""
    if self.__static_styles__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createStaticStyles()
      return self._getStaticStyles(_recursion=True)
    if isinstance(self.__static_styles__, dict):
      return self.__static_styles__
    e = typeMsg('self.__static_styles__', self.__static_styles__, dict)
    raise TypeError(monoSpace(e))

  def _createDynamicStyles(self) -> None:
    """Creates the dynamic styles."""
    dynamicFields = self.registerDynamicFields()
    styleIds = self._getStyleIds()
    states = self.registerStates()
    self.__dynamic_styles__ = {}
    for (key, value) in dynamicFields.items():
      for styleId in styleIds:
        for state in states:
          key = key.replace('__all_styleIds__', styleId)
          key = key.replace('__all_states__', state)
          if key in self.__dynamic_styles__:
            continue
          self.__dynamic_styles__[key] = value

  def _getDynamicStyles(self, **kwargs) -> dict[str, Any]:
    """Getter-function for the dynamic styles."""
    if self.__dynamic_styles__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createDynamicStyles()
      return self._getDynamicStyles(_recursion=True)
    if isinstance(self.__dynamic_styles__, dict):
      return self.__dynamic_styles__
    e = typeMsg('self.__dynamic_styles__', self.__dynamic_styles__, dict)
    raise TypeError(monoSpace(e))

  @abstractmethod
  def detectState(self, ) -> str:
    """Getter-function for the state."""

  @classmethod
  def updateSettings(cls, **kwargs) -> None:
    """The updateSettings method is called to update the settings."""
    subClasses = getattr(cls, '__sub_classes__', [])
    if subClasses is None:
      raise AttributeError
    for subClass in subClasses:
      if not hasAbstractMethod(subClass):
        subClass.registerSettings(**kwargs)

  @classmethod
  def registerSettings(cls, **kwargs) -> None:
    """The init subclass places the registered values into the settings
    object. """
    if hasAbstractMethod(cls):
      return
    clsName = cls.__name__
    styleIds = cls._getStyleIds() or ['normal', ]
    states = cls.registerStates() or ['base', ]
    fields = cls.registerFields() or {}
    dynamicFields = cls.registerDynamicFields() or {}
    app = QCoreApplication.instance()
    settings = getattr(app, 'getSettings', )()
    cls.__fallback_styles__ = {}
    cls.__style_types__ = {}
    for Id in styleIds:
      for state in states:
        for (name, value) in fields.items():
          key = '%s/%s/%s/%s' % (clsName, Id, state, name)
          cls.__fallback_styles__[key] = value
          cls.__style_types__[key] = type(value)
          settingsValue = settings.value(key, None)
          if settingsValue is None:
            settings.setValue(key, value)

  def _getSettingsNamedStyle(self, name: str) -> Any:
    """Gets the value in the settings for the given name"""
    key = '%s/%s' % (self._getStylePrefix(), name)
    app = QCoreApplication.instance()
    settings = getattr(app, 'getSettings', )()
    return settings.value(key, None)

  def _getBaseValue(self, name: str) -> Any:
    """Gets the value in the settings for the given name"""
    baseValue = self.registerFields().get(name, None)
    if baseValue is None:
      e = """The name: '%s' is not recognizes as the name of a style
      in the registerFields method on class: '%s'!""" % (
        name, self.__class__)
      raise KeyError(monoSpace(e))
    return baseValue

  def _getExpectedType(self, name: str) -> Any:
    """Getter-function for the expected type."""
    return type(self._getBaseValue(name))

  def _getNamedStyle(self, name: str) -> Any:
    """Getter-function for the named style."""
    key = '%s/%s' % (self._getStylePrefix(), name)
    expectedType = self._getExpectedType(name)
    baseValue = self._getBaseValue(name)
    fallbackValue = self.__fallback_styles__.get(key, None)
    settingsValue = self._getSettingsNamedStyle(name)
    value = fallbackValue if settingsValue is None else settingsValue

    if isinstance(value, expectedType):
      return value
    if isinstance(value, str):
      if isinstance(expectedType, EnumType):
        return resolveEnum(expectedType, value)

  def __init_subclass__(cls, **kwargs) -> None:
    """The __init_subclass__ method is called when a subclass is created."""
    existing = getattr(cls.__bases__[0], '__sub_classes__', []) or []
    setattr(cls, '__sub_classes__', [*existing, cls])
    super().__init_subclass__(**kwargs)
