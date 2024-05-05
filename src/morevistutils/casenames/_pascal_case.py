"""PascalCase is nearly the same as camel case except for beginning with a
capitalized word."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
from morevistutils.casenames import AbstractCase


class PascalCase(AbstractCase):
  """
  A class for managing names consisting of multiple words
  abstracted from the pascal case. PascalCase is similar to camelCase
  but starts with an uppercase letter.
  """

  @classmethod
  def joinWords(cls, *words: str) -> str:
    """
    Join the words together using the rules of the pascal case.
    """
    return ''.join(word.capitalize() for word in words)

  @classmethod
  def resolveName(cls, name: str) -> list[str]:
    """
    Assuming the name is of this case, this method is expected to
    return a list of lower case versions of the constituent words.
    The first character of each word is expected to be uppercase.
    """
    words = []
    word = []
    for char in name:
      if char.isupper():
        if word:
          words.append(''.join(word))
        word = [char.lower()]
      else:
        word.append(char)
    if word:
      words.append(''.join(word))
    return words
