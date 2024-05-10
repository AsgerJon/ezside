"""The hasAbstractMethod function checks if a class has an abstract method.
This allows for classes not inheriting from ABC to still make use of the
abstractmethod decorator. The function returns True if the class has an
abstract method, and False otherwise."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


def hasAbstractMethod(cls) -> bool:
  """Checks if the class has abstract methods."""
  for (key, val) in cls.__dict__.items():
    if callable(val):
      if getattr(val, '__isabstractmethod__', False):
        return True
  return False
