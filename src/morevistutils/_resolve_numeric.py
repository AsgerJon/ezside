"""The 'resolveNumeric' function attempts to resolve a string to a numeric
value. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Union

from morevistutils import resolveHex


def resolveNumeric(value: str) -> Union[int, float, complex]:
  """The 'resolveNumeric' function attempts to resolve a string to a numeric
  value. """
  maybeHex = resolveHex(value)
  if maybeHex is not None:
    return maybeHex
  for num in [int, float, complex]:
    try:
      return num(value)
    except ValueError as valueError:
      if num.__name__ in str(valueError):
        continue
      raise valueError
