"""ImgEdit shows an image and allows edits. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

import numpy as np
import torch
from PIL import Image
from PIL.ImageQt import QImage as QImagePIL
from PySide6.QtCore import QSizeF, QSize, QRectF, QPointF, Slot, QRect, \
  QEvent, Qt, Signal
from PySide6.QtGui import QPaintEvent, QPainter, QPixmap, QImage, \
  QMouseEvent, QEnterEvent, QColor
from PySide6.QtWidgets import QWidget
from icecream import ic
from torchvision.transforms import ToTensor, ToPILImage

from worktoy.desc import Field
from worktoy.parse import maybe
from worktoy.text import monoSpace

from ezside.dialogs import NewDialog
from ezside.tools import SizeRule
from ezside.widgets import BoxWidget

ic.configureOutput(includeContext=True)


class ImgEdit(BoxWidget):
  """ImgEdit shows an image and allows edits. """

  __inner_file__ = None
  __data_tensor__ = None
  __pix_map__ = None
  __left_mouse_pressed__ = None
  __under_mouse__ = None
  __paint_color__ = None

  pix = Field()
  fid = Field()
  data = Field()
  paintColor = Field()
  leftMouse = Field()

  requestColor = Signal()
  requestFid = Signal()
  newFid = Signal(str)
  openFid = Signal(str)
  saveFid = Signal(str)

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
    image = image.resize((256, 256), )
    transform = ToTensor()
    self.__data_tensor__ = transform(image)
    self.updateImage()
    self.openFid.emit(self.fid)

  @pix.GET
  def _getPix(self) -> QPixmap:
    """Getter-function for pixmap"""
    return self.__pix_map__ or QPixmap()

  def updateImage(self) -> None:
    """Updates the view"""
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
    self.update()
    self.adjustSize()
    self.update()
    self.setMinimumSize(self.pix.size())
    self.parent().adjustSize()
    self.parent().update()
    self.parent().parent().adjustSize()
    self.parent().parent().update()
    self.parent().parent().parent().adjustSize()
    self.parent().parent().parent().update()
    parentSize = self.parent().parent().parent().size()
    self.parent().parent().parent().setMinimumSize(parentSize)

  @Slot()
  def saveImage(self, ) -> None:
    """Slot saves the image to the file. """
    ic(os.path.basename(self.fid))
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
    return self.pix.size()

  def contentRect(self) -> QSizeF:
    """Return the content rectangle. """
    return self.requiredSize() + self.paddings

  def minimumSizeHint(self) -> QSize:
    """Return the minimum size hint. """
    return QPixmap.size(self.pix)

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paint the image. """
    BoxWidget.paintEvent(self, event)
    if not self.pix:
      return
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    center = viewRect.center()
    pixSize = QPixmap.size(self.pix)
    pixRect = QRectF(QPointF(0, 0), QSize.toSizeF(pixSize))
    pixRect.moveCenter(center)
    innerRect = QRect.toRectF(viewRect) - self.margins
    innerRect -= self.borders
    innerRect -= self.paddings
    innerRect.moveCenter(center)
    painter.drawPixmap(QPointF(0, 0, ), self.pix)
    painter.end()

  def __init__(self, parent: QWidget = None) -> None:
    BoxWidget.__init__(self, parent)
    self.sizeRule = SizeRule.EXPAND
    self.setMouseTracking(True)

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Sets the mouse down flag"""
    if event.buttons() == Qt.MouseButton.LeftButton:
      ic('left mouse!')
      self.__left_mouse_pressed__ = True
    ic(self.__data_tensor__.shape)

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Sets the mouse down flag"""
    self.__left_mouse_pressed__ = False

  def enterEvent(self, event: QEnterEvent) -> None:
    """Sets the under mouse flag"""
    self.__under_mouse__ = True

  def leaveEvent(self, event: QEvent) -> None:
    """Sets the under mouse flag"""
    self.__under_mouse__ = False
    self.__left_mouse_pressed__ = False

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Applies paint when mouse button held"""
    x, y = int(event.localPos().x()), int(event.localPos().y())
    i = int(y / self.width() * self.__data_tensor__.shape[2])
    j = int(x / self.height() * self.__data_tensor__.shape[1])

    i = min(max(0, i), self.__data_tensor__.shape[2] - 1)
    j = min(max(0, j), self.__data_tensor__.shape[1] - 1)

    rgb = self.paintColor
    r, g, b = float(rgb.red()), float(rgb.green()), float(rgb.blue())
    r, g, b = r / 255, g / 255, b / 255
    if self.leftMouse:
      self.__data_tensor__[0, i - 2:i + 2, j - 2:j + 2] = r
      self.__data_tensor__[1, i - 2:i + 2, j - 2:j + 2] = g
      self.__data_tensor__[2, i - 2:i + 2, j - 2:j + 2] = b
      self.updateImage()

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
