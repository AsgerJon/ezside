"""LayoutWidget provides a base class for widget classes intended for
management by the 'ezside.layouts' module."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Optional, TYPE_CHECKING

from PySide6.QtCore import QRect, QRectF, QSize
from PySide6.QtGui import QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget, QMainWindow
from worktoy.desc import Field
from worktoy.text import typeMsg

if TYPE_CHECKING:
  from ezside.layouts import AbstractLayout, LayoutItem

Rect: TypeAlias = Union[QRect, QRectF]


class LayoutWidget(QWidget):
  """LayoutWidget provides a base class for widget classes intended for
  management by the 'ezside.layouts' module."""

  __parent_layout__ = None
  __parent_layout_item__ = None
  __parent_rect__ = None
  __main_window__ = None

  parentLayout = Field()
  parentLayoutItem = Field()
  parentRect = Field()
  mainWindow = Field()

  @parentRect.GET
  def _getParentRect(self) -> QRectF:
    """Getter-function for the rectangle in the parent layout assigned to
    the inner content of this widget. """
    if isinstance(self.__parent_rect__, QRectF):
      return self.__parent_rect__
    if isinstance(self.__parent_rect__, QRect):
      return QRect.toRectF(self.__parent_rect__)
    return QRectF()

  @parentRect.SET
  def _setParentRect(self, rect: Rect) -> None:
    """Setter-function for the rectangle in the parent layout assigned to
    the inner content of this widget. """
    if not isinstance(rect, (QRect, QRectF)):
      e = typeMsg('parentRect', rect, QRectF)
      raise TypeError(e)
    self.__parent_rect__ = rect

  @parentLayoutItem.GET
  def _getParentLayoutItem(self) -> LayoutItem:
    """Getter-function for the layout item on the parent layout that
    contains this widget."""
    return self.__parent_layout_item__

  @parentLayoutItem.SET
  def _setParentLayoutItem(self, item: LayoutItem) -> None:
    """Setter-function for the layout item on the parent layout that
    contains this widget."""
    self.__parent_layout_item__ = item

  @parentLayout.GET
  def _getParentLayout(self) -> Optional[AbstractLayout]:
    """Getter-function for the parentLayout."""
    return self.__parent_layout__

  @parentLayout.SET
  def _setParentLayout(self, parentLayout: AbstractLayout) -> None:
    """Setter-function for the parentLayout."""
    if not isinstance(parentLayout, QWidget):
      e = typeMsg('parentLayout', parentLayout, QWidget)
      raise TypeError(e)
    self.__parent_layout__ = parentLayout

  @mainWindow.GET
  def _getMainWindow(self) -> Optional[QWidget]:
    """Getter-function for the mainWindow."""
    return self.__main_window__

  @mainWindow.SET
  def _setMainWindow(self, mainWindow: QMainWindow) -> None:
    """Setter-function for the mainWindow."""
    if not isinstance(mainWindow, QMainWindow):
      e = typeMsg('mainWindow', mainWindow, QMainWindow)
      raise TypeError(e)
    self.__main_window__ = mainWindow

  def sizeHint(self, ) -> QSize:
    """This method returns zero size to allow the widget to be managed
    entirely by the parent layout. """
    return QSize(0, 0, )

  def paintMeLike(self,
                  rect: Rect,
                  painter: QPainter,
                  event: QPaintEvent) -> Optional[tuple[Rect, QPainter]]:
    """Subclasses should implement this method to specify how to paint
    them. When used in a layout from 'ezside.layouts', only this method
    can specify painting, as QWidget.paintEvent will not be called.

    The painter and rectangle passed are managed by the layout and
    base widgets are expected to draw only inside the given rect. The
    layout ensures that this rect is at least the exact size specified by the
    'requiredSize' method on this widget.

    The method may return the rect and painter for further painting by a
    subclass. """

  def requiredSize(self) -> QSize:
    """This method informs the parent layout of the size this widget at
    minimum requires to render. """

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, type(self)):
        self.parentLayout = arg
        QWidget.__init__(self, arg)
        break
      if isinstance(arg, QMainWindow):
        self.mainWindow = arg
        QWidget.__init__(self, arg)
        break
    else:
      QWidget.__init__(self)
