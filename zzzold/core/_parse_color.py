"""The 'parseColor' creates an instance of QColor from positional
arguments and keyword arguments. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional as Maybe

from PySide6.QtGui import QColor
from icecream import ic
from vistutils.text import stringList, monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import colorDict
from morevistutils import resolveNumeric, resolveHex

ic.configureOutput(includeContext=True)


def _parseNamedColor(*args, **kwargs) -> Maybe[QColor]:
  """Attempts to find color named as the positional argument. """
  colorName = [*args, None][0]
  if colorName is None:
    return
  if not isinstance(colorName, str):
    return
  ic(colorName)
  if isinstance(colorName, str):
    colorVal = colorDict.get(colorName, None)
    if colorVal is not None:
      if isinstance(colorVal, QColor):
        return colorVal
      e = typeMsg(colorName, colorVal, QColor)
      raise TypeError(e)
  for (key, val) in colorDict.items():
    if key.lower() == colorName.lower():
      if isinstance(val, QColor):
        return val


def _parseKwargs(*args, **kwargs) -> Maybe[QColor]:
  """The '_parseKwargs' function creates a QColor instance from keyword
  arguments. """
  redKeys = stringList("""red, r, R, RED, Red""")
  greenKeys = stringList("""green, g, G, GREEN, Green""")
  blueKeys = stringList("""blue, b, B, BLUE, Blue""")
  alphaKeys = stringList("""alpha, a, A, ALPHA, Alpha""")
  values: dict[str, Maybe[int]] = dict(red=None,
                                       green=None,
                                       blue=None,
                                       alpha=255)
  KEYS = [redKeys, greenKeys, blueKeys, alphaKeys]
  for ((name, _), keys) in zip(values.items(), KEYS):
    for key in keys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, str):
          maybeHex = resolveHex(val)
          if maybeHex is not None:
            values[name] = maybeHex
            break
          maybeNum = resolveNumeric(val)
          if maybeNum is not None:
            values[name] = maybeNum
            break
        if isinstance(val, int):
          values[name] = val
          break
        if isinstance(val, float):
          if 0 <= val <= 1:
            values[name] = int(val * 255)
            break
  if None in values.values():
    return
  red, green, blue, alpha = (values['red'],
                             values['green'],
                             values['blue'],
                             values['alpha'])
  if all([isinstance(val, int) for val in values.values()]):
    if all([0 <= val <= 255 for val in values.values()]):
      return QColor(red, green, blue, alpha)


def _parsePosColor(*args, **kwargs) -> Maybe[QColor]:
  """The '_parseQColor' function creates a QColor instance from a QColor
  instance. """
  for arg in args:
    if isinstance(arg, QColor):
      return arg


def _parseKeyColor(*args, **kwargs) -> Maybe[QColor]:
  """The '_parseKeyColor' function creates a QColor instance from a QColor
  instance. """
  colorKeys = stringList("""color, c, C, COLOR, Color""")
  for color in colorKeys:
    if color in kwargs:
      val = kwargs[color]
      if isinstance(val, QColor):
        return val
      e = typeMsg(color, val, QColor)
      raise TypeError(e)


def _parseInt(*args, **kwargs) -> Maybe[QColor]:
  """The '_parseInt' function returns an integer if it is the only
  argument. """
  intArgs = []
  for arg in args:
    if isinstance(arg, int):
      if 0 <= arg <= 255:
        intArgs.append(arg)
      else:
        e = """The integer argument must be between 0 and 255, 
        but received '%d!""" % arg
        raise ValueError(monoSpace(e))
  if len(intArgs) == 3:
    return QColor(*intArgs, 255)
  if len(intArgs) > 3:
    return QColor(*intArgs[:4])


def _parseFloat(*args, **kwargs) -> Maybe[QColor]:
  """The '_parseFloat' function returns a float if it is the only
  argument. """
  floatArgs = []
  for arg in args:
    if isinstance(arg, float):
      if 0 <= arg <= 1:
        floatArgs.append(int(arg * 255))
      else:
        e = """The float argument must be between 0 and 1, 
        but received '%f!""" % arg
        raise ValueError(monoSpace(e))
  if len(floatArgs) == 3:
    return QColor(*floatArgs, 255)
  if len(floatArgs) > 3:
    return QColor(*floatArgs[:4])


def parseColor(*args, **kwargs) -> Maybe[QColor]:
  """The 'parseColor' function creates a QColor instance from positional
  arguments and keyword arguments. """
  parsers = [_parsePosColor, _parseKeyColor, _parseKwargs, _parseInt,
             _parseFloat, _parseNamedColor]
  for parser in parsers:
    maybeColor = parser(*args, **kwargs)
    if maybeColor is not None:
      return maybeColor
