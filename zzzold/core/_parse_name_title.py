"""The parseNameTitle function parses a name and title from arguments. It
allows setting a disallowed name or title."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from vistutils.text import stringList
from vistutils.waitaminute import typeMsg


def parseNameTitle(*args, **kwargs) -> dict[str, Optional[str]]:
  """Parses a name and title from arguments. It allows setting a disallowed
  name or title."""
  exceptValue = kwargs.get('_except', None)
  nameKeys = stringList("""name, Name""")
  titleKeys = stringList("""title, Title""")
  values: dict[str, Optional[str]] = dict(name=None, title=None)
  KEYS = [nameKeys, titleKeys]
  for ((key, val), keys) in zip(values.items(), KEYS):
    for k in keys:
      if k in kwargs:
        val = kwargs.get(k, None)
        if val == exceptValue:
          continue
        if isinstance(val, str):
          values[key] = val
          break
        e = typeMsg(k, val, str)
        raise TypeError(e)
    else:
      for arg in args:
        if isinstance(arg, str):
          if arg == exceptValue:
            continue
          values[key] = arg
          break
      else:
        if kwargs.get('_strict', True):
          e = typeMsg(key, val, str)
          raise ValueError(e)
  return values
