"""The icons module provides a collection of icons for use in the
application. The icons are provided as a dictionary with the icon name
as the key and the icon path as the value."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import Any

from PIL import Image


class _Icon:
  __inner_image__ = None

  def __init__(self, img: Any) -> None:
    self.__inner_image__ = img

  def __get__(self, instance: object, owner: Any) -> Image:
    if instance is None:
      return self.__inner_image__
    raise AttributeError(
      "Icon is a class attribute, not an instance attribute!")


class IconMeta(type):
  """The IconMeta metaclass is used to create the Icons class. The Icons
  class is a dictionary of icon names and their respective paths."""

  @staticmethod
  def _getIconPath() -> str:
    """Returns the path to the icon folder."""
    fileDir = os.path.join(os.path.dirname(__file__), '../')
    iconPath = os.path.join(fileDir, 'ezqt', 'windows', 'menus', 'icons', )
    return os.path.normpath(iconPath)

  @classmethod
  def __prepare__(mcls, name: str, bases: str, **kwargs):
    """Creates the dictionary for the Icons class."""
    iconPath = mcls._getIconPath()
    iconList = os.listdir(iconPath)
    namespace = {}
    for icon in iconList:
      if not icon.endswith('.png'):
        continue
      name, ext = os.path.splitext(icon)
      im = Image.open(icon)
      namespace[name] = Image.Image.load(im)
    return namespace


class Icons(IconMeta):
  """The icons module provides a collection of icons for use in the
  application. The icons are provided as a dictionary with the icon name
  as the key and the icon path as the value."""
