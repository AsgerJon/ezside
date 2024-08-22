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

  __iter_contents__ = None

  __folder_name__ = None

  folderName = Field()
  root = Field()
  absPath = Field()

  @staticmethod
  def getSchema() -> dict:
    """Returns the schema for the LoadResource class."""
    return {
        'margins'      : QMarginsF,
        'borders'      : QMarginsF,
        'paddings'     : QMarginsF,
        'corner_radius': QPointF,
        'padded_color' : QColor,
        'border_color' : QColor,
        'pen_color'    : QColor,
        'font_family'  : FontFamily,
        'font_size'    : int,
        'font_weight'  : FontWeight,
        'font_align'   : Align,
        'font_cap'     : FontCap
    }

  @staticmethod
  def encodeMargins(margins: QMarginsF) -> dict:
    """Encodes the margins to a dictionary."""
    return {
        'left'  : margins.left(),
        'top'   : margins.top(),
        'right' : margins.right(),
        'bottom': margins.bottom()
    }

  @staticmethod
  def decodeMargins(data: dict) -> QMarginsF:
    """Decodes the margins from a dictionary."""
    return QMarginsF(data['left'],
                     data['top'],
                     data['right'],
                     data['bottom'])

  @staticmethod
  def encodePointF(point: QPointF) -> dict:
    """Encodes the point to a dictionary."""
    return {
        'x': point.x(),
        'y': point.y()
    }

  @staticmethod
  def decodePointF(data: dict) -> QPointF:
    """Decodes the point from a dictionary."""
    return QPointF(data['x'], data['y'])

  @staticmethod
  def encodeColor(color: QColor) -> dict:
    """Encodes the color to a dictionary."""
    return {
        'red'  : color.red(),
        'green': color.green(),
        'blue' : color.blue(),
        'alpha': color.alpha()
    }

  @staticmethod
  def decodeColor(data: dict) -> QColor:
    """Decodes the color from a dictionary."""
    return QColor(data['red'],
                  data['green'],
                  data['blue'],
                  data.get('alpha', 255))

  @staticmethod
  def encodeFontFamily(family: FontFamily) -> str:
    """Encodes the font family to a string."""
    return family.name

  @staticmethod
  def decodeFontFamily(data: str) -> FontFamily:
    """Decodes the font family from a string."""
    return FontFamily(data)

  @staticmethod
  def encodeFontWeight(weight: FontWeight) -> str:
    """Encodes the font weight to a string."""
    return weight.name

  @staticmethod
  def decodeFontWeight(data: str) -> FontWeight:
    """Decodes the font weight from a string."""
    return FontWeight(data)

  @staticmethod
  def encodeAlign(align: Align) -> str:
    """Encodes the alignment to a string."""
    return align.name

  @staticmethod
  def decodeAlign(data: str) -> Align:
    """Decodes the alignment from a string."""
    return Align(data)

  @staticmethod
  def encodeFontCap(cap: FontCap) -> str:
    """Encodes the font cap to a string."""
    return cap.name

  @staticmethod
  def decodeFontCap(data: str) -> FontCap:
    """Decodes the font cap from a string."""
    return FontCap(data)

  @staticmethod
  def encodeData(data: dict) -> dict:
    """Encodes the data to a dictionary."""
    out = {}
    for key, value in data.items():
      if isinstance(value, QMarginsF):
        out[key] = LoadResource.encodeMargins(value)
      elif isinstance(value, QPointF):
        out[key] = LoadResource.encodePointF(value)
      elif isinstance(value, QColor):
        out[key] = LoadResource.encodeColor(value)
      elif isinstance(value, FontFamily):
        out[key] = LoadResource.encodeFontFamily(value)
      elif isinstance(value, FontWeight):
        out[key] = LoadResource.encodeFontWeight(value)
      elif isinstance(value, Align):
        out[key] = LoadResource.encodeAlign(value)
      elif isinstance(value, FontCap):
        out[key] = LoadResource.encodeFontCap(value)
      elif isinstance(value, str):
        if value.lower() == 'false':
          out[key] = False
        elif value.lower() == 'true':
          out[key] = True
        else:
          out[key] = value
      else:
        out[key] = value
    return out

  @staticmethod
  def decodeData(data: dict) -> dict:
    """Decodes the data from a dictionary."""
    out = {}
    for key, value in data.items():
      if isinstance(value, dict):
        if 'left' in value:
          out[key] = LoadResource.decodeMargins(value)
        elif 'x' in value:
          out[key] = LoadResource.decodePointF(value)
        elif 'red' in value:
          out[key] = LoadResource.decodeColor(value)
        else:
          out[key] = value
      elif isinstance(value, str):
        if value.lower() == 'false':
          out[key] = False
        elif value.lower() == 'true':
          out[key] = True
        else:
          out[key] = value
      else:
        out[key] = value
    return out

  @folderName.GET
  def _getFolderName(self) -> str:
    """Getter-function for the folder name"""
    return self.__folder_name__

  @root.GET
  def _getRootDirectory(self, ) -> str:
    """Returns path to root directory"""
    return self._getRoot()

  @absPath.GET
  def _getAbsolutePath(self, ) -> str:
    """Returns the absolute path to the resource directory."""
    return os.path.normpath(os.path.join(self.root, self.folderName))

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
  def getResourcePath(cls, *path: str) -> str:
    """Loads a directory from the resource directory."""
    root = cls._getRoot()
    return os.path.normpath(os.path.join(root, 'etc'))

  @classmethod
  def load(cls, *path: str) -> str:
    """Loads a file from the resource directory."""
    return os.path.normpath(os.path.join(cls.getResourcePath(), *path))

  def __init__(self, folderName: str = None) -> None:
    """Initializes the LoadResource object."""
    BaseObject.__init__(self)
    self.__folder_name__ = folderName

  def __iter__(self, ) -> Self:
    """Implementation of the iterator protocol. It iterates through the
    contents of the resource/folderName directory. """
    here = self.getResourcePath(self.folderName)
    self.__iter_contents__ = sorted([*os.listdir(here), ])
    return self

  def __next__(self, ) -> str:
    """Returns the path to the next item in the directory."""
    if self.__iter_contents__:
      out = os.path.join(self.absPath, self.__iter_contents__.pop(0))
      return os.path.normpath(out)
    raise StopIteration

  def __getitem__(self, key: str) -> Any:
    """Returns the path to the specified item in the directory."""
    value = self._searchKey(key)
    if os.path.exists(value):
      if os.path.isdir(value):
        return LoadResource(value)
      return value
    e = """The key: '%s' is associated with the item: '%s', but this 
    was not recognized as a file or directory!"""
    raise FileNotFoundError(monoSpace(e % (key, value)))

  def _searchKey(self, key: str) -> str:
    """Searches for an item matching the given key"""
    for item in self:
      if key in os.path.basename(item):
        return item
    for item in self:
      if key.lower() in os.path.basename(item).lower():
        return item
    for item in self:
      key2 = str(key.replace(' ', '')).replace('_', '').lower()
      item2 = item.replace(' ', '').replace('_', '').lower()
      if key2 in item2:
        return item
    raise KeyError(key)

  def loadJson(self, jsonFile: str) -> dict:
    """Loads the JSON file from the resource directory."""
    with open(self[jsonFile], 'r') as file:
      data = json.load(file)
    return self.decodeData(data)
