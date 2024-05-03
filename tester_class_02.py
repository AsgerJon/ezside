"""FUCK ME"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any


class SomeClass:
  """LMAO"""

  def __getattr__(self, key: str) -> None:
    """YOLO"""
    print('SomeClass.__getattr__(self, %s)' % key)
    raise AttributeError(key)


class AnotherClass:
  """LMAO"""

  def __getattr__(self, key: str) -> Any:
    """LMAO"""
    return 'AnotherClass.__getattr__(self, %s)' % key
