"""The auto singleton should be used to include the name as an enum
instance"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from attribox import Singleton


class auto(metaclass=Singleton):
  """LMAO"""

  def __call__(self, *args, **kwargs) -> type:
    """This is crazy!"""
    return auto
