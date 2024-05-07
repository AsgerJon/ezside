"""BaseWidget provides a common base class for all widgets in the
application."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from PySide6.QtWidgets import QWidget
from vistutils.text import monoSpace

from ezside.app import AppSettings
from ezside.widgets import _AttriWidget

if TYPE_CHECKING:
  pass


class BaseWidget(_AttriWidget):
  """BaseWidget provides a common base class for all widgets in the
  application."""

  __style_map__ = None
  __style_fields__ = None
  __style_fallbacks__ = None
  __field_names__ = None
  __style_ids__ = None
  __style_states__ = None
  __pos_args__ = None
  __key_args__ = None

  def __class_getitem__(cls, *args, **kwargs) -> Callable:
    """This method is used to provide a shorthand for the styleKey
    getter-function. The method is expected to be called with a string
    argument, which is the name of the field. """

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
    self.__style_id__ = kwargs.get('id', 'normal')

  def initUi(self, ) -> None:
    """Initializes the user interface for the widget. If subclasses have
    nested widgets or layouts, this method should be implemented to
    organize the widgets and layouts. Widget classes without layouts or
    nested widgets and which instead implement a custom paintEvent for
    example, need not implement this method. """

  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the widget. Subclasses
    with nested widgets and internal signal and slot logic, should
    implement this method to organize these. This method is invoked only
    after initUi, so the reimplementation may rely on widgets instantiated
    during initUi to be available. """

  def getState(self, ) -> str:
    """Getter-function for the current state of the widget. Subclasses
    may implement this method to provide the widget with state awareness."""

  def _getStyleId(self) -> str:
    """Getter-function for the style id."""
    return self.__style_id__

  @classmethod
  def registerStyleIds(cls) -> list[str]:
    """This method is expected to provide the different styleIds supported
    by the widget subclass. It is required for styleId aware widgets. If
    not implemented, the implied styleId 'base' will be used. Please note
    that subclasses must use the 'styleId' property to enable styleIds."""

  @classmethod
  def registerStates(cls) -> list[str]:
    """This method is expected to provide the different states supported by
    the widget subclass. If not implemented, the implied state 'normal' will
    be used. If implemented, the getStates method should also be implemented
    to provide the widget with state awareness. If not, the parent method
    will simply keep the state 'normal' regardless. """

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
    """Subclasses may implement this method to yield control of values to
    the app-wide setting system. This method is expected to return a
    mapping from field name to fallback value. Please note, that the
    expected type of the field is inferred from the fallback value.

    For example, a widget with a default font size of 16, may return:
    {
      'fontSize': 16,
    }

    Please note that group identity is not allowed here and will lead to
    undefined behaviour. If the font size is sensitive to state, styleId
    or even both, this field key remains the same.

    For example, the style-key presented to app wide settings might be:
    key = ExampleWidget/baseId/normalState/fontSize
    value = 12
    and then for the header id:
    key = ExampleWidget/headerId/normalState/fontSize
    value = 16"""

  @classmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """Subclasses may implement this method to implement centrally
    controlled dynamic fields. By default, the same fallback value is used
    for all states and styleIds. This method is responsible for setting
    alternative values for a given styleId and state in a dictionary whose
    entries override those in the fallback dictionary.

    For example, a widget wishing to indicate that the cursor is currently
    hovering on it, must have registered this state, for example under the
    name 'hover'. The method should return a mapping from field name to
    hover value. Only values defined here will be sensitive to the hover
    state.

    {
      'header': {
        '__all_states__': {
          'fontSize': 16,
          'fontWeight': Bold,
        }
      },
      'link': {
        'normal': {
          fontSize: 12,
          fontWeight: Normal,
        },
        'hover': {
          fontSize: 12,  # Redundant as no change applies
          fontWeight: Bold,
        }
      },
    }

    The styleKey-value pairs for the above example would then include:
    Label/header/normal/fontSize: 16
    Label/link/normal/fontSize: 12
    Label/link/normal/fontWeight: Normal
    Label/link/hover/fontSize: 12
    Label/link/hover/fontWeight: Bold
    Even though redundant to specify, the system will still register a value
    at both Label/link/hover/fontSize and Label/link/normal/fontSize. Please
    note that since the header is not intended to be sensitive to states,
    it may use the special name '__all_states__'. Similarly, if a widget
    is to be only state aware but not styleId aware, it may use the special
    name '__all_styleIds__'.
    """

  @classmethod
  def _applyFields(cls, ) -> None:
    """Applies the fields to the widget. Subclasses are not permitted to
    reimplement. This prohibition will be enforced in a future update."""
    fields = cls.registerFields()
    styleIds = cls.registerStyleIds() or ['normal']
    states = cls.registerStates() or ['base']
    dynamicFields = cls.registerDynamicFields() or {}
    styleMap = {}
    for Id in styleIds:
      for state in states:
        for (name, value) in fields.items():
          key = '%s/%s/%s/%s' % (cls.__name__, Id, state, name)
          styleMap[key] = value
    if '__all_styleIds__' in dynamicFields:
      allStyles = dynamicFields['__all_styleIds__']
      dynamicFields = {Id: allStyles for Id in styleIds}
    for (Id, stateMap) in dynamicFields.items():
      if '__all_states__' in stateMap:
        allStates = stateMap['__all_states__']
        stateMap = {state: allStates for state in states}
      for (state, fieldMap) in stateMap.items():
        for (name, value) in fieldMap.items():
          styleMap['%s/%s/%s/%s' % (cls.__name__, Id, state, name)] = value
    cls.__style_map__ = styleMap
    cls.__style_fields__ = fields
    cls.__style_ids__ = styleIds
    cls.__style_states__ = states
    cls.__field_names__ = [*fields.keys(), ]

  def _getStyleMap(self) -> dict[str, Any]:
    """Getter-function for the style map."""
    if self.__style_map__ is None:
      self._applyFields()
    return self.__style_map__

  def _getStyleFields(self) -> dict[str, Any]:
    """Getter-function for the style fields."""
    if self.__style_fields__ is None:
      self._applyFields()
    return self.__style_fields__

  def _getStyleIds(self) -> list[str]:
    """Getter-function for the style ids."""
    if self.__style_ids__ is None:
      self._applyFields()
    return self.__style_ids__

  def _getStyleStates(self) -> list[str]:
    """Getter-function for the style states."""
    if self.__style_states__ is None:
      self._applyFields()
    return self.__style_states__

  def _getFieldNames(self, ) -> list[str]:
    """Getter-function for the field name."""
    if self.__field_names__ is None:
      self._applyFields()
    return self.__field_names__

  def _getStylePrefix(self, ) -> str:
    """Getter-function for the style prefix."""
    clsName = self.__class__.__name__
    Id = self._getStyleId()
    state = self.getState() or 'base'
    return '%s/%s/%s' % (clsName, Id, state)

  def _getFieldValue(self, name: str) -> Any:
    """Getter-function for the field value."""
    styleKey = '%s/%s' % (self._getStylePrefix(), name)
    styleMap = self._getStyleMap()
    if styleKey in styleMap:
      fb = styleMap[styleKey]
    else:
      e = """Received field name '%s' yielding style-key: '%s', but no such
      has been registered: \n%s."""
      names = '\n  '.join([name for name in styleMap.keys()])
      raise KeyError(monoSpace(e % (name, styleKey, names)))
    return AppSettings().value(styleKey, fb)
