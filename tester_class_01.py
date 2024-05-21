"""LMAO"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import ABCMeta

from icecream import ic

from tester_class_02 import Sussinator

ic.configureOutput(includeContext=True)


@Sussinator(int)
class FakeInt:
  """
  A class that pretends to be an int.
  """

  def __init__(self, value: int) -> None:
    """
    Initialize with a numerical value.
    """
    self.value = value

# Example usage
