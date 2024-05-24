"""The 'resolveHex' receives a string representation of the hexadecimal value
and returns the integer value. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional as Maybe


def resolveHex(arg: str) -> Maybe[int]:
  """The 'resolveHexColor' function creates a QColor instance from a
  hexadecimal string. """
  hexVals = {k: i for i, k in enumerate('0123456789ABCDEF')}
  return sum([hexVals[c] * 16 ** i for i, c in enumerate(reversed(arg))])
