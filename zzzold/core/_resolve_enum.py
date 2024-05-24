"""The parseEnum function parses the name or value of a Qt Enum. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from enum import EnumType
from typing import Any

from vistutils.waitaminute import typeMsg


def _resolveEnumNamesValues(enumType: EnumType, nameVal: int | str) -> Any:
  """The parseEnum function parses the name or value of a Qt Enum. """
  for key, val in enumType:
    if isinstance(nameVal, str):
      if nameVal.lower() == key.lower():
        return val
    elif isinstance(nameVal, int):
      if nameVal == val.value:
        return val


def _resolveEnumInstances(enumType: EnumType, *args, ) -> Any:
  """This method parses the positional arguments and returns the first
  such argument of the given type."""
  for arg in args:
    if isinstance(arg, enumType):
      return arg


def resolveEnum(enumType: EnumType, *args, ) -> Any:
  """The parseEnum function parses the name or value of a Qt Enum. """
  out = _resolveEnumInstances(enumType, *args)
  if out is not None:
    if isinstance(out, enumType):
      return out
    e = typeMsg('out', out, enumType)
    raise TypeError(e)
  out = _resolveEnumNamesValues(enumType, *args)
  intArgs, strArgs = [], []
  for arg in args:
    if isinstance(arg, int):
      intArgs.append(arg)
    elif isinstance(arg, str):
      strArgs.append(arg)
    for item in enumType:
      if item.name in strArgs or item.value in intArgs:
        return item
