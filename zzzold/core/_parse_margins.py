"""The parseMargins functions parses positional arguments and keyword
arguments returning the first received instance of QMargins or QMarginsF."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Union, Optional

from PySide6.QtCore import QMargins, QMarginsF
from icecream import ic
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

Margins = Union[QMargins, QMarginsF]

ic.configureOutput(includeContext=True)


def _parseKeyMargins(**kwargs) -> tuple[Optional[Margins], dict]:
  """Parses keyword arguments for instances of QMargins or QMarginsF."""
  marginsKey = stringList("""margins, margin, marginsF, marginF""")
  for key in marginsKey:
    if key in kwargs:
      val = kwargs.get(key)
      if isinstance(val, (QMargins, QMarginsF)):
        data = {k: v for (k, v) in kwargs.items() if k != key}
        return val, data
      e = typeMsg(key, val, QMargins)
      raise TypeError(e)
  return None, kwargs


def _parsePosMargins(*args, ) -> tuple[Optional[Margins], list]:
  """Parses positional arguments for instance QMargins or QMarginsF"""
  for arg in args:
    if isinstance(arg, (QMargins, QMarginsF)):
      return arg, [a for a in args if a != arg]
  return None, [*args, ]


def _parseKeyInts(**kwargs) -> tuple[Optional[Margins], dict]:
  """Parses keyword arguments for keys: left, top, right, bottom. All
  keywords must be present for this function to resolve an instance of
  QMargins."""
  leftKeys = stringList("""left, Left, L, l""")
  topKeys = stringList("""top, Top, T, t""")
  rightKeys = stringList("""right, Right, R, r""")
  bottomKeys = stringList("""bottom, Bottom, B, b""")
  KEYS = [leftKeys, topKeys, rightKeys, bottomKeys]
  margins = dict(left=None, top=None, right=None, bottom=None)
  usedKeys = []
  for ((name, _), keys) in zip(margins.items(), KEYS):
    for key in keys:
      if key in kwargs:
        usedKeys.append(key)
        val = kwargs.get(key)
        if isinstance(val, float):
          if val.is_integer():
            val = int(val)
        if isinstance(val, int):
          margins[name] = val
          break
        e = typeMsg(key, val, int)
        raise TypeError(e)
  values = []
  keys = stringList("""left, top, right, bottom""")
  for key in keys:
    val = margins.get(key, None)
    if val is None:
      break
    if isinstance(val, int):
      values.append(val)
    else:
      e = typeMsg('val', val, int)
      raise TypeError(e)
  else:
    data = {k: v for (k, v) in kwargs.items() if k not in usedKeys}
    return QMargins(*values), data
  return None, kwargs


def _parsePosInts(*args) -> tuple[Optional[Margins], list]:
  """Parses positional arguments for values of integer type. If one is
  found, an instance with all margins at that value is returned. If two
  are found the left and right margins are set to the first and the top
  and bottom the second. If three is found, the second value is used for
  top and for bottom. Otherwise, the first four found will be assigned as
  left, top, right and bottom in the order found. Please note, that if not
  even one value is found, no instance is returned at all. """
  intArgs = [arg for arg in args if isinstance(arg, int)]
  if len(intArgs) == 1:
    val = intArgs[0]
    args = [arg for arg in args if arg not in intArgs]
    return QMargins(val, val, val, val), args
  if len(intArgs) == 2:
    left, top = intArgs
    args = [arg for arg in args if arg not in intArgs]
    return QMargins(left, top, left, top), args
  if len(intArgs) == 3:
    left, top, right = intArgs
    args = [arg for arg in args if arg not in intArgs]
    return QMargins(left, top, right, top), args
  if len(intArgs) > 3:
    left, top, right, bottom = intArgs[:4]
    args = [arg for arg in args if arg not in intArgs]
    return QMargins(left, top, right, bottom), args
  return None, [*args, ]


def parseMargins(*args, **kwargs) -> tuple[Optional[Margins], list, dict]:
  """The parseMargins functions parses positional arguments and keyword
  arguments returning the first received instance of QMargins or
  QMarginsF."""
  keyMargins, kwargs = _parseKeyMargins(**kwargs)
  if keyMargins is not None:
    return keyMargins, [*args, ], kwargs
  posMargins, args = _parsePosMargins(*args)
  if posMargins is not None:
    return posMargins, args, kwargs
  keyInts, kwargs = _parseKeyInts(**kwargs)
  if keyInts is not None:
    return keyInts, args, kwargs
  posInts, args = _parsePosInts(*args)
  if posInts is not None:
    return posInts, args, kwargs
  return None, args, kwargs
