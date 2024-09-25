"""ImgEdit shows an image and allows edits. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TypeAlias, Union, Any

import numpy as np
import torch
from PIL import Image
from PySide6.QtCore import (QSizeF, QSize, QRectF, QPointF, Slot, Qt, Signal,
                            QRect, QTimer, QPoint)
from PySide6.QtGui import QPainter, QPixmap, QImage, \
  QColor, QContextMenuEvent, QPaintEvent, QBrush, QPointerEvent, QEventPoint
from icecream import ic
from torchvision.transforms import ToTensor, ToPILImage
from worktoy.desc import Field, AttriBox, THIS
from worktoy.parse import maybe
from worktoy.text import typeMsg

from ezside.dialogs import NewDialog
from ezside.base_widgets import AbstractButton
from ezside.style import Align
from ezside.tools import emptyPen
from ezside.widgets import ImgContextMenu

Rect: TypeAlias = Union[QRect, QRectF]
ic.configureOutput(includeContext=True)


class ImgEdit(AbstractButton):
  """ImgEdit shows an image and allows edits. """

  __fallback_paint_color__ = QColor(255, 255, 255, 255)
  __fallback_brush_radius__ = 5

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
  paintBrush = Field()
  paintCenter = Field()
  paintTensor = Field()
  mouseRegion = Field()
  imageTimer = Field()

  requestColor = Signal()
  requestFid = Signal()
  newFid = Signal(str)
  openFid = Signal(str)
  saveFid = Signal(str)

  def getAlignment(self) -> Align:
    """Getter-function for the alignment setting"""
    return Align.CENTER

  @imageTimer.GET
  def _getImageTimer(self, **kwargs) -> QTimer:
    """Getter-function for the image timer"""
    if self.__image_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__image_timer__ = QTimer()
      self.__image_timer__.setInterval(40)
      self.__image_timer__.setSingleShot(False)
      self.__image_timer__.setTimerType(Qt.TimerType.PreciseTimer)
      # self.__image_timer__.timeout.connect(self.updateImage)
      return self._getImageTimer(_recursion=True)
    if isinstance(self.__image_timer__, QTimer):
      return self.__image_timer__
    e = typeMsg('imageTimer', self.__image_timer__, QTimer)
    raise TypeError(e)

  @brushRadius.GET
  def _getBrushRadius(self) -> int:
    """Getter-function for brush radius"""
    return maybe(self.__brush_radius__, self.__fallback_brush_radius__)

  @brushRadius.SET
  def _setBrushRadius(self, brushRadius: int) -> None:
    """Setter-function for brush radius"""
    self.__brush_radius__ = brushRadius

  @fid.ONSET
  def _onFidSet(self, oldVal: str, newVal: str) -> None:
    """Hook to change in fid"""
    self.newFid.emit(newVal)

  @paintColor.GET
  def _getPaintColor(self) -> QColor:
    """Getter-function for paint color"""
    return maybe(self.__paint_color__, self.__fallback_paint_color__)

  @paintColor.SET
  def _setPaintColor(self, color: QColor) -> None:
    """Setter-function for paint color"""
    self.__paint_color__ = color

  @paintCenter.GET
  def _getPaintCenter(self) -> QPointF:
    """Getter-function for paint center"""
    topLeft = self.parentRect.topLeft()
    center = self.cursorPosition - topLeft
    R = self.brushRadius
    paintSize = self.requiredSize()
    W, H = paintSize.width(), paintSize.height()
    X, Y = center.x(), center.y()
    h, w = self.__data_tensor__.shape[1:]
    x, y = X * w / W, Y * h / H
    return QPointF(x, y)

  @paintTensor.GET
  def _getPaintTensor(self) -> torch.Tensor:
    """Getter-function for paint tensor"""
    center = QPointF.toPoint(self.paintCenter)
    w, h = self.__data_tensor__.shape[2], self.__data_tensor__.shape[1]
    r = self.brushRadius
    x, y = center.x(), center.y()
    x0, x1 = max(0, x - r), min(w, x + r)
    y0, y1 = max(0, y - r), min(h, y + r)
    x0, x1, y0, y1 = int(x0), int(x1), int(y0), int(y1)
    paintTensor = torch.zeros(3, y1 - y0, x1 - x0)
    paintTensor[0, :, :] = self.paintColor.red() / 255
    paintTensor[1, :, :] = self.paintColor.green() / 255
    paintTensor[2, :, :] = self.paintColor.blue() / 255
    return paintTensor

  @Slot(QColor)
  def setPaintColor(self, color: QColor) -> None:
    """Setter-slot for paint color"""
    self.__paint_color__ = color

  @paintBrush.GET
  def _getPaintBrush(self) -> QBrush:
    """Getter-function for paint brush"""
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    brush.setColor(self.paintColor)
    return brush

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
    self.update()
    self.openFid.emit(self.fid)

  @pix.GET
  def _getPix(self) -> QPixmap:
    """Getter-function for pixmap"""
    if self.__data_tensor__ is None:
      return QPixmap()
    pilImage = ToPILImage()(self.__data_tensor__)
    imgArray = np.array(pilImage)
    if pilImage.mode == "RGB":
      fmt = QImage.Format.Format_RGB888
    elif pilImage.mode == "RGBA":
      fmt = QImage.Format.Format_RGBA8888
    else:
      raise ValueError("Unsupported PIL image mode.")
    h, w, _ = imgArray.shape
    qImage = QImage(imgArray.data, w, h, imgArray.strides[0], fmt)
    return QPixmap.fromImage(qImage)

  @mouseRegion.GET
  def _getMouseRegion(self) -> QRectF:
    """Getter-function for mouse region"""
    return maybe(self.__mouse_region__, QRectF())

  @mouseRegion.SET
  def _setMouseRegion(self, mouseRegion: QRectF) -> None:
    """Setter-function for mouse region"""
    self.__mouse_region__ = mouseRegion

  #
  # def updateImage(self) -> None:
  #   """Updates the view"""
  #   oldSize = self.parentLayout.requiredSize()
  #   if self.__data_tensor__ is None:
  #     return
  #   pilImage = ToPILImage()(self.__data_tensor__)
  #   imageArray = np.array(pilImage)
  #   if pilImage.mode == "RGB":
  #     fmt = QImage.Format.Format_RGB888
  #   elif pilImage.mode == "RGBA":
  #     fmt = QImage.Format.Format_RGBA8888
  #   else:
  #     raise ValueError("Unsupported PIL image mode.")
  #   h, w, _ = imageArray.shape
  #   qImage = QImage(imageArray.data, w, h, imageArray.strides[0], fmt)
  #   self.__pix_map__ = QPixmap.fromImage(qImage)
  #   rect = QRectF(QPointF(0, 0), QSizeF(w, h))
  #   self.mouseRegion = rect - self.allMargins
  #   newSize = self.parentLayout.requiredSize()
  #   sizeIncrease = QSizeF.toSize(newSize - oldSize)
  #   self.parentLayout.resize(QSizeF.toSize(newSize))
  #   newWindowSize = self.mainWindow.size() + sizeIncrease
  #   self.mainWindow.resize(newWindowSize)
  #   self.parentLayout.adjustSize()

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

  def paintMeLike(self,
                  rect: Rect,
                  painter: QPainter,
                  event: QPaintEvent) -> Any:
    """Paint the image. """
    parent = AbstractButton.paintMeLike
    rect, painter, event = parent(self, rect, painter, event)

    center = rect.center()
    innerRect = rect - self.allMargins
    innerRect.moveCenter(center)
    self.mouseRegion = innerRect
    painter.drawPixmap(innerRect.topLeft(), self.pix)
    if self.underMouse:
      painter.setPen(emptyPen())
      painter.setBrush(self.paintBrush)
      center, radius = self.cursorPosition, self.brushRadius
      painter.drawEllipse(center, radius, radius)
    return rect, painter, event

  def __init__(self, *args, **kwargs) -> None:
    AbstractButton.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)

  def initSignalSlot(self) -> None:
    """Initializes the signal-slot connections. """
    AbstractButton.initSignalSlot(self)
    self.imageTimer.timeout.connect(self.update)
    self.imageTimer.start()

  def contextMenuEvent(self, event: QContextMenuEvent) -> None:
    """Right-click should open tool options"""
    self.contextMenu.popup(event.globalPos(), )

  def newImage(self, size: QSize, fid: str = None) -> None:
    """Slot creates a new image. """
    self.__data_tensor__ = torch.ones(3, size.height(), size.width())
    if fid is None:
      here = os.path.abspath(os.path.dirname(__file__))
      root = os.path.normpath(os.path.join(here, "..", ".."))
      fid = os.path.join(root, "unnamed.png")
    self.fid = fid
    self.update()

  @Slot(NewDialog)
  def fromDialog(self, newDialog: NewDialog) -> None:
    """Creates a new image from the wizard. """
    self.newImage(QSize(newDialog.width, newDialog.height),
                  newDialog.fileName)

  def applyBrush(self, ) -> None:
    """Apply the brush to the image. """
    center = QPointF.toPoint(self.paintCenter)
    w, h = self.__data_tensor__.shape[2], self.__data_tensor__.shape[1]
    r = self.brushRadius
    x, y = center.x(), center.y()
    x0, x1 = max(0, x - r), min(w, x + r)
    y0, y1 = max(0, y - r), min(h, y + r)
    x0, x1, y0, y1 = int(x0), int(x1), int(y0), int(y1)
    x0, x1 = max(0, x - r), min(w, x + r)
    y0, y1 = max(0, y - r), min(h, y + r)
    self.__data_tensor__[:, y0:y1, x0:x1] = self.paintTensor

  def handleMouseMove(self, pointerEvent: QPointerEvent) -> bool:
    """Handle mouse move. """
    if self.pressedButton == Qt.MouseButton.LeftButton:
      eventPoint = QPointerEvent.point(pointerEvent, 0)
      self.__cursor_position__ = QEventPoint.position(eventPoint)
      self.applyBrush()
    return AbstractButton.handleMouseMove(self, pointerEvent)
