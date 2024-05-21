"""The 'parseHorizontalLayout' function parses arguments to a horizontal
alignment values."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from vistutils.parse import maybe
from vistutils.text import stringList

from ezside.core import AlignLeft, \
  AlignHCenter, \
  AlignCenter, \
  AlignRight, AlignFlag, resolveEnum
from ezside.core import AlignTop, AlignVCenter, AlignBottom

HFlags = [AlignLeft, AlignHCenter, AlignCenter, AlignRight, ]
VFlags = [AlignTop, AlignVCenter, AlignCenter, AlignBottom, ]

hFlags = stringList("""horizontalAlignment, horizontalAlign, horizontal""")
vFlags = stringList("""verticalAlignment, verticalAlign, vertical""")
alignKeys = stringList("""alignment, align, alignFlag""")
allKeys = list({*hFlags, *vFlags, *alignKeys})


def _parseHorizontalKwargs(**kwargs) -> AlignFlag:
  """Parses the kwargs to a horizontal alignment value."""
  for key in [*hFlags, *alignKeys]:
    if key in kwargs:
      val = kwargs[key]
      if isinstance(val, AlignFlag):
        return val
      if isinstance(val, (str, int)):
        val = resolveEnum(AlignFlag, val)
        if isinstance(val, AlignFlag):
          return val


def _parseVerticalKwargs(**kwargs) -> AlignFlag:
  """Parses the kwargs to a vertical alignment value."""
  for key in [*vFlags, *alignKeys]:
    if key in kwargs:
      val = kwargs[key]
      if isinstance(val, AlignFlag):
        return val
      if isinstance(val, (str, int)):
        val = resolveEnum(AlignFlag, val)
        if isinstance(val, AlignFlag):
          return val


def _parseHorizontalArgs(*args) -> AlignFlag:
  """Parses the args to a horizontal alignment value."""
  for arg in args:
    if isinstance(arg, AlignFlag):
      return arg
    if isinstance(arg, (str, int)):
      arg = resolveEnum(AlignFlag, arg)
      if isinstance(arg, AlignFlag):
        return arg


def _parseVerticalArgs(*args) -> AlignFlag:
  """Parses the args to a vertical alignment value."""
  for arg in args:
    if isinstance(arg, AlignFlag):
      return arg
    if isinstance(arg, (str, int)):
      arg = resolveEnum(AlignFlag, arg)
      if isinstance(arg, AlignFlag):
        return arg


def parseHorizontalAlignment(*args, **kwargs) -> Optional[AlignFlag]:
  """Parses the horizontal alignment from the input arguments."""
  keyVal = _parseHorizontalKwargs(**kwargs)
  posVal = _parseHorizontalArgs(*args)
  if keyVal in HFlags:
    return keyVal
  if posVal in HFlags:
    return posVal


def parseVerticalAlignment(*args, **kwargs) -> Optional[AlignFlag]:
  """Parses the vertical alignment from the input arguments."""
  keyVal = _parseVerticalKwargs(**kwargs)
  posVal = _parseVerticalArgs(*args)
  if keyVal in VFlags:
    return keyVal
  if posVal in VFlags:
    return posVal


def parseAlignment(*args, **kwargs) -> Optional[AlignFlag]:
  """Parses the alignment from the input arguments."""
  hAlign = parseHorizontalAlignment(*args, **kwargs)
  vAlign = parseVerticalAlignment(*args, **kwargs)
  if isinstance(hAlign, AlignFlag) and isinstance(vAlign, AlignFlag):
    return hAlign | vAlign
