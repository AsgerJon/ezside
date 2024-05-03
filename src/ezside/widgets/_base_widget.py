"""
BaseWidget provides a base class for the widgets. Using AttriBox they
provide brushes, pens and fonts as attributes. These widgets are not meant
for composite widgets directly but instead for the constituents. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QWidget, QBoxLayout, QLayout
from PySide6.QtWidgets import QGridLayout
from attribox import AttriBox
from icecream import ic
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from ezside.core import alignDict, AlignFlag, Center

ic.configureOutput(includeContext=True, )


class _BoxedWidget(QWidget):
  """Convenient class populating the body with the names required by
  AttriBox"""
  __outer_box__ = None
  __owning_instance__ = None
  __field_owner__ = None
  __field_name__ = None

  def getOuterBox(self) -> AttriBox:
    """Getter-function for the outer box"""
    if self.__outer_box__ is None:
      e = """The outer box has not been set!"""
      raise RuntimeError(e)
    if isinstance(self.__outer_box__, AttriBox):
      return self.__outer_box__
    e = typeMsg('__outer_box__', self.__outer_box__, AttriBox)
    raise TypeError(e)

  def getOwningInstance(self) -> Optional[QWidget]:
    """Getter-function for the owning instance"""
    return self.__owning_instance__

  def getFieldName(self) -> Optional[str]:
    """Getter-function for the field name"""
    return self.__field_name__

  def getFieldOwner(self) -> Optional[type]:
    """Getter-function for the field owner"""
    return self.__field_owner__


class _ParserWidget(_BoxedWidget):
  """Convenient class providing parsers"""

  @staticmethod
  def _namedLayout(layoutName: str, **kwargs) -> QLayout:
    """Tries to return the layout named"""
    if layoutName in alignDict:
      return alignDict[layoutName]
    if kwargs.get('strict', False):
      e = """Unable to recognize '%s' as the name of a layout!"""
      raise ValueError(e)

  @classmethod
  def _parseLayout(cls, *args, **kwargs) -> Optional[QLayout]:
    """Parses from given arguments an instance of QLayout"""
    layoutKeys = stringList("""layout, ui, grid""")
    for key in layoutKeys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, QLayout):
          return val
        if isinstance(val, str):
          return cls._namedLayout(val, strict=True)
        e = typeMsg('layout', val, QLayout)
        raise TypeError(e)
    else:
      for arg in args:
        if isinstance(arg, QLayout):
          return arg
        if isinstance(arg, str):
          arg = cls._namedLayout(arg, strict=False)
          if arg is not None:
            return arg

  @staticmethod
  def _parseGrid(*args, **kwargs) -> dict[str, Optional[int]]:
    """Parses argument to row, col, rowSpan and colSpan"""
    rowKeys = stringList("""row, vertical""")
    colKeys = stringList("""col, horizontal""")
    rowSpanKeys = stringList("""rowSpan, verticalSpan""")
    colSpanKeys = stringList("""colSpan, horizontalSpan""")
    KEYS = [rowKeys, colKeys, rowSpanKeys, colSpanKeys]
    values = dict(row=None, col=None, rowSpan=None, colSpan=None)
    for (keys, name) in zip(KEYS, values):
      for key in keys:
        if key in kwargs:
          val = kwargs[key]
          if isinstance(val, int):
            values[name] = val
            break
          e = typeMsg(key, val, int)
          raise TypeError(e)
      else:
        for arg in args:
          if isinstance(arg, int):
            values[name] = arg
            break
    return values

  @staticmethod
  def _parseAlign(*args, **kwargs) -> Optional[AlignFlag]:
    """Parses argument to AlignFlag"""
    alignKeys = stringList("""align, alignment""")
    for key in alignKeys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, AlignFlag):
          return val
        if isinstance(val, str):
          return alignDict[val]
        e = typeMsg('align', val, AlignFlag)
        raise TypeError(e)


class BaseWidget(_ParserWidget):
  """BaseWidget provides a base class for the widgets. Using AttriBox they
  provide brushes, pens and fonts as attributes. These widgets are not meant
  for composite widgets directly but instead for the constituents. """

  def getMain(self, ) -> BaseWidget:
    """Getter-function for the main window"""
    main = self
    while isinstance(main.getOwningInstance(), BaseWidget):
      main = main.getOwningInstance()
    return main

  def getApp(self, ) -> QCoreApplication:
    """Getter-function for the application"""
    return self.getMain().getApp()

  def initStyle(self, ) -> None:
    """Initialize the style of the widget"""

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""

  def initSignalSlot(self) -> None:
    """Initialize the signal slot"""

  def layIn(self, *args, **kwargs) -> None:
    """Places self in given layout"""
    self.getApp()
    layout = self._parseLayout(*args, **kwargs)
    if layout is None:
      e = """Missing layout argument!"""
      raise ValueError(e)
    self.initStyle()
    self.initUi()
    self.initSignalSlot()
    align = self._parseAlign(*args, **kwargs) or Center
    if isinstance(layout, QGridLayout):
      parsed = self._parseGrid(*args, **kwargs)
      row = parsed.get('row', None)
      col = parsed.get('col', None)
      if row is None or col is None:
        e = """Missing row or column argument"""
        raise ValueError(e)
      rowSpan = parsed.get('rowSpan', 1)
      colSpan = parsed.get('colSpan', 1)
      QGridLayout.addWidget(layout, self, row, col, rowSpan, colSpan, align)
    if isinstance(layout, QBoxLayout):
      return QBoxLayout.addWidget(layout, self, alignment=align)
    return layout.addWidget(self, alignment=align)
