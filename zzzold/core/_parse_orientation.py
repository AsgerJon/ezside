"""This file provides orientation parsers."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from ezside.core import ORIENTATION, HORIZONTAL, VERTICAL


def _parseKwargs(**kwargs) -> dict[ORIENTATION, Optional[bool]]:
  """Parses keyword arguments. Words found are set to True, otherwise
  left at None"""
  hKeys = stringList("""horizontal, h, hor, x""")
  vKeys = stringList("""vertical, v, ver, y""")
  out = {HORIZONTAL: None, VERTICAL: None}
  KEYS = [hKeys, vKeys]
  for (orientation, keys) in zip(ORIENTATION, KEYS):
    for key in keys:
      if key in kwargs:
        val = kwargs.get(key)
        if isinstance(val, bool):
          out[orientation] = val
          break
        e = typeMsg(key, val, bool)
        raise TypeError(e)
  return out


def _parseEnum(*args) -> dict[ORIENTATION, Optional[bool]]:
  """Parses positional arguments. Enum values found are set to True,
  otherwise left at None"""
  return {
    HORIZONTAL: True if HORIZONTAL in args else None,
    VERTICAL  : True if VERTICAL in args else None
  }


def _parseStr(*args) -> dict[ORIENTATION, Optional[bool]]:
  """Parses positional arguments. Words found are set to True, otherwise
  left at None"""
  hName, vName = 'horizontal', 'vertical'
  hFlag, vFlag = None, None
  for arg in args:
    if isinstance(arg, str):
      if arg.lower() == hName and hFlag is None:
        hFlag = True
      elif arg.lower() == vName and vFlag is None:
        vFlag = True
  return {HORIZONTAL: hFlag, VERTICAL: vFlag}


def parseOrientation(*args, **kwargs) -> ORIENTATION:
  """Parses positional and keyword arguments returning the first received
  instance of ORIENTATION."""
  orientationKwargs = _parseKwargs(**kwargs)
  orientationEnum = _parseEnum(*args)
  orientationStr = _parseStr(*args)
  data = [orientationKwargs, orientationEnum, orientationStr]
  for orientation in data:
    for key, val in orientation.items():
      if val:
        return key
