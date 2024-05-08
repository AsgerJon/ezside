"""The Q class provides a work-around for the dreaded
isinstance function allowing instead:
Q[someInstance::SomeClass] is equivalent to:
isinstance(someInstance, SomeClass)
"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


class Q:
  """Q provides the shortest workaround for isinstance!"""

  def __class_getitem__(cls, item: slice) -> bool:
    """Returns whether the instance is an instance of the class. """
    return True if isinstance(item.start, item.step) else False
