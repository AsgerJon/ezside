"""IconParser obtains a QIcon for a named action and returns it as a QIcon
or as QPixmap. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

import torch
from PIL import Image
from PySide6.QtGui import QIcon, QPixmap, QImage
from PySide6.QtWidgets import QLabel
from icecream import ic
from torch import Tensor
from torchvision.transforms.v2 import ToTensor
from worktoy.desc import Field
from worktoy.text import stringList

from ezside.parser import AbstractParser
from ezside.tools import LoadResource

ic.configureOutput(includeContext=True)


class IconParser(AbstractParser):
  """IconParser obtains a QIcon for a named action and returns it as a QIcon
  or as QPixmap. """

  __fallback_name__ = 'risitas'
  __icon_name__ = None
  __icon_path__ = None
  __load_resource__ = None

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, str):
        self.__icon_name__ = arg
        break
    else:
      self.__icon_name__ = self.__fallback_name__
    self.__load_resource__ = LoadResource('icons')

  def getLoadResource(self) -> LoadResource:
    """Returns the resource loader."""
    return self.__load_resource__

  def getIconFile(self) -> str:
    """Returns the icon file name."""
    iconPath = self.getLoadResource().getFilePath(self.__icon_name__)
    if iconPath is None:
      iconPath = self.getLoadResource().getFilePath(self.__fallback_name__)
    ic(iconPath)
    return iconPath

  def getIconPath(self, ) -> str:
    """Returns the icon directory path."""
    return self.__load_resource__.getContentPath()

  def getQPixmap(self) -> QPixmap:
    """Returns the icon as a QPixmap."""
    iconFile = self.getIconFile()
    pix = QPixmap()
    QPixmap.load(pix, iconFile)
    return pix

  def getQIcon(self) -> QIcon:
    """Getter-function for QIcon"""
    pix = self.getQPixmap()
    ic(pix.size())
    return QIcon(pix)
