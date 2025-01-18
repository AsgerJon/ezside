"""AbstractWidget provides an abstract baseclass for widgets. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING

from PySide6.QtCore import Signal
from PySide6.QtGui import QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget
from worktoy.desc import Field
from worktoy.text import typeMsg

from ..core import Rect, BoxModel, EmptyPen, EmptyBrush, Size
from ..enums import Align

PaintJob: TypeAlias = tuple[Rect, QPainter]


class AbstractWidget(QWidget):
  """AbstractWidget provides an abstract baseclass for widgets. """

  #  Fallback values for the model, size policy and alignment.
  __fallback_model__ = lambda *__, **_: BoxModel()
  __fallback_align__ = lambda *__, **_: Align.CENTER

  #  Private variables.
  __box_model__ = None
  __size_policy__ = None
  __align_policy__ = None
  __painted_rect__ = None

  __mouse_events__ = None

  sizePol = Field()
  align = Field()

  #  Properties.
  width = Field()
  height = Field()
  paintedRect = Field()
  paintedSize = Field()

  emptyPen = EmptyPen()
  emptyBrush = EmptyBrush()

  debug = Signal(str)
  debugType = Signal(str)
  debugPress = Signal(str)

  @paintedRect.GET
  def _getPaintedRect(self) -> Rect:
    """Getter-function for the paintedRect property."""
    if self.__painted_rect__ is None:
      return Rect()
    return self.__painted_rect__

  @paintedSize.GET
  def _getPaintedSize(self) -> Size:
    """Getter-function for the paintedSize property."""
    if TYPE_CHECKING:
      assert isinstance(self.paintedRect, Rect)
    return self.paintedRect.size

  @width.GET
  def _getWidth(self) -> int:
    """Getter-function for the width property."""
    if TYPE_CHECKING:
      assert isinstance(self.paintedSize, Size)
    return self.paintedSize.width

  @height.GET
  def _getHeight(self) -> int:
    """Getter-function for the height property."""
    if TYPE_CHECKING:
      assert isinstance(self.paintedSize, Size)
    return self.paintedSize.height

  def getBoxModel(self, **kwargs) -> BoxModel:
    """Getter-function for the instance of BoxModel matching current
    state. Subclasses may reimplement this method to provide a specific
    instance of BoxMode.  """
    if self.__box_model__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__box_model__ = self.__fallback_model__()
      return self.getBoxModel(_recursion=True)
    if isinstance(self.__box_model__, BoxModel):
      return self.__box_model__
    e = typeMsg('__box_model__', self.__box_model__, BoxModel)
    raise TypeError(e)

  @align.GET
  def getAlignPolicy(self, **kwargs) -> Align:
    """Getter-function for the alignment policy of the widget. """
    if self.__align_policy__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__align_policy__ = self.__fallback_align__()
      return self.getAlignPolicy(_recursion=True)
    if isinstance(self.__align_policy__, Align):
      return self.__align_policy__
    e = typeMsg('__align_policy__', self.__align_policy__, Align)
    raise TypeError(e)

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation of the paint event. """
    box = self.getBoxModel()
    painter = QPainter()
    painter.begin(self, )
    rx, ry = box.cornerRadiusX, box.cornerRadiusY
    marginRect = Rect(painter.viewport())
    painter.setPen(self.emptyPen)
    painter.setBrush(box.marginColor.brush)
    painter.drawRoundedRect(marginRect.Q, rx, ry)
    borderRect = marginRect - box.marginShape
    painter.setBrush(box.borderColor.brush)
    painter.drawRoundedRect(borderRect.Q, rx, ry)
    paddingRect = borderRect - box.borderShape
    painter.setBrush(box.paddingColor.brush)
    painter.drawRoundedRect(paddingRect.Q, rx, ry)
    viewRect = paddingRect - box.paddingShape
    self.__painted_rect__ = viewRect
    self.paintContent(viewRect, painter)
    painter.end()

  def __init__(self, *args, ) -> None:
    for arg in args:
      if isinstance(arg, QWidget):
        QWidget.__init__(self, arg)
        break
    else:
      QWidget.__init__(self)
    QWidget.setMinimumSize(self, 32, 32)
    QWidget.setMouseTracking(self, True)

  def paintContent(self, rect: Rect, painter: QPainter) -> PaintJob:
    """This method must be implemented by subclasses. The rect parameter
    given is the area that is assigned to the visible content of the
    widget. """
    return rect, painter

  def initUi(self, ) -> None:
    """Subclasses may implement this method to hook into immediately
    before the widget is first shown. """
    self.setMinimumSize(32, 32)
