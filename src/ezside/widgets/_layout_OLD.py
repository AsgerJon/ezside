"""Layout provides the request type of QLayout, either vertical,
horizontal or gridded. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtWidgets import QGridLayout, QWidget
from attribox import AttriBox
from icecream import ic
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from eznum import EZnum, auto
from ezside.widgets import BaseWidget


class LayoutEnum(EZnum):
  """LayoutEnum provides the request type of QLayout, either vertical,
  horizontal or gridded. """
  VERTICAL = auto()
  HORIZONTAL = auto()
  GRID = auto()


class InnerLayout(QGridLayout):
  """Layout wrapper"""

  __col_count__ = 0
  __row_count__ = 0
  __total_count__ = 0

  def __init__(self, layoutType: Any = None) -> None:
    """Initializes the Layout instance. """
    QGridLayout.__init__(self, )
    self.__layout_mode__ = None
    if isinstance(layoutType, LayoutEnum):
      self.__layout_mode__ = layoutType
    elif isinstance(layoutType, str):
      if layoutType in LayoutEnum:
        self.__layout_mode__ = LayoutEnum[layoutType]
    else:
      self.__layout_mode__ = LayoutEnum['grid']

  def addWidget(self, *args) -> None:
    """Adds a widget to the layout. """
    if self.__layout_mode__ == LayoutEnum.HORIZONTAL:
      self.addHorizontalWidget(*args)
    elif self.__layout_mode__ == LayoutEnum.VERTICAL:
      self.addVerticalWidget(*args)
    elif self.__layout_mode__ == LayoutEnum.GRID:
      self.addGridWidget(*args)

  def addHorizontalWidget(self, *args) -> None:
    """Adds a widget to the layout. """
    widget = [*[a for a in args if isinstance(a, QWidget)], None][0]
    if isinstance(widget, QWidget):
      QGridLayout.addWidget(self, widget, 0, self.__total_count__, )
      self.__total_count__ += 1
      self.__col_count__ += 1

  def addVerticalWidget(self, *args) -> None:
    """Adds a widget to the layout. """
    widget = [*[a for a in args if isinstance(a, QWidget)], None][0]
    if isinstance(widget, QWidget):
      QGridLayout.addWidget(self, widget, self.__total_count__, 0)
      self.__total_count__ += 1
      self.__row_count__ += 1

  def addGridWidget(self, *args) -> None:
    """Adds a widget to the layout. """
    widget = [*[a for a in args if isinstance(a, QWidget)], None][0]
    intArgs = [a for a in args if isinstance(a, int)]
    row, col, rowSpan, colSpan = None, None, None, None
    if len(intArgs) % 2:
      e = """Expected even number of integer arguments, but received: %d"""
      raise ValueError(e % len(intArgs))
    if len(intArgs) > 4:
      e = """Expected at most 4 integer arguments, but received: %d"""
      raise ValueError(e % len(intArgs))
    if len(intArgs) == 4:
      row, col, rowSpan, colSpan, = intArgs
    elif len(intArgs) == 2:
      row, col, rowSpan, colSpan, = intArgs[0], intArgs[1], 1, 1
    elif not intArgs:
      rowSpan, colSpan = 1, 1
      C, R = self.__col_count__, self.__row_count__
      c = self.__total_count__ % self.__col_count__
      r = self.__total_count__ % self.__row_count__
      if C > R:
        row, col = r - 1, c
        self.__col_count__ += colSpan
      else:
        row, col = r, c - 1
        self.__row_count__ += rowSpan
    if all([isinstance(a, int) for a in [row, col, rowSpan, colSpan]]):
      QGridLayout.addWidget(self, widget, row, col, rowSpan, colSpan)
      self.__total_count__ += (rowSpan * colSpan)

  def parentAddWidget(self, widget, *args) -> None:
    """Adds a widget to the layout. """
    widget.initUi()
    widget.connectActions()
    if isinstance(widget, BaseWidget):
      QGridLayout.addWidget(self, widget, *args)
    elif isinstance(widget, QWidget):
      QGridLayout.addWidget(self, widget, *args)
    else:
      e = typeMsg('widget', widget, BaseWidget)
      raise TypeError(e)


class Layout(BaseWidget):
  """Layout class with built-in widget"""

  baseWidget = AttriBox[BaseWidget]()
  innerLayout = AttriBox[InnerLayout]()
  __total_count__ = 0

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the Layout instance. """
    BaseWidget.__init__(self, )
    ic(self)
    self.__widget_registry__ = {}
    self.layoutType = None
    modeKeys = stringList("""layoutType, mode, orientation""")
    for key in modeKeys:
      if key in kwargs:
        val = kwargs.get(key)
        if val in LayoutEnum:
          self.layoutType = val
          break
        if isinstance(val, str):
          if val in LayoutEnum:
            self.layoutType = LayoutEnum[val]
            break
    else:
      for arg in args:
        if arg in LayoutEnum:
          self.layoutType = arg
          break
      else:
        self.layoutType = LayoutEnum['grid']

  def addWidget(self, widget: BaseWidget, *args) -> None:
    """Adds a widget to the layout. """
    if self.innerLayout.__layout_mode__ == LayoutEnum.VERTICAL:
      return self.innerLayout.addVerticalWidget(widget)
    if self.innerLayout.__layout_mode__ == LayoutEnum.HORIZONTAL:
      return self.innerLayout.addHorizontalWidget(widget)
    row, col, rowSpan, colSpan = [*args, 1, 1, ][:4]
    key = row + col * 1j
    if key in self.__widget_registry__:
      e = """A widget already exists at the given position."""
      raise ValueError(e)
    self.innerLayout.parentAddWidget(widget, *args)
    self.__widget_registry__[key] = widget
    for i in range(rowSpan):
      for j in range(colSpan):
        self.__widget_registry__[key + i + j * 1j] = widget
        text = '__widget_%s_%s__' % (i, j)
        setattr(self, text, widget)

  def buildLayout(self) -> None:
    """Builds the layout. """
    for (position, widget) in self.__widget_registry__.items():
      if not isinstance(widget, (BaseWidget, QWidget)):
        e = typeMsg('widget', widget, BaseWidget)
        raise TypeError(e)
      widget.initUi()
      widget.connectActions()
      self.innerLayout.parentAddWidget(widget, *position)
    self.setLayout(self.innerLayout)
    self.initUi()
