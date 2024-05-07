"""The SmartMap enhances the flexibility of the standard dictionary
allowing keys to support cross-case lookups. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from morevistutils.casenames import Key


class SmartMap(dict):
  """The SmartMap enhances the flexibility of the standard dictionary
  allowing keys to support cross-case lookups. """

  def __getitem__(self, name: str) -> object:
    """Get the value of the key."""
    return dict.__getitem__(self, Key(name))

  def __setitem__(self, name: str, value: object) -> None:
    """Set the value of the key."""
    dict.__setitem__(self, Key(name), value)

  def __contains__(self, name: str) -> bool:
    """Return True if the key is in the SmartMap."""
    for key in self:
      if name in Key(key):
        return True
    return False

  def __delitem__(self, name: str) -> None:
    """Delete the key."""
    dict.__delitem__(self, Key(name))

  def get(self, name: str, default: object = None) -> object:
    """Get the value of the key."""
    return dict.get(self, Key(name), default)
