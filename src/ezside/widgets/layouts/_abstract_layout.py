"""AbstractLayout provides a subclass of BaseWidget implementing layout
functionality through composition. Instead of calling 'addWidget' on a
widget, it should be called on the layout. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
import os.path
from typing import Any, Self

from PySide6.QtCore import QObject
from attribox import AttriBox
from icecream import ic
from vistutils.parse import maybe
from vistutils.waitaminute import typeMsg

from ezside.core import AlignVCenter, \
  AlignHCenter, \
  AlignFlag, \
  AlignBottom, \
  AlignTop, AlignRight, AlignLeft
from ezside.widgets import BaseWidget, HorizontalSpacer, VerticalSpacer
from ezside.widgets.layouts import AlignBox
from morevistutils import Bag

Shiboken = type(QObject)

ic.configureOutput(includeContext=True, )


class AbstractLayout(BaseWidget):
  """HorizontalLayout provides a layout packing widgets horizontally. The
  class supports alignments and spacing between widgets. It achieves this by
  the use of spacers."""
  __iter_contents__ = None

  __first_run__ = True

  __added_widgets__ = None
  __widgets_dict__ = None
  __widget_instances__ = None

  vAlign = AttriBox[AlignBox]()
  hAlign = AttriBox[AlignBox]()
  __left_spacer__ = AttriBox[HorizontalSpacer]()
  __right_spacer__ = AttriBox[HorizontalSpacer]()
  __top_spacer__ = AttriBox[VerticalSpacer]()
  __bottom_spacer__ = AttriBox[VerticalSpacer]()
  spacing = AttriBox[int]()
  widgets = AttriBox[list]()

  def __init__(self, *args, **kwargs) -> None:
    BaseWidget.__init__(self, *args, **kwargs)
    _spacing, _h, _v = None, None, None
    _spacing = kwargs.get('spacing', None)
    _h = kwargs.get('hAlign', None)
    _v = kwargs.get('vAlign', None)
    for arg in args:
      if isinstance(arg, int) and _spacing is None:
        _spacing = arg
      elif isinstance(arg, AlignFlag):
        if arg in [AlignVCenter, AlignTop, AlignBottom] and _v is None:
          _v = arg
        elif arg in [AlignHCenter, AlignLeft, AlignRight] and _h is None:
          _h = arg
    self.spacing = maybe(_spacing, 0)
    self.vAlign = maybe(_v, AlignVCenter)
    self.hAlign = maybe(_h, AlignHCenter)

  def _getAddedWidgets(self) -> list[dict[str, Any]]:
    """Return the added widgets classes."""
    if self.__added_widgets__ is None:
      self.__added_widgets__ = []
    return self.__added_widgets__

  def _getWidgetDict(self, ) -> dict[str, Any]:
    """Return the added widgets classes."""
    if self.__widgets_dict__ is None:
      self.__widgets_dict__ = {}
    return self.__widgets_dict__

  def _registerWidget(self, widget: BaseWidget, key: str) -> None:
    """Register the widget instance."""
    self._getWidgetDict()[key] = widget

  @abstractmethod
  def initUi(self, ) -> None:
    """Subclasses must implement this method. It should instantiate the
    widgets added with 'addWidget', add them to the layout and finally
    set the layout to itself. Generally, subclasses should provide an
    internal instance of QLayout or a subclass thereof. For example
    through the use of AttriBox. """

  def initSignalSlot(self, ) -> None:
    """Since the same layout subclass is intended to manage different
    widgets and widget setups, widgets should in general not rely on this
    method. Instead,  subclasses of BaseWidget should organize signals on
    slots themselves. Nevertheless, it is available to implement and if
    so it is invoked after 'initUi'. """

  def addWidget(self, WidgetClass: Any, *args, **kwargs) -> None:
    """Add a widget class to the layout. Please note, that deferred
    arguments may be included in this call. These are then passed to the
    widget class upon instantiation. """
    if isinstance(WidgetClass, Bag):
      return self.addWidget(WidgetClass.cls,
                            *[*WidgetClass.posArgs, *args, ],
                            **{**WidgetClass.keyArgs, **kwargs, })
    if not isinstance(WidgetClass, type):
      e = typeMsg('WidgetClass', WidgetClass, type)
      raise TypeError(e)
    if not issubclass(WidgetClass, BaseWidget):
      e = typeMsg('WidgetClass', WidgetClass, BaseWidget)
      raise TypeError(e)
    entry = dict(widget=WidgetClass, pos=[*args, ], key={**kwargs, })
    self._getAddedWidgets().append(entry)

  def initWidget(self, cls: Shiboken, *args, **kwargs) -> BaseWidget:
    """Initiates the given Widget class. Please note that Shiboken is the
    special metaclass from which QObject is derived. """
    if not isinstance(cls, Shiboken):
      e = typeMsg('Widget', cls, Shiboken)
      raise TypeError(e)
    if not issubclass(cls, BaseWidget):
      e = typeMsg('Widget', cls, BaseWidget)
      raise TypeError(e)
    parent = self.getOwningInstance()
    key = kwargs.get('key', None)
    ic(key)
    widget = cls(parent, *args, **kwargs)
    widget.initUi()
    widget.initSignalSlot()
    self.widgets.append(widget)
    if key is not None:
      if isinstance(key, str):
        self._registerWidget(widget, key)
    return widget

  def __iter__(self, ) -> Self:
    """Implementation of iterator protocol."""
    self.__iter_contents__ = [*self.widgets, ]
    return self

  def __next__(self, ) -> Any:
    """Implementation of iterator protocol."""
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __len__(self, ) -> int:
    """Return the number of widgets added to the layout."""
    return len(self._getAddedWidgets())

  def __getitem__(self, *args) -> BaseWidget:
    """Return the widget at the given index."""
    try:
      if len(args) != 1:
        e = """AbstractLayout only supports one argument for indexing."""
        raise TypeError(e)
      index, key = None, None
      if isinstance(args[0], int):
        return self.widgets[args[0]]
      elif isinstance(args[0], str):
        widget = self._getWidgetDict().get(args[0], )
        if isinstance(widget, BaseWidget):
          return widget
        e = typeMsg('key', widget, BaseWidget)
        raise TypeError(e) from Exception(str(args))
    except Exception as exception:
      if self.__first_run__:
        lines = []
        for key, val in self._getWidgetDict().items():
          lines.append('%s: %s' % (key, val))
        txt = '\n'.join(lines)
        here = os.path.dirname(os.path.abspath(__file__))
        fid = os.path.join(here, 'lmao')
        with open(fid, 'w', encoding='utf8') as f:
          f.write(txt)
        __first_run__ = False

      raise exception
