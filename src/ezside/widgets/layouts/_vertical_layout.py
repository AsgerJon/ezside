"""VerticalLayout provides a layout packing widgets vertically. The
class supports alignments and spacing between widgets. It achieves this by
the use of spacers. Although labelled a 'layout' it is in fact a widget.
The suggested use is to add widget classes to it during initUi and call
'setCentralWidget' on it after. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout
from attribox import AttriBox

from ezside.core import AlignTop, AlignVCenter, Center, AlignBottom
from ezside.widgets.layouts import AbstractLayout


class VerticalLayout(AbstractLayout):
  """VerticalLayout provides a layout packing widgets vertically. The
  class supports alignments and spacing between widgets. It achieves this by
  the use of spacers."""

  __inner_layout__ = AttriBox[QVBoxLayout]()

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    parent = self.getOwningInstance()
    self.__inner_layout__.setContentsMargins(0, 0, 0, 0)
    self.__inner_layout__.setSpacing(self.spacing)
    if self.vAlign in [AlignTop, AlignVCenter, Center]:
      self.__inner_layout__.addWidget(self.__top_spacer__)
    for entry in self._getAddedWidgets():
      cls, args, kwargs = entry['widget'], entry['pos'], entry['key']
      self.__inner_layout__.addWidget(cls(parent, *args, **kwargs))
    if self.vAlign in [AlignBottom, AlignVCenter, Center]:
      self.__inner_layout__.addWidget(self.__bottom_spacer__)
    self.setLayout(self.__inner_layout__)
