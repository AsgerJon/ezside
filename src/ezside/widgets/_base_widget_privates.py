"""_BaseWidgetPrivates provides a base class for the BaseWidget class
that provides the private attributes and functionality."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget
from icecream import ic
from vistutils.fields import EmptyField
from vistutils.parse import maybe
from vistutils.text import monoSpace, stringList
from vistutils.waitaminute import typeMsg

from ezside.app import AppSettings
from ezside.widgets import _AttriWidget

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class _BaseWidgetPrivates(_AttriWidget):
  """_BaseWidgetPrivates provides a base class for the BaseWidget class
  that provides the private attributes and functionality."""

  __debug_flag__ = None

  __style_fields__ = None
  __style_states__ = None

  __static_styles__ = None
  __dynamic_styles__ = None
  __style_id__ = None
  __fallback_id__ = 'normal'

  styleId = EmptyField()

  @classmethod
  def addStyleId(cls, styleId: str) -> None:
    """Adds a styleId to the class."""
    settings = AppSettings()
    settingsKey = '%s/%s' % (cls.__name__, 'styleIds')
    existing = maybe(settings.value(settingsKey, ), [])
    if styleId not in existing:
      settings.setValue(settingsKey, [*existing, styleId])

  @styleId.GET
  def _getStyleId(self, **kwargs) -> str:
    """Getter-function for the styleId."""
    if self.__style_id__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._setStyleId(self.__fallback_id__)
      return self._getStyleId(_recursion=True)
    if isinstance(self.__style_id__, str):
      return self.__style_id__
    e = typeMsg('self.__style_id__', self.__style_id__, str)
    raise TypeError(monoSpace(e))

  @styleId.SET
  def _setStyleId(self, styleId: str) -> None:
    """Setter-function for the styleId."""
    if self.__style_id__ is not None:
      e = """The styleId has already been assigned!"""
      raise AttributeError(e)
    if isinstance(styleId, str):
      self.__style_id__ = styleId
      settings = AppSettings()
      settingsKey = '%s/%s' % (self.__class__.__name__, 'styleIds')
      existingStyleIds = maybe(settings.value(settingsKey, ), [])
      if styleId not in existingStyleIds:
        settings.setValue(settingsKey, [*existingStyleIds, styleId])
    else:
      e = typeMsg('styleId', styleId, str)
      raise TypeError(e)

  def __init__(self, *args, **kwargs) -> None:
    """Subclasses that wish to allow __init__ to set the value of the
    'styleId' and other subclass specific primitive attributes, must apply
    these before invoking the parent __init__ method. This is because
    the __init__ automatically triggers the rest of the 'init' methods.
    Please note that BaseWidget will look for keyword arguments to set the
    styleId, at the following names:
      - 'styleId'
      - 'style'
      - 'id'
    defaulting to 'base' if none are found. """
    for arg in args:
      if isinstance(arg, QWidget):
        QWidget.__init__(self, arg)
        break
    else:
      QWidget.__init__(self)
    styleIdKeys = stringList("""id, styleId, style""")
    for key in styleIdKeys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, str):
          self.styleId = val
          break
        e = typeMsg('val', val, str)
        raise TypeError(monoSpace(e))
    else:
      self.styleId = 'normal'

    settings = AppSettings()
    settingsKey = '%s/%s' % (self.__class__.__name__, 'styleIds')
    existing = settings.value(settingsKey, [], list)
    if self.__style_id__ not in existing:
      settings.setValue(settingsKey, [*existing, self.__style_id__])

  @classmethod
  @abstractmethod
  def registerFields(cls) -> dict[str, Any]:
    """Getter-function for the fields."""

  @classmethod
  @abstractmethod
  def registerStates(cls) -> list[str]:
    """Getter-function for the states."""

  @classmethod
  @abstractmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """Getter-function for the dynamic fields."""

  @classmethod
  def _getStyleIds(cls, ) -> list[str]:
    """Getter-function for the style ids."""
    settings = AppSettings()
    settingsKey = '%s/%s' % (cls.__name__, 'styleIds')
    if settings.value(settingsKey, None, list) is None:
      settings.setValue(settingsKey, ['normal', ])
    styleIds = settings.value(settingsKey, None, list)
    if isinstance(styleIds, list):
      for arg in styleIds:
        if not isinstance(arg, str):
          e = typeMsg('arg', arg, str)
          raise TypeError(monoSpace(e))
      return styleIds
    elif isinstance(styleIds, str):
      return [styleIds, ]
    e = typeMsg('styleIds', styleIds, list)
    raise TypeError(monoSpace(e))

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
    dynamicFields = self.registerFields()
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

  def _fuckQSettings(self) -> dict[str, type]:
    """CUNTCUNTCUNT"""
    return {k: type(v) for (k, v) in self.registerFields().items()}

  Weight, Cap = QFont.Weight, QFont.Capitalization

  def _getStyle(self, key: str) -> Any:
    """Returns the value for the current instance at the given key"""
    staticStyles = self._getStaticStyles()
    dynamicStyles = self._getDynamicStyles()
    styleKey = '%s/%s' % (self._getStylePrefix(), key)
    styleType = self._fuckQSettings()[key]
    settings = AppSettings()
    cunt = settings.value(styleKey, None, styleType)
    if cunt is not None and not isinstance(cunt, styleType):
      try:
        return object.__call__(styleType, cunt)
      except Exception as exception:
        raise SystemExit from exception
    if cunt is not None:
      if not isinstance(cunt, styleType):
        msg = """At key: '%s', received '%s' of type '%s', but expected type 
        '%s'""" % (key, cunt, type(cunt).__name__, styleType.__name__)
        raise SystemExit(monoSpace(msg))
    if settings.value(styleKey, None, styleType) is not None:
      return settings.value(styleKey)

    if styleKey in dynamicStyles:
      style = dynamicStyles[styleKey]
      settings.setValue(styleKey, style)
      return style
    if styleKey in staticStyles:
      style = staticStyles[styleKey]
      settings.setValue(styleKey, style)
      return style
    e = """Received field name '%s' yielding style-key: '%s', but no such
    has been registered: \n%s."""
    names = '\n  '.join([name for name in staticStyles.keys()])
    print(styleKey)
    for key, val in dynamicStyles.items():
      print(key, val)
    for key, val in staticStyles.items():
      print(key, val)
    raise KeyError(monoSpace(e % (key, styleKey, names)))
