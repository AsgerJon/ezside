"""The 'parseSpacing' function parses the spacing value from arguments."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.text import stringList
from vistutils.waitaminute import typeMsg


def parseSpacing(*args, **kwargs) -> tuple[int, list, dict]:
  """The 'parseSpacing' function parses the spacing value from arguments."""
  spacingKeys = stringList("""spacing, gap, space""")
  for key in spacingKeys:
    if key in kwargs:
      val = kwargs[key]
      if isinstance(val, int):
        keyArgs = {k: v for (k, v) in kwargs.items() if k != key}
        return val, [*args, ], keyArgs
      e = typeMsg(key, val, int)
      raise TypeError(e)
  else:
    for arg in args:
      if isinstance(arg, int):
        posArgs = [a for a in args if a != arg]
        return arg, posArgs, {**kwargs, }
    else:
      return -1, [*args, ], {**kwargs, }
