"""HorizontalLayout provides a layout packing widgets horizontally. The
class supports alignments and spacing between widgets. It achieves this by
the use of spacers. Although labelled a 'layout' it is in fact a widget.
The suggested use is to add widget classes to it during initUi and call
'setCentralWidget' on it after. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QHBoxLayout
from attribox import AttriBox

from ezside.core import AlignLeft, Center, AlignHCenter
from ezside.widgets.layouts import AbstractLayout

Shiboken = type(QObject)


class HorizontalLayout(AbstractLayout):
  """HorizontalLayout provides a layout packing widgets horizontally. The
  class supports alignments and spacing between widgets. It achieves this by
  the use of spacers."""

  __inner_layout__ = AttriBox[QHBoxLayout]()

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    parent = self.getOwningInstance()
    self.__inner_layout__.setContentsMargins(0, 0, 0, 0)
    self.__inner_layout__.setSpacing(self.spacing)
    if self.hAlign in [AlignLeft, AlignHCenter, Center]:
      self.__inner_layout__.addWidget(self.__left_spacer__)
    for entry in self._getAddedWidgets():
      cls, args, kwargs = entry['widget'], entry['pos'], entry['key']
      self.__inner_layout__.addWidget(cls(parent, *args, **kwargs))
    self.setLayout(self.__inner_layout__)
