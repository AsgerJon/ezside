"""The 'parseAlignments' function parses positional and keyword arguments
to instances of Qt.AlignmentFlag."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from vistutils.parse import maybe
from vistutils.text import stringList, monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import AlignFlag, \
  AlignLeft, \
  AlignHCenter, \
  AlignCenter, \
  AlignRight, AlignTop, AlignVCenter, AlignBottom, resolveEnum

hFlags = [AlignLeft, AlignHCenter, AlignCenter, AlignRight, ]
vFlags = [AlignTop, AlignVCenter, AlignCenter, AlignBottom, ]

hKeys = stringList("""horizontalAlignment, horizontalAlign, horizontal""")
vKeys = stringList("""verticalAlignment, verticalAlign, vertical""")
alignKeys = stringList("""alignment, align, alignFlag""")


def _parseHorizontalKwargs(**kwargs) -> Optional[AlignFlag]:
  """Parses the kwargs to a horizontal alignment value."""
  for key in [*hKeys, *alignKeys]:
    if key in kwargs:
      val = kwargs[key]
      if isinstance(val, AlignFlag):
        return val
      if isinstance(val, (str, int)):
        val = resolveEnum(AlignFlag, val)
        if isinstance(val, AlignFlag):
          return val
      e = typeMsg('horizontalAlignment', val, AlignFlag)
      raise TypeError(e)


def _parseVerticalKwargs(**kwargs) -> Optional[AlignFlag]:
  """Parses the kwargs to a vertical alignment value."""
  for key in [*vKeys, *alignKeys]:
    if key in kwargs:
      val = kwargs[key]
      if isinstance(val, AlignFlag):
        return val
      if isinstance(val, (str, int)):
        val = resolveEnum(AlignFlag, val)
        if isinstance(val, AlignFlag):
          return val
      e = typeMsg('verticalAlignment', val, AlignFlag)
      raise TypeError(e)


def _parseHorizontalArgs(*args) -> Optional[AlignFlag]:
  """Parses the args to a horizontal alignment value."""
  for arg in args:
    if isinstance(arg, AlignFlag):
      return arg
    if isinstance(arg, (str, int)):
      arg = resolveEnum(AlignFlag, arg)
      if isinstance(arg, AlignFlag):
        return arg
    e = typeMsg('horizontalAlignment', arg, AlignFlag)
    raise TypeError(e)


def _parseVerticalArgs(*args) -> Optional[AlignFlag]:
  """Parses the args to a vertical alignment value."""
  for arg in args:
    if isinstance(arg, AlignFlag):
      return arg
    if isinstance(arg, (str, int)):
      arg = resolveEnum(AlignFlag, arg)
      if isinstance(arg, AlignFlag):
        return arg
    e = typeMsg('verticalAlignment', arg, AlignFlag)
    raise TypeError(e)


def parseHorizontalAlignment(*args, **kwargs) -> AlignFlag:
  """The 'parseHorizontalAlignment' function parses positional and keyword
  arguments to instances of Qt.AlignmentFlag. """
  keyVal = _parseHorizontalKwargs(**kwargs)
  posVal = _parseHorizontalArgs(*args)
  return maybe(keyVal, posVal, 0)


def parseVerticalAlignment(*args, **kwargs) -> AlignFlag:
  """The 'parseVerticalAlignment' function parses positional and keyword
  arguments to instances of Qt.AlignmentFlag. """
  keyVal = _parseVerticalKwargs(**kwargs)
  posVal = _parseVerticalArgs(*args)
  return maybe(keyVal, posVal, 0)


def parseAlignment(*args, **kwargs) -> AlignFlag:
  """The 'parseAlignments' function parses positional and keyword arguments
  to instances of Qt.AlignmentFlag."""
  hAlign = parseHorizontalAlignment(*args, **kwargs)
  vAlign = parseVerticalAlignment(*args, **kwargs)
  return hAlign | vAlign
