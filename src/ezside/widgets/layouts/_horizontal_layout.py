"""HorizontalLayout provides a layout packing widgets horizontally. The
class supports alignments and spacing between widgets. It achieves this by
the use of spacers. Although labelled a 'layout' it is in fact a widget.
The suggested use is to add widget classes to it during initUi and call
'setCentralWidget' on it after. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QHBoxLayout, QMainWindow
from attribox import AttriBox
from vistutils.waitaminute import typeMsg

from ezside.core import AlignLeft, \
  Center, \
  AlignHCenter, \
  AlignRight, \
  Tight, \
  Prefer
from ezside.widgets import BaseWidget
from ezside.widgets.layouts import AbstractLayout

Shiboken = type(QObject)


class HorizontalLayout(AbstractLayout):
  """HorizontalLayout provides a layout packing widgets horizontally. The
  class supports alignments and spacing between widgets. It achieves this by
  the use of spacers."""

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
    """Registers field"""
    return {}

  @classmethod
  def registerStates(cls) -> list[str]:
    """Registers states"""
    return ['base', ]

  @classmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """Registers dynamic fields"""
    return {}

  def detectState(self) -> str:
    """State detection"""
    return 'base'

  __inner_layout__ = AttriBox[QHBoxLayout]()

  def __init__(self, *args, **kwargs) -> None:
    AbstractLayout.__init__(self, *args, **kwargs)
    self.setSizePolicy(Tight, Prefer, )

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    parent = self.getOwningInstance()
    self.__inner_layout__.setContentsMargins(0, 0, 0, 0)
    self.__inner_layout__.setSpacing(self.spacing)
    if self.hAlign in [AlignRight, AlignHCenter, Center]:
      self.__inner_layout__.addWidget(self.__left_spacer__)
    for entry in self._getAddedWidgets():
      cls, args, kwargs = entry['widget'], entry['pos'], entry['key']
      widget = self.initWidget(cls, *args, **kwargs)
      self.__inner_layout__.addWidget(widget)
    self.setLayout(self.__inner_layout__)
    if self.hAlign in [AlignHCenter, Center, AlignLeft]:
      self.__inner_layout__.addWidget(self.__right_spacer__, )
    if isinstance(parent, QMainWindow):
      self.setLayout(self.__inner_layout__)
      parent.setCentralWidget(self)
    elif isinstance(parent, BaseWidget):
      parent.setLayout(self.__inner_layout__)
    else:
      e = typeMsg('parent', parent, BaseWidget)
      raise TypeError
