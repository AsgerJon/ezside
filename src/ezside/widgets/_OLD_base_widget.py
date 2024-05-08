#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
#
# from typing import TYPE_CHECKING, Callable, Any
#
# from PySide6.QtGui import QPaintEvent, QPainter, QColor, QPen
# from PySide6.QtWidgets import QWidget
# from icecream import ic
# from vistutils.parse import maybe
# from vistutils.text import monoSpace, stringList
# from vistutils.waitaminute import typeMsg
#
# from ezside.app import AppSettings
# from ezside.core import SolidLine, emptyBrush
# from ezside.widgets import _AttriWidget
#
# if TYPE_CHECKING:
#   pass
#
# ic.configureOutput(includeContext=True)
#
#
# class BaseWidget(_AttriWidget):
#   """BaseWidget provides a common base class for all widgets in the
#   application."""
#
#   __debug_flag__ = None
#
#   __static_styles__ = None
#   __dynamic_styles__ = None
#
#   __style_map__ = None
#   __style_fields__ = None
#   __style_fallbacks__ = None
#   __field_names__ = None
#   __style_id__ = None
#   __style_ids__ = None
#   __style_states__ = None
#   __pos_args__ = None
#   __key_args__ = None
#
#   def __class_getitem__(cls, *args, **kwargs) -> Callable:
#     """This method is used to provide a shorthand for the styleKey
#     getter-function. The method is expected to be called with a string
#     argument, which is the name of the field. """
#
#   def __init__(self, *args, **kwargs) -> None:
#     """Subclasses that wish to allow __init__ to set the value of the
#     'styleId' and other subclass specific primitive attributes, must apply
#     these before invoking the parent __init__ method. This is because
#     the __init__ automatically triggers the rest of the 'init' methods.
#     Please note that BaseWidget will look for keyword arguments to set the
#     styleId, at the following names:
#       - 'styleId'
#       - 'style'
#       - 'id'
#     defaulting to 'base' if none are found. """
#     for arg in args:
#       if isinstance(arg, QWidget):
#         QWidget.__init__(self, arg)
#         break
#     else:
#       QWidget.__init__(self)
#     styleIdKeys = stringList("""id, styleId, style""")
#     for key in styleIdKeys:
#       if key in kwargs:
#         val = kwargs[key]
#         if isinstance(val, str):
#           self.__style_id__ = val
#           break
#         e = typeMsg('val', val, str)
#         raise TypeError(monoSpace(e))
#     else:
#       self.__style_id__ = 'normal'
#     self._applyFields()
#
#   def initUi(self, ) -> None:
#     """Initializes the user interface for the widget. If subclasses have
#     nested widgets or layouts, this method should be implemented to
#     organize the widgets and layouts. Widget classes without layouts or
#     nested widgets and which instead implement a custom paintEvent for
#     example, need not implement this method. """
#
#   def initSignalSlot(self) -> None:
#     """Initializes the signal/slot connections for the widget. Subclasses
#     with nested widgets and internal signal and slot logic, should
#     implement this method to organize these. This method is invoked only
#     after initUi, so the reimplementation may rely on widgets instantiated
#     during initUi to be available. """
#
#   def _getState(self) -> str:
#     """Getter-function for the current state of the widget. Subclasses
#     may implement this method to provide the widget with state
#     awareness."""
#     return maybe(self.getState(), 'base')
#
#   def getState(self, ) -> str:
#     """Getter-function for the current state of the widget. Subclasses
#     may implement this method to provide the widget with state
#     awareness."""
#
#   def _getStyleId(self) -> str:
#     """Getter-function for the style id."""
#     return self.__style_id__
#
#   @classmethod
#   def registerStyleIds(cls) -> list[str]:
#     """This method is expected to provide the different styleIds supported
#     by the widget subclass. It is required for styleId aware widgets. If
#     not implemented, the implied styleId 'base' will be used. Please note
#     that subclasses must use the 'styleId' property to enable styleIds."""
#
#   @classmethod
#   def registerStates(cls) -> list[str]:
#     """This method is expected to provide the different states supported by
#     the widget subclass. If not implemented, the implied state 'normal'
#     will
#     be used. If implemented, the getStates method should also be
#     implemented
#     to provide the widget with state awareness. If not, the parent method
#     will simply keep the state 'normal' regardless. """
#
#   @classmethod
#   def registerFields(cls) -> dict[str, Any]:
#     """Subclasses may implement this method to yield control of values to
#     the app-wide setting system. This method is expected to return a
#     mapping from field name to fallback value. Please note, that the
#     expected type of the field is inferred from the fallback value.
#
#     For example, a widget with a default font size of 16, may return:
#     {
#       'fontSize': 16,
#     }
#
#     Please note that group identity is not allowed here and will lead to
#     undefined behaviour. If the font size is sensitive to state, styleId
#     or even both, this field key remains the same.
#
#     For example, the style-key presented to app wide settings might be:
#     key = ExampleWidget/baseId/normalState/fontSize
#     value = 12
#     and then for the header id:
#     key = ExampleWidget/headerId/normalState/fontSize
#     value = 16"""
#
#   @classmethod
#   def registerDynamicFields(cls) -> dict[str, Any]:
#     """Subclasses may implement this method to implement centrally
#     controlled dynamic fields. By default, the same fallback value is used
#     for all states and styleIds. This method is responsible for setting
#     alternative values for a given styleId and state in a dictionary whose
#     entries override those in the fallback dictionary.
#
#     For example, a widget wishing to indicate that the cursor is currently
#     hovering on it, must have registered this state, for example under the
#     name 'hover'. The method should return a mapping from field name to
#     hover value. Only values defined here will be sensitive to the hover
#     state.
#
#     {
#       'header': {
#         '__all_states__': {
#           'fontSize': 16,
#           'fontWeight': Bold,
#         }
#       },
#       'link': {
#         'normal': {
#           fontSize: 12,
#           fontWeight: Normal,
#         },
#         'hover': {
#           fontSize: 12,  # Redundant as no change applies
#           fontWeight: Bold,
#         }
#       },
#     }
#
#     The implement ths above, this method should return a dictionary with
#     styleKey to value. For the above example, the class 'Label' provides
#     the following dynamic fields:
#
#     {
#       'Label/header/__all_states__/fontSize': 16,
#       'Label/header/__all_states__/fontWeight': Bold,
#       'Label/link/normal/fontSize': 12,
#       'Label/link/normal/fontWeight': Normal,
#       'Label/link/hover/fontSize': 12,
#       'Label/link/hover/fontWeight': Bold,
#     }
#
#     The styleKey-value pairs for the above example would then include:
#     Label/header/normal/fontSize: 16
#     Label/link/normal/fontSize: 12
#     Label/link/normal/fontWeight: Normal
#     Label/link/hover/fontSize: 12
#     Label/link/hover/fontWeight: Bold
#     Even though redundant to specify, the system will still register a
#     value
#     at both Label/link/hover/fontSize and Label/link/normal/fontSize.
#     Please
#     note that since the header is not intended to be sensitive to states,
#     it may use the special name '__all_states__'. Similarly, if a widget
#     is to be only state aware but not styleId aware, it may use the special
#     name '__all_styleIds__'.
#     """
#
#   def _createStaticStyles(self) -> None:
#     """Creates the static styles."""
#     fields = self.registerFields() or {}
#     styleIds = self.registerStyleIds() or ['normal']
#     states = self.registerStates() or ['base']
#     self.__static_styles__ = {}
#     for Id in styleIds:
#       for state in states:
#         for (name, value) in fields.items():
#           key = '%s/%s/%s/%s' % (self.__name__, Id, state, name)
#           self.__static_styles__[key] = value
#
#   def _getStaticStyles(self, **kwargs) -> dict[str, Any]:
#     """Getter-function for the static styles."""
#     if self.__static_styles__ is None:
#       if kwargs.get('_recursion', False):
#         raise RecursionError
#       self._createStaticStyles()
#       return self._getStaticStyles(_recursion=True)
#     if isinstance(self.__static_styles__, dict):
#       return self.__static_styles__
#     e = typeMsg('self.__static_styles__', self.__static_styles__, dict)
#     raise TypeError(monoSpace(e))
#
#   def _createDynamicStyles(self) -> None:
#     """Creates the dynamic styles."""
#     dynamicFields = self.registerDynamicFields() or {}
#     styleIds = self.registerStyleIds() or ['normal']
#     states = self.registerStates() or ['base']
#     self.__dynamic_styles__ = {}
#     for (key, value) in dynamicFields.items():
#       for styleId in styleIds:
#         for state in states:
#           key = key.replace('__all_styleIds__', styleId)
#           key = key.replace('__all_states__', state)
#           if key in self.__dynamic_styles__:
#             continue
#           self.__dynamic_styles__[key] = value
#
#   def _getDynamicStyles(self, **kwargs) -> dict[str, Any]:
#     """Getter-function for the dynamic styles."""
#     if self.__dynamic_styles__ is None:
#       if kwargs.get('_recursion', False):
#         raise RecursionError
#       self._createDynamicStyles()
#       return self._getDynamicStyles(_recursion=True)
#     if isinstance(self.__dynamic_styles__, dict):
#       return self.__dynamic_styles__
#     e = typeMsg('self.__dynamic_styles__', self.__dynamic_styles__, dict)
#     raise TypeError(monoSpace(e))
#
#   def getStyleValue(self, key: str) -> Any:
#     """Returns the value for the current instance at the given key"""
#     clsName = self.__class__.__name__
#     styleId = self._getStyleId()
#     state = self._getState() or 'base'
#     styleKey = '%s/%s/%s/%s' % (clsName, styleId, state, key)
#     staticStyles = self._getStaticStyles()
#     dynamicStyles = self._getDynamicStyles()
#     if styleKey in dynamicStyles:
#       return dynamicStyles[styleKey]
#     if styleKey in staticStyles:
#       return staticStyles[styleKey]
#     e = """Received field name '%s' yielding style-key: '%s', but no such
#     has been registered: \n%s."""
#     names = '\n  '.join([name for name in staticStyles.keys()])
#     raise KeyError(monoSpace(e % (key, styleKey, names)))
#
#   @classmethod
#   def _applyFields(cls, ) -> None:
#     """Applies the fields to the widget. Subclasses are not permitted to
#     reimplement. This prohibition will be enforced in a future update."""
#     fields = cls.registerFields() or {}
#     styleIds = cls.registerStyleIds() or ['normal']
#     states = cls.registerStates() or ['base']
#     dynamicFields = cls.registerDynamicFields() or {}
#     styleMap = {}
#     for Id in styleIds:
#       for state in states:
#         for (name, value) in fields.items():
#           key = '%s/%s/%s/%s' % (cls.__name__, Id, state, name)
#           styleMap[key] = value
#     for (key, value) in dynamicFields.items():
#       for styleId in styleIds:
#         for state in states:
#           key = key.replace('__all_styleIds__', styleId)
#           key = key.replace('__all_states__', state)
#           if key in styleMap:
#             continue
#           styleMap[key] = value
#     cls.__style_map__ = styleMap
#     cls.__style_fields__ = fields
#     cls.__style_ids__ = styleIds
#     cls.__style_states__ = states
#     cls.__field_names__ = [*fields.keys(), ]
#
#   def _getStyleMap(self) -> dict[str, Any]:
#     """Getter-function for the style map."""
#     if self.__style_map__ is None:
#       self._applyFields()
#     return self.__style_map__
#
#   def _getStyleFields(self) -> dict[str, Any]:
#     """Getter-function for the style fields."""
#     if self.__style_fields__ is None:
#       self._applyFields()
#     return self.__style_fields__
#
#   def _getStyleIds(self) -> list[str]:
#     """Getter-function for the style ids."""
#     if self.__style_ids__ is None:
#       self._applyFields()
#     return self.__style_ids__
#
#   def _getStyleStates(self) -> list[str]:
#     """Getter-function for the style states."""
#     if self.__style_states__ is None:
#       self._applyFields()
#     return self.__style_states__
#
#   def _getFieldNames(self, ) -> list[str]:
#     """Getter-function for the field name."""
#     if self.__field_names__ is None:
#       self._applyFields()
#     return self.__field_names__
#
#   def _getStylePrefix(self, ) -> str:
#     """Getter-function for the style prefix."""
#     clsName = self.__class__.__name__
#     styleId = self._getStyleId()
#     state = self._getState() or 'base'
#     key = '%s/%s/%s' % (clsName, styleId, state)
#     return key
#
#   def _getFieldValue(self, name: str) -> Any:
#     """Getter-function for the field value."""
#     styleKey = '%s/%s' % (self._getStylePrefix(), name)
#     styleMap = self._getStyleMap()
#     if styleKey in styleMap:
#       fb = styleMap[styleKey]
#     else:
#       e = """Received field name '%s' yielding style-key: '%s', but no such
#       has been registered: \n%s."""
#       names = '\n  '.join([name for name in styleMap.keys()])
#       raise KeyError(monoSpace(e % (name, styleKey, names)))
#     return AppSettings().value(styleKey, fb)
#
#   def paintEvent(self, event: QPaintEvent) -> None:
#     """The paintEvent method paints the widget."""
#     if self.__debug_flag__ is None:
#       return
#     painter = QPainter()
#     painter.begin(self)
#     viewRect = painter.viewport()
#     pen = QPen()
#     pen.setStyle(SolidLine)
#     pen.setWidth(1)
#     pen.setColor(QColor(0, 0, 0, ))
#     painter.setPen(pen)
#     painter.setBrush(emptyBrush())
#     painter.drawRoundedRect(viewRect, 4, 4)
#     painter.end()
