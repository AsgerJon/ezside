"""
A class for managing names in the sentence case format.
Sentence Case capitalizes only the first letter of the first word,
leaving all other words in lowercase.
"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
from morevistutils.casenames import AbstractCase


class SentenceCase(AbstractCase):
  """
  A class for managing names in the sentence case format.
  Sentence Case capitalizes only the first letter of the first word,
  leaving all other words in lowercase.
  """

  @classmethod
  def joinWords(cls, *words: str) -> str:
    """
    Join the words together using the rules of the sentence case.
    """
    if not words:
      return ""
    return words[0].capitalize() + ' ' + ' '.join(
      word.lower() for word in words[1:])

  @classmethod
  def resolveName(cls, name: str) -> list[str]:
    """
    Assuming the name is in sentence case, this method returns a list of
    words
    all in lowercase except the first one capitalized.
    """
    return name.split()
