"""The 'parseLineLength' function parses arguments to integer valued line
length."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from vistutils.parse import maybe
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg


def _parseKwargs(**kwarg) -> Optional[int]:
  """Parses the kwargs to an integer value."""

  lineLenKeys = stringList("""lineLength, lines, lineLen, line_length""")
  for key in lineLenKeys:
    if key in kwarg:
      val = kwarg[key]
      if isinstance(val, int):
        if val > 0:
          return val
        e = """Received negative value for line length!"""
        raise ValueError(e)
      e = typeMsg('lineLength', val, int)
      raise TypeError(e)


def _parseInts(*args) -> Optional[int]:
  """Parses the args to an integer value."""
  for arg in args:
    if isinstance(arg, int):
      if arg > 0:
        return arg
      e = """Received negative value for line length!"""
      raise ValueError(e)


def parseLineLength(*args, **kwarg) -> Optional[int]:
  """Parses the line length from the input arguments."""
  keyVal = _parseKwargs(**kwarg)
  posVal = _parseInts(*args)
  return maybe(keyVal, posVal)
