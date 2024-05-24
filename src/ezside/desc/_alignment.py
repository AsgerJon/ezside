"""Alignment implements descriptor protocols for horizontal and vertical
alignment flags. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from ezside.app import EZObject, MissingSettingsError
from ezside.desc import SettingsDescriptor, AlignFlag, AlignLeft
from ezside.desc import AlignRight, AlignHCenter, AlignTop, AlignBottom
from ezside.desc import AlignVCenter, AlignCenter


def parseAlignFlag(*args) -> AlignFlag:
  """Parses the alignment flag."""
  for arg in args:
    if isinstance(arg, AlignFlag):
      return arg
    if isinstance(arg, (str, int)):
      for item in AlignFlag:
        if isinstance(arg, int):
          if item.value == arg:
            return item
        if isinstance(arg, str):
          if item.name.lower() == arg.lower():
            return item


HAlignFlags = [AlignLeft, AlignRight, AlignHCenter, AlignCenter]
VAlignFlags = [AlignTop, AlignBottom, AlignVCenter, AlignCenter]


class HAlign(SettingsDescriptor):
  """The 'HAlign' class provides horizontal alignment flags. """

  def getContentClass(self) -> type:
    """Returns the content class."""
    return AlignFlag

  def create(self, instance: EZObject, owner: type, **kwargs) -> AlignFlag:
    """Create the content."""
    parsedValue = parseAlignFlag(*self.getArgs())
    if isinstance(parsedValue, AlignFlag):
      if parsedValue in HAlignFlags:
        if parsedValue == AlignCenter:
          return AlignHCenter
        return parsedValue
    raise MissingSettingsError(self.__class__.__name__)


class VAlign(SettingsDescriptor):
  """The 'VAlign' class provides vertical alignment flags. """

  def getContentClass(self) -> type:
    """Returns the content class."""
    return AlignFlag

  def create(self, instance: EZObject, owner: type, **kwargs) -> AlignFlag:
    """Create the content."""
    parsedValue = parseAlignFlag(*self.getArgs())
    if isinstance(parsedValue, AlignFlag):
      if parsedValue in VAlignFlags:
        if parsedValue == AlignCenter:
          return AlignVCenter
        return parsedValue
    key = '%s/alignment/vertical' % instance.settingsId
    return self.settings.value(key)

  def getFallbackValues(self) -> dict[str, Any]:
    """Returns the fallback values."""
    return {
      'normal/vertical/alignment': AlignTop,
    }
