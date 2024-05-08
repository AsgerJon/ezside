"""FUCK YOU"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from attribox import AttriBox
from icecream import ic

from ezside.widgets.layouts import AlignBox


class Hate(type):
  """You"""

  def __getitem__(cls, *args, **kwargs) -> Any:
    """Kill yourself"""
    ic(cls, args, kwargs)


class Cunt:
  """KILL YOURSELF"""

  align = AttriBox[AlignBox]()

  def __str__(self) -> str:
    """LMAO"""
    return str(self.align)

  def __getitem__(self, item: Any) -> Any:
    """FUCK"""
    # ic(item)
