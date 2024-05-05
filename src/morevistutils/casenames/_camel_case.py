"""CamelCase subclasses AbstractCase providing an abstraction of the camel
case representation of variable names. For example, if a variable name are
to represent the top-left corner of a rectangle, a camel case version of
the variable name might be: 'topLeftCorner'. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from morevistutils.casenames import AbstractCase


class CamelCase(AbstractCase):
  """A class for managing names consisting of multiple words abstracted from
  the camel case. Instances can be created from different cases and more
  words may be added to an existing instance. The class provides conversion
  back to any of the supported cases. """

  @classmethod
  def joinWords(cls, *words: str) -> str:
    """Join the words together using the rules of the case."""
    if not words:
      return ''
    name = words[0]
    return ''.join([name, *[word.capitalize() for word in words[1:]]])

  @classmethod
  def resolveName(cls, name: str = None) -> list[str]:
    """Assuming the name is of this case, this method is expected to
    return a list of lower case versions of the constituent words. """
    if name is None:
      return []
    words = []
    word = []
    for char in name:
      if char.isupper():
        words.append(''.join(word))
        word = [char.lower()]
      else:
        word.append(char)
    else:
      words.append(''.join(word))
    return words
