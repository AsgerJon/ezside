"""Font encapsulates settings for fonts and text rendering."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field, AttriBox
from worktoy.meta import BaseObject

from ezside.tools import FontWeight, FontFamily, FontCap


class Font(BaseObject):
  """Font encapsulates settings for fonts and text rendering."""

  weight = AttriBox[FontWeight](FontWeight.NORMAL)
  size = AttriBox[int](12)
  family = AttriBox[FontFamily](FontFamily.COURIER)
  cap = AttriBox[FontCap](FontCap.MIX)

  size = Field()
  family = Field()
  cap = Field()
  italic = Field()
  underline = Field()
  strike = Field()

  align = Field()
  color = Field()
