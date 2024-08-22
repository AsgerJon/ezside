"""LayoutWidget provides a base class for widget classes intended for
management by the 'ezside.layouts' module."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TypeAlias, Union, Optional, TYPE_CHECKING, Any

from PySide6.QtCore import QRect, QRectF, QSizeF, QPointF, QSize, \
  QCoreApplication
from PySide6.QtGui import QPainter, QPaintEvent, QPointerEvent
from PySide6.QtWidgets import QWidget, QMainWindow
from worktoy.desc import Field
from worktoy.parse import maybe
from worktoy.text import typeMsg

from ezside.tools import Align

if TYPE_CHECKING:
  from ezside.layouts import AbstractLayout, LayoutItem, LayoutIndex

Rect: TypeAlias = Union[QRect, QRectF]


class LayoutWidget(QWidget):
  """LayoutWidget provides a base class for widget classes intended for
  management by the 'ezside.layouts' module."""

  __style_id__ = None

  __parent_layout__ = None
  __parent_layout_item__ = None
  __parent_rect__ = None
  __parent_index__ = None
  __main_window__ = None
  __under_mouse__ = None
  __content_alignment__ = None

  styleId = Field()
  style = Field()
  parentLayout = Field()
  parentLayoutItem = Field()
  parentIndex = Field()
  parentRect = Field()
  mainWindow = Field()
  underMouse = Field()
  app = Field()

  @style.GET
  def _getStyle(self, ) -> dict:
    """Getter-function for the style"""

  @styleId.GET
  def _getStyleId(self) -> str:
    """Getter-function for the styleId"""
    if self.__style_id__ is None:
      return 'default'
    if isinstance(self.__style_id__, str):
      return self.__style_id__
    e = typeMsg('styleId', self.__style_id__, str)
    raise TypeError(e)

  @app.GET
  def _getApp(self) -> QCoreApplication:
    """Getter-function for the app"""
    return QCoreApplication.instance()

  @underMouse.GET
  def _getUnderMouse(self) -> bool:
    """Getter-function for the underMouse"""
    return True if self.__under_mouse__ else False

  @underMouse.SET
  def _setUnderMouse(self, underFlag: bool) -> None:
    """Setter-function for the underMouse"""
    if maybe(self.__under_mouse__, False) ^ maybe(underFlag, False):
      self.__under_mouse__ = underFlag

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

  @parentIndex.GET
  def _getParentIndex(self) -> LayoutIndex:
    """Getter-function for the parent index."""
    return self.__parent_index__

  @parentIndex.SET
  def _setParentIndex(self, index: LayoutIndex) -> None:
    """Setter-function for the parent index."""
    self.__parent_index__ = index

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

  def paintMeLike(self,
                  rect: Rect,
                  painter: QPainter,
                  event: QPaintEvent) -> Any:
    """Subclasses should implement this method to specify how to paint
    them. When used in a layout from 'ezside.layouts', only this method
    can specify painting, as QWidget.paintEvent will not be called.

    The painter and rectangle passed are managed by the layout and
    base widgets are expected to draw only inside the given rect. The
    layout ensures that this rect is at least the exact size specified by the
    'requiredSize' method on this widget.

    The method may return the rect and painter for further painting by a
    subclass. """

  def update(self, ) -> None:
    """Transmits update request to parent layout"""
    if self.parentLayout:
      return self.parentLayout.update()
    QWidget.update(self)

  def sizeHint(self) -> QSize:
    """Returns the size hint"""
    if self.parentLayout is None:
      return QSizeF.toSize(self.requiredSize())
    return QSize(0, 0, )

  def minimumSizeHint(self) -> QSize:
    """Return the minimum size hint. """
    if self.parentLayout is None:
      return QSizeF.toSize(self.requiredSize())
    return QSize(0, 0, )

  def _alignRect(self, paintRect: QRectF) -> QRectF:
    """This method returns the rectangle of 'requiredSize' aligned in the
    given rectangle according to the 'Align' setting. """
    rect = QRectF(QPointF(0, 0), self.requiredSize())
    return self.getAlignment().fitRectF(rect, paintRect)

  def requiredSize(self) -> QSizeF:
    """This method informs the parent layout of the size this widget at
    minimum requires to render. """

  def getAlignment(self) -> Align:
    """Getter-function for the alignment setting"""
    return Align.CENTER

  def handleLeaveEvent(self, pointerEvent: QPointerEvent) -> bool:
    """Method handling leave events"""
    return False

  def handleEnterEvent(self, pointerEvent: QPointerEvent) -> bool:
    """Method handling enter events"""
    return False

  def handlePointerEvent(self, pointerEvent: QPointerEvent) -> bool:
    """Method handling pointer events"""
    return False

  def __init__(self, *args, **kwargs) -> None:
    for arg in args:
      if isinstance(arg, QWidget):
        QWidget.__init__(self, arg)
        break
    else:
      QWidget.__init__(self, )
    for arg in args:
      if getattr(arg, '__abstract_layout__', None) is not None:
        self.parentLayout = arg
        break
    id_ = kwargs.get('id', None)
    styleId = kwargs.get('styleId', None)
    styleDefault = 'default'
    self.__style_id__ = maybe(styleId, id_, styleDefault)
