"""FUCK YOU"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from attribox import AttriBox
from icecream import ic

from ezside.widgets.layouts import AlignBox
from vistutils.metas import AbstractNamespace as NS, AbstractMetaclass


class SpaceName(NS):
  """LMAO"""

  def compile(self, *args, **kwargs) -> dict:
    return {k: v for (k, v) in dict.items(self)}


class Hate(AbstractMetaclass):
  """You"""

  def __getitem__(cls, *args, **kwargs) -> Any:
    """Kill yourself"""
    ic(cls, args, kwargs)

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> NS:
    return SpaceName(mcls, name, bases, **kwargs)

  def __new__(mcls, *args, **kwargs) -> Any:
    """LMAO"""
    name, bases, namespace = [*args, None, None][:3]
    attrs = namespace.compile()
    cls = AbstractMetaclass.__new__(mcls, name, bases, attrs, **kwargs)
    setattr(cls, 'lmao', namespace.getAnnotations())
    setattr(cls, 'yolo', namespace.__access_log__)
    return cls


class Cunt(metaclass=Hate):
  """KILL YOURSELF"""

  def __str__(self) -> str:
    """LMAO"""
    return str(self.align)

  def __getitem__(self, item: Any) -> Any:
    """FUCK"""
    # ic(item)

  def hereIsMyNumber(self) -> 69420:
    """This is crazy"""

  def callMeMaybe(self) -> None:
    """lmao"""

  cunt: bool
  shit: bool
