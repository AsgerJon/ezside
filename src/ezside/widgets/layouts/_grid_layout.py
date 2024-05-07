"""GridLayout provides a grid layout for organizing widgets in a grid. The
class supports alignments and spacing between widgets. It achieves this by
the use of spacers. Although labelled a 'layout' it is in fact a widget.
The suggested use is to add widget classes to it during initUi and call
'setCentralWidget' on it after."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QGridLayout
from attribox import AttriBox
from vistutils.text import monoSpace

from ezside.widgets.layouts import AbstractLayout
from ezside.core import AlignLeft, AlignHCenter, AlignRight, Center
from ezside.core import AlignTop, AlignVCenter, AlignBottom


class GridLayout(AbstractLayout):
  """GridLayout provides a grid layout for organizing widgets in a grid. The
  class supports alignments and spacing between widgets. It achieves this by
  the use of spacers. Although labelled a 'layout' it is in fact a widget.
  The suggested use is to add widget classes to it during initUi and call
  'setCentralWidget' on it after."""

  __inner_layout__ = AttriBox[QGridLayout]()

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    parent = self.getOwningInstance()
    self.__inner_layout__.setContentsMargins(0, 0, 0, 0)
    self.__inner_layout__.setSpacing(self.spacing)
    addedWidgets = self._getAddedWidgets()
    rowOffset, colOffset = 0, 0
    if self.hAlign in [AlignLeft, AlignHCenter, Center]:
      rowOffset = 1
    if self.vAlign in [AlignTop, AlignVCenter, Center]:
      colOffset = 1
    maxRow, maxCol = 0, 0
    for entry in addedWidgets:
      cls, args, kwargs = entry['widget'], entry['pos'], entry['key']
      intArgs = [arg for arg in args if isinstance(arg, int)]
      notInts = [arg for arg in args if not isinstance(arg, int)]
      row, col = kwargs.get('row', None), kwargs.get('col', None)
      rowSpan = kwargs.get('rowSpan', 1)
      colSpan = kwargs.get('colSpan', 1)
      if row is None and col is None:
        if len(intArgs) in [2, 4]:
          row, col, rowSpan, colSpan = [*intArgs, 1, 1][:4]
        else:
          e = """GridLayout requires 2 or 4 integer arguments for each widget
          specifying the row and column and optional the row and column 
          span. The spans default to 1. If integers are required in the 
          positional arguments by the constructor, GridLayout does provide
          keyword arguments at 'row' and 'col' and at 'rowSpan' and 
          'colSpan'. """
          raise ValueError(monoSpace(e))
      elif row is None or col is None:
        e = """When setting row and col with keyword arguments, both must 
        be provided, but received: %s, %s""" % (row, col)
        raise ValueError(monoSpace(e))
      row += rowOffset
      col += colOffset
      maxRow = max(row + rowSpan, maxRow)
      maxCol = max(col + colSpan, maxCol)
      widget = cls(parent, *notInts, **kwargs)
      self.__inner_layout__.addWidget(widget, row, col, rowSpan, colSpan)
    if rowOffset:
      self.__inner_layout__.addWidget(self.__left_spacer__, 0, 0, maxCol, 1)
    if colOffset:
      self.__inner_layout__.addWidget(self.__top_spacer__, 0, 0, 1, maxRow)
    if self.hAlign in [AlignHCenter, Center, AlignRight]:
      rightSpacer = self.__right_spacer__
      self.__inner_layout__.addWidget(rightSpacer, 0, maxCol, maxRow, 1)
    if self.vAlign in [AlignVCenter, Center, AlignBottom]:
      bottomSpacer = self.__bottom_spacer__
      self.__inner_layout__.addWidget(bottomSpacer, maxRow, 0, 1, maxCol)
    self.setLayout(self.__inner_layout__)
