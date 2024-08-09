"""IconParser obtains a QIcon for a named action and returns it as a QIcon
or as QPixmap. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

import torch
from PIL import Image
from PySide6.QtGui import QIcon, QPixmap, QImage
from torch import Tensor
from torchvision.transforms.v2 import ToTensor
from worktoy.desc import Field
from worktoy.text import stringList

from ezside.parser import AbstractParser


class IconParser(AbstractParser):
  """IconParser obtains a QIcon for a named action and returns it as a QIcon
  or as QPixmap. """

  __fallback_name__ = 'risitas'
  __icon_name__ = None
  __data_tensor__ = None

  @classmethod
  def _getRoot(cls, here: str = None) -> str:
    """Returns path to root directory"""
    if here is None:
      here = os.path.dirname(os.path.abspath(__file__))
    items = os.listdir(here)
    rootItems = stringList("""src, README.md ,LICENSE""")
    for item in rootItems:
      if item not in items:
        parentDir = cls._getRoot(os.path.join(here, '..'))
        return cls._getRoot(os.path.normpath(parentDir))
    else:
      return here

  @classmethod
  def getIconPath(cls, e: str = None) -> str:
    """Returns the icon directory path"""
    if e is not None:
      if not os.path.isabs(e):
        e = """Encountered bad path: '%s'!""" % e
        raise ValueError(e)
      if not os.path.exists(e):
        e = """While searching for icon directory '%s' was reached, 
        which does not exist!"""
        raise FileNotFoundError(e)
      if os.path.isfile(e):
        e = """While searching for icon directory '%s' was reached, 
        which is a file!"""
        raise NotADirectoryError(e)
      raise RecursionError

    iconPath = cls._getRoot()
    for directory in stringList("""src, ezside, app, icons"""):
      iconPath = os.path.join(iconPath, directory)
      iconPath = os.path.normpath(iconPath)
      if not os.path.exists(iconPath):
        return cls.getIconPath(iconPath)
    return iconPath

  name = Field()
  file = Field()
  icon = Field()
  pix = Field()
  img = Field()
  data = Field()
  pil = Field()

  def __init__(self, name: str) -> None:
    """Initializes the parser on the name of the icon."""
    AbstractParser.__init__(self)
    self.__icon_name__ = name

  @name.GET
  def _getIconName(self) -> str:
    """Getter-function for the icon name."""
    if self.__icon_name__ is None:
      return self.__fallback_name__
    return self.__icon_name__

  @name.SET
  def _setIconName(self, newName: str) -> None:
    """Setter-function for the icon name."""
    self.__icon_name__ = newName

  @file.GET
  def _getFile(self) -> str:
    """Getter-function for the file."""
    iconPath = self.getIconPath()
    for item in os.listdir(iconPath):
      if self.name in item:
        iconFile = os.path.join(iconPath, item)
        if os.path.isfile(iconFile):
          return iconFile
    return os.path.join(iconPath, '%s.png' % self.__fallback_name__)

  @pix.GET
  def _getPix(self) -> QPixmap:
    """Getter-function for the pixmap."""
    return QPixmap(self.file)

  @icon.GET
  def _getIcon(self) -> QIcon:
    """Getter-function for the icon."""
    return QIcon(self.pix)

  @img.GET
  def _getImg(self) -> QImage:
    """Getter-function for the image."""
    return QPixmap.toImage(self.pix)

  @pil.GET
  def _getPilImage(self) -> Image:
    """Getter-function for the PIL image."""
    return Image.fromqpixmap(self.pix)

  @data.GET
  def _getData(self, **kwargs) -> Tensor:
    """Getter-function for the data."""
    return ToTensor()(self.pil)
