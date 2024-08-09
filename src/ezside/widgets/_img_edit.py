"""ImgEdit shows an image and allows edits. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TypeAlias, Union

import numpy as np
import torch
from PIL import Image
from PySide6.QtCore import (QSizeF, QSize, QRectF, QPointF, Slot, QEvent,
                            Qt, Signal, QRect, QTimer)
from PySide6.QtGui import QPainter, QPixmap, QImage, \
  QMouseEvent, QEnterEvent, QColor, QContextMenuEvent
from PySide6.QtWidgets import QMenu
from icecream import ic
from torchvision.transforms import ToTensor, ToPILImage
from worktoy.desc import Field, AttriBox, THIS
from worktoy.parse import maybe
from worktoy.text import typeMsg

from ezside.dialogs import NewDialog
from ezside.basewidgets import BoxWidget
from ezside.widgets import ImgContextMenu

Rect: TypeAlias = Union[QRect, QRectF]
ic.configureOutput(includeContext=True)


class ImgEdit(BoxWidget):
  """ImgEdit shows an image and allows edits. """

  __inner_file__ = None
  __data_tensor__ = None
  __pix_map__ = None
  __left_mouse_pressed__ = None
  __under_mouse__ = None
  __paint_color__ = None
  __mouse_region__ = None
  __brush_radius__ = None
  __image_timer__ = None

  contextMenu = AttriBox[ImgContextMenu](THIS)

  brushRadius = Field()
  pix = Field()
  fid = Field()
  data = Field()
  paintColor = Field()
  leftMouse = Field()
  mouseRegion = Field()
  imageTimer = Field()

  requestColor = Signal()
  requestFid = Signal()
  newFid = Signal(str)
  openFid = Signal(str)
  saveFid = Signal(str)

  @imageTimer.GET
  def _getImageTimer(self, **kwargs) -> QTimer:
    """Getter-function for the image timer"""
    if self.__image_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__image_timer__ = QTimer()
      self.__image_timer__.setInterval(10)
      self.__image_timer__.setSingleShot(True)
      self.__image_timer__.setTimerType(Qt.TimerType.PreciseTimer)
      self.__image_timer__.timeout.connect(self.updateImage)
      return self._getImageTimer(_recursion=True)
    if isinstance(self.__image_timer__, QTimer):
      return self.__image_timer__
    e = typeMsg('imageTimer', self.__image_timer__, QTimer)
    raise TypeError(e)

  @brushRadius.GET
  def _getBrushRadius(self) -> int:
    """Getter-function for brush radius"""
    return self.__brush_radius__

  @brushRadius.SET
  def _setBrushRadius(self, brushRadius: int) -> None:
    """Setter-function for brush radius"""
    self.__brush_radius__ = brushRadius

  @fid.ONSET
  def _onFidSet(self, oldVal: str, newVal: str) -> None:
    """Hook to change in fid"""
    self.newFid.emit(newVal)

  @leftMouse.GET
  def _getLeftMouse(self) -> bool:
    """Getter-function for left mouse"""
    return self.__left_mouse_pressed__

  @paintColor.GET
  def _getPaintColor(self) -> QColor:
    """Getter-function for paint color"""
    return maybe(self.__paint_color__, QColor(0, 0, 0, ))

  @Slot(QColor)
  def setPaintColor(self, color: QColor) -> None:
    """Setter-slot for paint color"""
    self.__paint_color__ = color

  @Slot(str)
  def openImage(self, fid: str) -> None:
    """Slot opens the given image. """
    self.fid = fid
    image = Image.open(fid).convert("RGB")
    aspectRatio = image.size[0] / image.size[1]
    if aspectRatio < 1:
      image = image.resize((256, int(256 / aspectRatio)), )
    else:
      image = image.resize((int(256 * aspectRatio), 256), )
    transform = ToTensor()
    self.__data_tensor__ = transform(image)
    ic(self.__data_tensor__.shape)
    self.updateImage()
    self.openFid.emit(self.fid)

  @pix.GET
  def _getPix(self) -> QPixmap:
    """Getter-function for pixmap"""
    return self.__pix_map__ or QPixmap()

  @mouseRegion.GET
  def _getMouseRegion(self) -> QRectF:
    """Getter-function for mouse region"""
    return maybe(self.__mouse_region__, QRectF())

  @mouseRegion.SET
  def _setMouseRegion(self, mouseRegion: QRectF) -> None:
    """Setter-function for mouse region"""
    self.__mouse_region__ = mouseRegion

  def updateImage(self) -> None:
    """Updates the view"""
    oldSize = self.parentLayout.requiredSize()
    if self.__data_tensor__ is None:
      return
    pilImage = ToPILImage()(self.__data_tensor__)
    imageArray = np.array(pilImage)
    if pilImage.mode == "RGB":
      fmt = QImage.Format.Format_RGB888
    elif pilImage.mode == "RGBA":
      fmt = QImage.Format.Format_RGBA8888
    else:
      raise ValueError("Unsupported PIL image mode.")
    h, w, _ = imageArray.shape
    qImage = QImage(imageArray.data, w, h, imageArray.strides[0], fmt)
    self.__pix_map__ = QPixmap.fromImage(qImage)
    rect = QRectF(QPointF(0, 0), QSizeF(w, h))
    self.mouseRegion = rect - self.allMargins
    newSize = self.parentLayout.requiredSize()
    sizeIncrease = QSizeF.toSize(newSize - oldSize)
    self.parentLayout.resize(QSizeF.toSize(newSize))
    newWindowSize = self.mainWindow.size() + sizeIncrease
    self.mainWindow.resize(newWindowSize)
    self.parentLayout.adjustSize()

  @Slot(str)
  def saveImage(self, fid: str) -> None:
    """Slot saves the image to the file. """
    self.fid = fid
    if self.fid is None or os.path.basename(self.fid) == "unnamed.png":
      return self.requestFid.emit()
    self.pix.save(self.fid)
    self.saveFid.emit(self.fid)

  @Slot(str)
  def saveAsImage(self, fid: str = None) -> None:
    """Slot saves the image to the given file. """
    if fid is None:
      if self.fid is None:
        return self.requestFid.emit()
      self.pix.save(self.fid)
    self.fid = fid
    self.pix.save(fid)

  @fid.GET
  def _getFid(self, **kwargs) -> str:
    """Return the file path. """
    return self.__inner_file__

  @fid.SET
  def _setFid(self, fid: str) -> None:
    """Set the file path. """
    self.__inner_file__ = fid

  def requiredSize(self) -> QSizeF:
    """Return the required size. """
    if not self.pix:
      return QSizeF(256, 256)
    return self.pix.size()

  def paintMeLike(self, rect: Rect, painter: QPainter) -> None:
    """Paint the image. """
    BoxWidget.paintMeLike(self, rect, painter)
    if not self.pix:
      return
    viewRect = rect
    center = viewRect.center()
    pixSize = QPixmap.size(self.pix)
    pixRect = QRectF(QPointF(0, 0), QSize.toSizeF(pixSize))
    pixRect.moveCenter(center)
    innerRect = viewRect - self.margins
    innerRect -= self.borders
    innerRect -= self.paddings
    innerRect.moveCenter(center)
    self.mouseRegion = innerRect
    painter.drawPixmap(innerRect.topLeft(), self.pix)

  def __init__(self, *args) -> None:
    BoxWidget.__init__(self, *args)
    self.setMouseTracking(True)
    self.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)

  def contextMenuEvent(self, event: QContextMenuEvent) -> None:
    """Right-click should open tool options"""
    self.contextMenu.popup(event.globalPos(), )

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Sets the mouse down flag"""
    if event.buttons() == Qt.MouseButton.LeftButton:
      self.__left_mouse_pressed__ = True
      if not self.imageTimer.isActive():
        self.imageTimer.start()
    if event.buttons() == Qt.MouseButton.RightButton:
      contextEvent = QContextMenuEvent(QContextMenuEvent.Reason.Mouse,
                                       event.pos())
      self.contextMenuEvent(contextEvent)

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Sets the mouse down flag"""
    self.__left_mouse_pressed__ = False
    if self.imageTimer.isActive():
      self.imageTimer.stop()

  def enterEvent(self, event: QEnterEvent) -> None:
    """Sets the under mouse flag"""
    self.__under_mouse__ = True

  def leaveEvent(self, event: QEvent) -> None:
    """Sets the under mouse flag"""
    self.__under_mouse__ = False
    self.__left_mouse_pressed__ = False

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Applies paint when mouse button held"""
    if self.__data_tensor__ is None:
      return
    p = event.pos()
    x, y = p.x(), p.y()
    width, height = self.pix.size().width(), self.pix.size().height()
    j0 = int(x / width * self.__data_tensor__.shape[2])
    i0 = int(y / height * self.__data_tensor__.shape[1])

    rgb = self.paintColor
    if rgb is None:
      self.contextMenu.popup(event.globalPos(), )
      return
    r, g, b = float(rgb.red()), float(rgb.green()), float(rgb.blue())
    r, g, b = r / 255, g / 255, b / 255
    if self.leftMouse:
      for ii in range(-5, 5):
        for jj in range(-5, 5):
          if i0 + ii < 0 or i0 + ii >= self.__data_tensor__.shape[1]:
            continue
          if ii * ii + jj * jj < 25:
            r0 = self.__data_tensor__[0, i0 + ii, j0 + jj]
            g0 = self.__data_tensor__[1, i0 + ii, j0 + jj]
            b0 = self.__data_tensor__[2, i0 + ii, j0 + jj]
            self.__data_tensor__[0, i0 + ii, j0 + jj] = 0.75 * r0 + 0.25 * r
            self.__data_tensor__[1, i0 + ii, j0 + jj] = 0.75 * g0 + 0.25 * g
            self.__data_tensor__[2, i0 + ii, j0 + jj] = 0.75 * b0 + 0.25 * b
    if not self.imageTimer.isActive():
      self.imageTimer.start()

  def newImage(self, size: QSize, fid: str = None) -> None:
    """Slot creates a new image. """
    self.__data_tensor__ = torch.ones(3, size.height(), size.width())
    if fid is None:
      here = os.path.abspath(os.path.dirname(__file__))
      root = os.path.normpath(os.path.join(here, "..", ".."))
      fid = os.path.join(root, "unnamed.png")
    self.fid = fid
    self.updateImage()

  @Slot(NewDialog)
  def fromDialog(self, newDialog: NewDialog) -> None:
    """Creates a new image from the wizard. """
    self.newImage(QSize(newDialog.width, newDialog.height),
                  newDialog.fileName)
