"""The 'parseRect' function parses rectangles from the arguments"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Optional

from PySide6.QtCore import QMarginsF, QMargins
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

sourceKeys = stringList("""source, sourceRect, sourceRectangle""")
targetKeys = stringList("""target, targetRect, targetRectangle""")
staticKeys = stringList("""staticRect, staticRectangle, static""")
movingKeys = stringList("""movingRect, movingRectangle, moving""")

Margin = QMargins | QMarginsF
Margins = tuple[Margin, Margin]


def parseKwargsSourceTargetRect(*args, **kwargs) -> Margins:
  """Parses the keyword arguments to source and target rectangles."""
  rects = dict(static=None, moving=None)
  KEYS = [staticKeys, movingKeys]
  for ((name, val), keys) in zip(kwargs.items(), KEYS):
    for key in keys:
      if key in kwargs:
        rect = kwargs[key]
        if isinstance(rect, (QMargins, QMarginsF)):
          rects[name] = rect
          break
        e = typeMsg(name, rect, QMargins)
        raise TypeError(e)
    else:
      for arg in args:
        if isinstance(arg, (QMargins, QMarginsF)):
          if arg not in [v for (k, v) in rects.items()]:
            rects[name] = arg
            break
      else:
        e = """Unable to parse the source and target rectangles from the
        given arguments!"""
        raise ValueError(e)
  return rects.get('static'), rects.get('moving')


def parseRect(*args, **kwargs) -> Optional[Margin]:
  """Parses the arguments to the first rectangle received. """
  rectKeys = stringList("""rect, rectangle, QRect, QRectF""")
  for key in rectKeys:
    if key in kwargs:
      val = kwargs.get(key)
      if isinstance(val, (QMargins, QMarginsF)):
        return val
      e = typeMsg('rect', val, QMargins)
      raise TypeError(e)
  else:
    for arg in args:
      if isinstance(arg, (QMargins, QMarginsF)):
        return arg
    else:
      if kwargs.get('strict', True):
        e = """Unable to parse the rectangle from the given arguments!"""
        raise ValueError(e)
