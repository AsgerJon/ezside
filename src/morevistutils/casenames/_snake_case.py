"""SnakeCase subclasses AbstractCase providing an abstraction of the snake
case representation of variable names. For example, if a variable name are
to represent the top-left corner of a rectangle, a snake case version of
the variable name might be: 'top-left-corner'. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from morevistutils.casenames import AbstractCase


class SnakeCase(AbstractCase):
  """A class for managing names consisting of multiple words abstracted from
  the snake case. Instances can be created from different cases and more
  words may be added to an existing instance. The class provides conversion
  back to any of the supported cases. """

  @classmethod
  def joinWords(cls, *words: str) -> str:
    """Join the words together using the rules of the case."""
    return '_'.join(words)

  @classmethod
  def resolveName(cls, name: str) -> list[str]:
    """Assuming the name is of this case, this method is expected to
    return a list of lower case versions of the constituent words. """
    return name.split('_')
