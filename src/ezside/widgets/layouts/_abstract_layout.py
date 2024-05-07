"""AbstractLayout provides a subclass of BaseWidget implementing layout
functionality through composition. Instead of calling 'addWidget' on a
widget, it should be called on the layout. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from PySide6.QtCore import QObject
from attribox import AttriBox
from vistutils.waitaminute import typeMsg

from ezside.widgets import BaseWidget, HorizontalSpacer, VerticalSpacer
from ezside.widgets.layouts import AlignBox

Shiboken = type(QObject)


class AbstractLayout(BaseWidget):
  """HorizontalLayout provides a layout packing widgets horizontally. The
  class supports alignments and spacing between widgets. It achieves this by
  the use of spacers."""

  __added_widgets__ = None

  vAlign = AttriBox[AlignBox]()
  hAlign = AttriBox[AlignBox]()
  __left_spacer__ = AttriBox[HorizontalSpacer]()
  __right_spacer__ = AttriBox[HorizontalSpacer]()
  __top_spacer__ = AttriBox[VerticalSpacer]()
  __bottom_spacer__ = AttriBox[VerticalSpacer]()
  spacing = AttriBox[int]()

  def _getAddedWidgets(self) -> list[dict[str, Any]]:
    """Return the added widgets classes."""
    if self.__added_widgets__ is None:
      self.__added_widgets__ = []
    return self.__added_widgets__

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

  def addWidget(self, cls: Shiboken, *args, **kwargs) -> None:
    """Add a widget class to the layout. Please note, that deferred
    arguments may be included in this call. These are then passed to the
    widget class upon instantiation. """
    if not issubclass(cls, BaseWidget):
      e = typeMsg('cls', cls, BaseWidget)
      raise TypeError(e)
    entry = dict(widget=cls, pos=[*args, ], key={**kwargs, })
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
    widget = cls(parent, *args, **kwargs)
    widget.initUi()
    widget.initSignalSlot()
    return widget
