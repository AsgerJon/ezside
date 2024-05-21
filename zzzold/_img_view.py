"""ImgView subclasses the CanvasWidget and provides a widget for displaying
images. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os.path
from typing import Any

from PySide6.QtCore import QPointF, QPoint, QMargins
from PySide6.QtGui import QImage, QPixmap

from ezside.core import KeepAspect, SMOOTH
from ezside.widgets import CanvasWidget, GraffitiVandal


class ImgView(CanvasWidget):
  """ImgView subclasses the CanvasWidget and provides a widget for displaying
  images. """

  __inner_image__ = None
  __image_file__ = None

  def __init__(self, *args, **kwargs) -> None:
    CanvasWidget.__init__(self, *args, **kwargs)
    if kwargs.get('icon', None) is not None:
      self.setIcon(kwargs['icon'])
    self.setMinimumSize(32, 32)

  def setImageURL(self, key: str, url: str = None) -> None:
    """Sets the image to the image at the given key. If no URL is
    specified, the key is expected to point to a cached image. """
    raise NotImplementedError

  def setImageFile(self, filePath: str, **kwargs) -> None:
    """Sets the image to the image at the given key. The image is loaded
    from the file path. """
    if not os.path.isabs(filePath):
      if kwargs.get('_recursion', False):
        raise RecursionError
      cachedDir = self.getAppSettings().getCachedDir()
      newPath = os.path.join(cachedDir, filePath)
      return self.setImageFile(newPath, _recursion=True)
    if not os.path.exists(filePath):
      raise FileNotFoundError(filePath)
    if os.path.isdir(filePath):
      raise IsADirectoryError(filePath)
    self.__image_file__ = filePath

  def setIcon(self, iconName: str) -> None:
    """Sets the image to the named icon. """
    iconFolder = self.getAppSettings().iconFolder()
    iconPath = os.path.join(iconFolder, iconName)
    if iconPath[-4:] != '.png':
      iconPath += '.png'
    self.setImageFile(iconPath)

  def getImage(self, ) -> QImage:
    """Returns the image file path. """
    return QImage(self.__image_file__)

  def getPixMap(self, ) -> QPixmap:
    """Returns the image file path. """
    return QPixmap(self.__image_file__)

  def customPaint(self, painter: GraffitiVandal) -> None:
    """Paints the image on the widget. """
    viewRect = painter.viewport()
    viewSize = viewRect.size()
    pix = self.getPixMap()
    pixSize = pix.size()
    painter.drawPixmap(viewRect, pix.scaled(viewSize, KeepAspect, SMOOTH))

  def defaultStyles(self, name: str) -> Any:
    """The defaultStyles method provides the default values for the
    styles."""
    if name == 'radius':
      return QPointF(0, 0)
    if name == 'borders':
      return QMargins(0, 0, 0, 0)
