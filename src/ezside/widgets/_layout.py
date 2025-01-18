"""Layout subclasses QGridLayout providing support for widgets in the
framework. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from PySide6.QtWidgets import QGridLayout, QApplication, QWidget, QLayout

from worktoy.text import typeMsg, monoSpace
from worktoy.parse import maybe
from worktoy.desc import AttriBox, Field, THIS
from worktoy.base import BaseObject, overload, FastObject

from . import AbstractWidget, LayoutIndex
from ..enums import Align, VerticalAlign, HorizontalAlign


class Layout(BaseObject):
  """Layout subclasses QGridLayout providing support for widgets in the
  framework. """

  __iter_contents__ = None

  __fallback_hor__ = HorizontalAlign.LEFT
  __fallback_ver__ = VerticalAlign.TOP
  __hor_align__ = None
  __ver_align__ = None

  __base_widget__ = None
  __base_layout__ = None
  __parent_widget__ = None
  __child_widgets__ = None

  baseWidget = Field()  # Windows should set this widget as central widget
  Q = Field()  # The underlying QGridLayout instance
  parent = Field()  # The parent widget or window of this layout
  nCols = Field()  # The number of columns in the layout
  nRows = Field()  # The number of rows in the layout
  horAlign = Field()  # The horizontal alignment of the layout
  verAlign = Field()  # The vertical alignment of the layout
  align = Field()  # The alignment of the layout

  @nCols.GET
  def _getNCols(self, ) -> int:
    """Getter-function for number of columns in the layout."""
    out = -1
    for (index, _) in self:
      out = max(out, index.lastCol)
    return out + 1

  @nRows.GET
  def _getNRows(self, ) -> int:
    """Getter-function for number of rows in the layout."""
    out = -1
    for (index, _) in self:
      out = max(out, index.lastRow)
    return out + 1

  @horAlign.GET
  def _getHorAlign(self, ) -> Align:
    """Getter-function for horizontal alignment of the layout."""
    return maybe(self.__hor_align__, self.__fallback_hor__)

  @verAlign.GET
  def _getVerAlign(self, ) -> Align:
    """Getter-function for vertical alignment of the layout."""
    return maybe(self.__ver_align__, self.__fallback_ver__)

  @align.GET
  def _getAlign(self, ) -> Align:
    """Getter-function for the alignment of the layout."""
    hor, ver = self.horAlign, self.verAlign
    for member in Align:
      if member.horizontal == hor and member.vertical == ver:
        return member
    e = """Unable to resolve alignment: %s, %s!"""
    raise ValueError(monoSpace(e % (hor, ver)))

  def _getChildWidgets(self, ) -> dict[LayoutIndex, AbstractWidget]:
    return maybe(self.__child_widgets__, dict())

  def __getitem__(self, layoutIndex: LayoutIndex) -> AbstractWidget:
    for (index, widget) in self:
      if layoutIndex in index:
        return widget
    e = """This layout does not provide a widget at: %s!"""
    raise IndexError(monoSpace(e % layoutIndex))

  def __setitem__(self, index: LayoutIndex, widget: AbstractWidget) -> None:
    if not isinstance(widget, AbstractWidget):
      e = typeMsg('widget', widget, AbstractWidget)
      raise TypeError(e)
    if not isinstance(index, LayoutIndex):
      e = typeMsg('index', index, LayoutIndex)
      raise TypeError(e)
    existing = self._getChildWidgets()
    if index in existing:
      e = """A widget already exists at index: %s!"""
      raise IndexError(monoSpace(e % index))
    self.__child_widgets__ = {**existing, index: widget}

  def __contains__(self, layoutIndex: LayoutIndex) -> bool:
    try:
      return self[layoutIndex] or True
    except IndexError:
      return False

  def _createLayout(self, ) -> None:
    """This method creates the layout for the widget. """
    if TYPE_CHECKING:
      assert isinstance(self.baseWidget, QWidget)
      assert isinstance(self.Q, QGridLayout)
      assert isinstance(self.align, Align)
    self.__base_layout__ = QGridLayout()
    QLayout.setAlignment(self.Q, self.align.Q)
    for (index, widget) in self:
      widget.initUi()
      QGridLayout.addWidget(self.__base_layout__, widget, *index.values())

  @Q.GET
  def _getBaseLayout(self, **kwargs) -> QGridLayout:
    if self.__base_layout__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createLayout()
      return self._getBaseLayout(_recursion=True)
    if isinstance(self.__base_layout__, QGridLayout):
      return self.__base_layout__
    e = typeMsg('__base_layout__', self.__base_layout__, QGridLayout)
    raise TypeError(e)

  def _createWidget(self, ) -> None:
    """This method creates the widget for the layout. """
    if TYPE_CHECKING:
      assert isinstance(self.parent, QWidget)
      assert isinstance(self.Q, QGridLayout)
    self.__base_widget__ = QWidget(self.parent)
    self.__base_widget__.setLayout(self.Q)

  @baseWidget.GET
  def _getBaseWidget(self, **kwargs) -> QWidget:
    if self.__base_widget__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createWidget()
      return self._getBaseWidget(_recursion=True)
    if isinstance(self.__base_widget__, QWidget):
      return self.__base_widget__
    e = typeMsg('__inner_widget__', self.__base_widget__, QWidget)
    raise TypeError(e)

  @parent.GET
  def _getParent(self, ) -> QWidget:
    if self.__parent_widget__ is None:
      e = """The parent widget has not been set!"""
      raise RuntimeError(monoSpace(e))
    if isinstance(self.__parent_widget__, QWidget):
      return self.__parent_widget__
    e = typeMsg('__parent_widget__', self.__parent_widget__, QWidget)
    raise TypeError(monoSpace(e))

  def __init__(self, *args, **kwargs) -> None:
    for arg in args:
      if isinstance(arg, QWidget):
        self.__parent_widget__ = arg
        break
    else:
      e = """The parent widget must be set as the first argument to the
      constructor!"""
      raise ValueError(monoSpace(e))

  def __iter__(self, ) -> Self:
    """Implements the iterator protocol. """
    self.__iter_contents__ = [*self._getChildWidgets().items(), ]
    return self

  def __next__(self, ) -> tuple[LayoutIndex, AbstractWidget]:
    if self.__iter_contents__ is None:
      e = """The iterator has not been initialized!"""
      raise RuntimeError(e)
    if not isinstance(self.__iter_contents__, list):
      e = typeMsg('__iter_contents__', self.__iter_contents__, list)
      raise TypeError(e)
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def nextIndex(self, ) -> LayoutIndex:
    """This method suggest the next index in the layout. """
    if TYPE_CHECKING:
      assert isinstance(self.nRows, int)
      assert isinstance(self.nCols, int)
    for i in range(self.nRows):
      for j in range(self.nCols):
        try:
          if not isinstance(self[LayoutIndex(i, j)], AbstractWidget):
            raise TypeError
          continue
        except IndexError:
          return LayoutIndex(i, j)
    if self.nRows > self.nCols:  # Adds a column
      return LayoutIndex(0, self.nCols)
    return LayoutIndex(self.nRows, 0)  # Adds a row

  def addWidget(self, widget: AbstractWidget, *args, **kwargs) -> None:
    """This method adds a widget to the layout. """
    if not args:
      if kwargs.get('_recursion', False):
        raise RecursionError
      return self.addWidget(widget, self.nextIndex(), _recursion=True)
    index = LayoutIndex(*args)
    widget.initUi()
    self[index] = widget
