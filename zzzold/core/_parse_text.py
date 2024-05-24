"""The 'parseText' function parses arguments to a string valued text."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.parse import maybe
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg


def _parseKwargs(**kwarg) -> str:
  """Parses the kwargs to a string value."""

  textKeys = stringList("""text, txt, initText, label, header""")
  for key in textKeys:
    if key in kwarg:
      val = kwarg[key]
      if isinstance(val, str):
        return val
      e = typeMsg('text', val, str)
      raise TypeError(e)


def _parseArgs(*args) -> str:
  """Parses the args to a string value."""
  for arg in args:
    if isinstance(arg, str):
      return arg


def parseText(*args, **kwarg) -> str:
  """Parses the text from the input arguments."""
  keyVal = _parseKwargs(**kwarg)
  posVal = _parseArgs(*args)
  return maybe(keyVal, posVal)
