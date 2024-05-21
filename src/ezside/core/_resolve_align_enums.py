"""This module provides functions that resolve alignment enum names."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from ezside.core import AlignFlag


def resolveAlign(*args, **kwargs) -> AlignFlag:
  """This module provides functions that resolve alignment enum names."""
  alignmentKeys = stringList("""alignment, align, alignFlag, 
  alignFlagName,""")
  for key in alignmentKeys:
    if key in kwargs:
      val = kwargs.get(key)
      if isinstance(val, AlignFlag):
        return val
      if isinstance(val, (str, int)):
        return resolveAlign(val)
      e = typeMsg('alignment', val, AlignFlag)
      raise TypeError(e)
  else:
    name, value = None, None
    for arg in args:
      if isinstance(arg, str) and name is None:
        name = arg
      elif isinstance(arg, int) and value is None:
        value = arg

    for key, val in AlignFlag:
      if name is not None and key.lower() == name.lower():
        return val
      if value is not None and val == value:
        return val
