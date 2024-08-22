"""LoadResource provides a common interface for retrieving assets from the
resource directory. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import json
import os
from typing import Self, Any

from PySide6.QtCore import QPointF, QMarginsF
from PySide6.QtGui import QColor
from worktoy.desc import Field
from worktoy.meta import BaseObject
from worktoy.text import stringList, monoSpace

from ezside.tools import FontFamily, FontWeight, Align, FontCap


class LoadResource(BaseObject):
  """LoadResource provides a common interface for retrieving assets from the
  resource directory. """

  __content_path__ = None

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
  def getResourcePath(cls) -> str:
    """Loads a directory from the resource directory."""
    root = cls._getRoot()
    return os.path.normpath(os.path.join(root, 'etc'))

  def __init__(self, *path) -> None:
    """Initializes the resource loader."""
    BaseObject.__init__(self)
    resPath = self.getResourcePath()
    self.__content_path__ = os.path.normpath(os.path.join(resPath, *path))

  def getContentPath(self) -> str:
    """Getter-function for the content path"""
    return self.__content_path__

  def getFilePath(self, name: str) -> str:
    """Getter-function for named item in the content path"""
    for item in os.listdir(self.__content_path__):
      item2 = item.lower()
      item2 = item2.replace(' ', '')
      item2 = item2.replace('_', '')
      name2 = name.lower()
      name2 = name2.replace(' ', '')
      name2 = name2.replace('_', '')
      if name2 in item2:
        namedPath = os.path.join(self.__content_path__, item)
        return os.path.normpath(namedPath)
